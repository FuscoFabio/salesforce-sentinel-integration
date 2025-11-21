# Low Level Design – Salesforce → Sentinel Integration

Documento di dettaglio per l’infrastruttura Azure che orchestri il polling dagli Event Log Files Salesforce e l’ingestione verso Microsoft Sentinel (Log Analytics).

## 1. Panoramica
- **Obiettivo**: estrarre Event Log Files critici (Login/Logout/API/…) da Salesforce, trasformarli in formato SIEM e inviarli a Log Analytics, con supporto multi-ambiente (dev, collaudo, produzione).
- **Componenti principali**: Azure Functions (timer trigger), Storage account, Log Analytics Workspace + Microsoft Sentinel, Azure Key Vault, Application Insights, Azure DevOps Pipelines per il CI/CD.

## 2. Architettura
```
Salesforce Event Log Files
        ↓ OAuth (Password/JWT)
Azure Function (timer trigger)
        ↓ Trasformazione SIEM + batching
Azure Log Analytics Workspace
        ↓
Microsoft Sentinel
```

### 2.1 Ambienti
| Ambiente | Function App | Log Type | Environment tag |
|----------|--------------|----------|-----------------|
| Dev      | `salesforce-sentinel-dev` | `SalesforceDev_CL` | `dev` |
| Collaudo | `salesforce-sentinel-test`| `SalesforceTest_CL`| `test` |
| Prod     | `salesforce-sentinel-prod`| `SalesforceProd_CL`| `prod` |

Tutte le Function App puntano allo stesso Log Analytics workspace, differenziando i dati via `LogAnalytics__LogType` e `Environment__Name`.

## 3. Componenti Azure

### 3.1 Function App (Python)
- **Trigger**: `TimerTrigger` (`0 */5 * * * *`, configurabile).
- **Runtime**: Python 3.13, Functions v4.
- **Plan**: Consumption (default) o Premium per cold-start ridotti.
- **Settings principali**:
  - Salesforce (`Salesforce__*`), inclusi `Salesforce__AuthMode` (`password` / `jwt`), `Salesforce__JwtPrivateKey` o `Salesforce__JwtPrivateKeyPath`, `Salesforce__LoginUrl`, `Salesforce__JwtSubject`.
  - Log Analytics (`LogAnalytics__WorkspaceId`, `LogAnalytics__WorkspaceKey`, `LogAnalytics__LogType`).
  - `Environment__Name` per tagging.
- Checkpoint persistente (consigliato):
  - `Checkpoint__StorageConnectionString`
  - `Checkpoint__TableName`, `Checkpoint__PartitionKey`, `Checkpoint__RowKey`
  - `Checkpoint__OverlapMinutes`, `Checkpoint__FallbackHours`
- Altre opzioni: `Salesforce__JwtLifetimeSeconds`.
- **Monitoring**: Application Insights collegato; diagnostic logs inviati al workspace.

### 3.2 Storage Account
- Necessario per la Function (AzureWebJobsStorage).
- Contiene:
  - **Table Storage** per la tabella `Checkpoint__TableName` dove viene salvata `LastProcessedDate`.
  - **Blob/Queue** (in futuro, se si introduce pattern a coda).
- Abilitare firewall + VNet se richiesto; sfruttare Managed Identity per accesso e per l’eventuale Key Vault reference della connection string.

### 3.3 Log Analytics Workspace + Microsoft Sentinel
- Workspace unico con Sentinel abilitato.
- Riceve eventi tramite Data Collector API (tabella `Salesforce*_CL`).
- Sentinel usa query KQL, workbook e regole su quelle tabelle.

### 3.4 Azure Key Vault
- Conserva segreti critici:
  - `Salesforce__ConsumerSecret`, `Salesforce__Password`, `Salesforce__SecurityToken`.
  - Chiavi private per il JWT (PEM/base64). Eventualmente salvate come secret multiline.
- Function App con Managed Identity → Key Vault Access Policy / RBAC.
- App settings usano Key Vault references (`@Microsoft.KeyVault(...)`).

### 3.5 Application Insights
- Abilitato per ogni Function App.
- Metriche monitorate: durata esecuzione, eccezioni, dipendenze (Salesforce/Log Analytics).
- Alert:
  - errori >=3 negli ultimi X minuti;
  - durata media > soglia;
  - zero eventi ingestiti per > N run.

### 3.6 CI/CD (Azure DevOps Pipelines)
- Pipeline definita in `azure-pipelines.yml` con stage: Build, Deploy Dev, Deploy Collaudo, Deploy Prod.
- Variabili principali:
  - `azureServiceConnection` (service connection ARM);
  - `devFunctionApp`, `testFunctionApp`, `prodFunctionApp`;
  - `functionProjectPath`.
- Ogni stage di deploy usa il task `AzureFunctionApp@1` (Linux, Python 3.13) e si appoggia agli ambienti Azure DevOps per approvazioni manuali.
- La pipeline installa i requirements per validazione e poi pubblica direttamente la cartella della Function App (il runtime installa le dipendenze al primo avvio).

## 4. Flussi Dettagliati

### 4.1 Polling Salesforce
1. Timer trigger avvia `salesforce_sentinel_polling`.
2. `SalesforceClient` autentica:
   - **Password flow**: `grant_type=password`.
   - **JWT flow**: genera assertion firmata con private key (RS256) e scambia token (`grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer`).
3. Recupera `EventLogFile` per intervallo (ultimi 5 minuti + margine).
4. Scarica ogni file CSV e lo trasforma in eventi SIEM (classe `DataTransformer`).

### 4.2 Invio a Log Analytics
1. Eventi aggregati in `all_events`.
2. Batch da 1000 eventi (≈30 MB) inviati tramite `LogAnalyticsClient`.
3. Ogni record include `Environment` (se impostato).
4. In caso di errore: log + retry sul batch successivo.
5. Salvataggio checkpoint su Azure Table Storage (`Checkpoint__*`) con timestamp dell’ultimo evento processato.

## 5. Scaling-Out / Performance
- Vedi `docs/implementation/scaling-out.md` per raccomandazioni complete.
- Punti chiave:
  - valutare Premium Plan per cold start;
  - ridurre intervallo timer o usare pipeline a coda;
  - parallelizzare download/parse con limiti di concorrenza;
  - sfruttare il checkpoint persistente per mantenere esecuzioni idempotenti;
  - monitorare `REQUEST_LIMIT_EXCEEDED` e applicare backoff.

## 6. Sicurezza
- **Segreti**: centralizzati in Key Vault; niente segreti hardcoded.
- **Managed Identity**: usato per Key Vault, Storage, eventuali code.
- **Network**: opzionale VNet integration, private endpoint per Storage/Key Vault/Log Analytics se richiesto.
- **Salesforce**: Connected App con certificato per JWT; utente con permessi minimali (solo Event Monitoring).
- **Log Analytics**: accesso limitato tramite RBAC Azure + Sentinel.

## 7. Logging e Observability
- Application Insights (telemetria runtime).
- Log Analytics (dati ingestiti, query KQL per health check).
- Alerting incrociato (Insights + Sentinel).
- Uso del campo `Environment` per filtrare i log per ambiente.

## 8. Deployment & Configurazione
- Provisioning infrastruttura tramite Bicep/Terraform o manuale (Function App, Storage, Insights, Key Vault, Workspace, ambienti).
- Pipeline Azure DevOps (`azure-pipelines.yml`):
  - Stage sequenziali con ambienti Dev/Test/Prod per sfruttare approvazioni.
  - Task `AzureFunctionApp@1` con pacchetto dalla cartella `azure-function/salesforce-sentinel-polling`.
- Configurazioni differenziate per ambiente tramite:
  - App settings (`Environment__Name`, `LogAnalytics__LogType`, variabili Salesforce, checkpoint).
  - Variable group / Library per i nomi delle Function App e Service Connection condiviso.

## 9. Roadmap Tecnica
- Introdurre queue trigger per scaling ulteriore.
- Automazione Bicep/Terraform dell’infrastruttura.
- Workbook Sentinel dedicato per la soluzione Salesforce.

## 10. Riferimenti
- `azure-function/salesforce-sentinel-polling/README.md`
- `docs/implementation/scaling-out.md`
- `DEPLOYMENT.md`
- [Azure Functions scale and hosting](https://learn.microsoft.com/azure/azure-functions/functions-scale)
- [Salesforce JWT OAuth Flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm)
- [Azure Functions + Azure Pipelines](https://learn.microsoft.com/azure/azure-functions/functions-how-to-azure-devops)

