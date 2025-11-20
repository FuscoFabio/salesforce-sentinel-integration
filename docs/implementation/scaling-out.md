# Guida allo Scaling-Out della Salesforce → Sentinel Function

Questa guida descrive come dimensionare e orchestrare l'Azure Function `salesforce-sentinel-polling` per gestire in modo efficiente volumi crescenti di Event Log Files Salesforce mantenendo costi e latenze sotto controllo.

## Obiettivi
- Ridurre il tempo complessivo di ingestione quando aumentano gli eventi da Salesforce
- Evitare il superamento dei rate limit Salesforce e i limiti di Log Analytics
- Garantire affidabilità e recupero rapido in caso di errori o picchi imprevisti

## Leve di Scaling

### 1. Piano di Esecuzione
- **Consumption (default)**: scala automaticamente fino al limite della regione. Usa `WEBSITE_MAX_DYNAMIC_APPLICATION_SCALE_OUT` per controllare il numero massimo di istanze.
- **Elastic Premium / Dedicated**: fornisce istanze pre-warm e scaling prevedibile. Consigliato se il timer deve partire senza cold start o con finestre molto strette.

### 2. Timer e Scheduling
- Il trigger attuale (`0 */5 * * * *`) esegue ogni 5 minuti. Per volumi maggiori:
  - Riduci l’intervallo (es. ogni 2 minuti) per diminuire la quantità di eventi per run.
  - Pianifica esecuzioni aggiuntive solo nelle fasce orarie critiche usando più Function App dedicate (dev/test/prod) oppure orchestrando cron diversificati.

### 3. Batch e Concorrenza
- Mantieni l’invio in batch verso Log Analytics (1000 eventi ~30 MB). Se necessario aumenta/diminuisci il batch in base alla dimensione media degli eventi.
- Parallelizza operazioni IO-bound:
  - Scarico Event Log Files in parallelo (es. `asyncio` o thread pool limitato).
  - Trasformazione CSV concorrente rispettando la memoria disponibile.
- Evita di superare i rate limit Salesforce introducendo un **limitatore di richieste** (max 10 download concorrenti, backoff esponenziale su `REQUEST_LIMIT_EXCEEDED`).

### 4. Persistenza Checkpoint
- La function salva automaticamente il checkpoint su **Azure Table Storage** quando configuri `Checkpoint__StorageConnectionString` (altri parametri: `Checkpoint__TableName`, `Checkpoint__PartitionKey`, `Checkpoint__RowKey`).
- Usa `Checkpoint__OverlapMinutes` (default 5) per aggiungere una finestra di sicurezza tra una run e l'altra e `Checkpoint__FallbackHours` per definire il recupero in assenza di dati.
- Persistendo il checkpoint puoi:
  - Scalare su più istanze senza duplicare gli eventi.
  - Ridurre il range di polling alla finestra minima richiesta.

### 5. Pattern con Code/Queue
- Per picchi estremi, separa i ruoli:
  - **Function timer**: estrae e mette i record in una coda (Storage Queue/Event Hub).
  - **Function queue trigger**: scala automaticamente in risposta al backlog e invia a Log Analytics.
- Con Durable Functions puoi orchestrare fan-out/fan-in mantenendo stato e checkpoint automatici.

### 6. Monitoraggio e Telemetria
- Abilita Application Insights e crea alert su:
  - Durata media e 95° percentile del timer trigger.
  - Numero di eventi per run e tasso di errori.
  - Eventuali risposte `429`/`REQUEST_LIMIT_EXCEEDED`.
- Usa Sentinel/Log Analytics per verificare il volume ingestito:
  ```kql
  Salesforce_CL
  | summarize count() by Environment, bin(TimeGenerated, 5m)
  ```
  In base ai trend, adegua il cron o il batch size.

### 7. Configurazioni per Ambiente
- Ogni Function App (dev, collaudo, prod) può usare lo stesso workspace, ma con:
  - `Environment__Name` diverso per riconoscere il volume/latency per ambiente.
  - `LogAnalytics__LogType` differenziato per filtri più rapidi.
  - Parametri dedicati (`Salesforce__AuthMode`, `Salesforce__JwtSubject`, timer) così puoi scalare solo dove serve.

### 8. Best Practice di Sicurezza durante lo Scaling
- Usa Managed Identity + Key Vault per le chiavi JWT quando aumenti il numero di istanze.
- Limita i permessi Salesforce dell’utente di integrazione (solo Event Log Files).

## Procedura Consigliata
1. **Stimare il volume**: definisci eventi min/max per finestra.
2. **Scegli il piano**: inizia con Consumption, passa a Premium se il cold start impatta gli SLA.
3. **Ottimizza cron/batch**: riduci la finestra di polling e calibra il batch.
4. **Implementa checkpoint persistente** e, se necessario, pipeline a coda.
5. **Monitora e adatta**: crea workbook/alert per reagire a code o latenze.

## Riferimenti
- [Azure Functions scale and hosting](https://learn.microsoft.com/azure/azure-functions/functions-scale)
- [Salesforce Event Monitoring API Limits](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/sforce_api_objects_eventlogfile.htm)
- [Azure Durable Functions patterns](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview)

