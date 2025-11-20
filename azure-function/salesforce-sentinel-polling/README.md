# Azure Function: Salesforce to Sentinel Polling

Azure Function serverless in Python per il polling schedulato di eventi Salesforce e invio ad Azure Log Analytics (Sentinel).

## Panoramica

Questa Azure Function esegue polling ogni **5 minuti** per:
1. Estrarre Event Log Files da Salesforce tramite API
2. Trasformare gli eventi in formato SIEM
3. Inviare gli eventi ad Azure Log Analytics per l'analisi in Sentinel

## Caratteristiche

- ✅ **Serverless e Scalabile**: Esegue su Azure Functions Consumption Plan
- ✅ **Polling Schedulato**: Timer Trigger ogni 5 minuti
- ✅ **Eventi SIEM**: Estrae eventi critici (Login, Logout, API, URI, Report, Dashboard)
- ✅ **Trasformazione Dati**: Converte eventi Salesforce in formato standard SIEM
- ✅ **Invio Batch**: Ottimizzato per inviare eventi in batch a Log Analytics
- ✅ **Gestione Errori**: Retry automatico e logging completo
- ✅ **Checkpointing**: Traccia eventi già processati (da implementare con storage persistente)

## Architettura

```
Salesforce Event Log Files API
    ↓
Azure Function (Timer Trigger - 5 min)
    ↓
Trasformazione Dati SIEM
    ↓
Azure Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Prerequisiti

- Azure Subscription
- Azure Function App (Consumption o Premium Plan)
- Log Analytics Workspace con Azure Sentinel abilitato
- Credenziali Salesforce:
  - Consumer Key (Client ID)
  - Consumer Secret (Client Secret)
  - Username
  - Password
  - Security Token
- Workspace ID e Primary Key di Log Analytics

## Configurazione

### 1. Variabili d'Ambiente

Configura le seguenti variabili d'ambiente nella Function App:

**Salesforce:**
```
Salesforce__ConsumerKey=<your-consumer-key>
Salesforce__ConsumerSecret=<your-consumer-secret>
Salesforce__Username=<salesforce-username>
Salesforce__Password=<salesforce-password>
Salesforce__SecurityToken=<security-token>
Salesforce__AuthMode=password
Salesforce__LoginUrl=https://login.salesforce.com
# Valori per JWT (opzionali, usa PEM o base64)
Salesforce__JwtPrivateKey=<base64-o-PEM>
Salesforce__JwtPrivateKeyPath=/path/to/key.pem
Salesforce__JwtAudience=https://login.salesforce.com
Salesforce__JwtSubject=<integration-user@company.com>
Salesforce__JwtLifetimeSeconds=300
```

**Log Analytics:**
```
LogAnalytics__WorkspaceId=<workspace-id>
LogAnalytics__WorkspaceKey=<workspace-key>
LogAnalytics__LogType=Salesforce_CL
Environment__Name=dev
```

> Suggerimento: usa `LogAnalytics__LogType` e/o `Environment__Name` diversi per distinguere gli ambienti (es. `SalesforceDev_CL`, `Environment__Name=collaudo`).

**Checkpoint Persistente (Azure Table Storage):**
```
Checkpoint__StorageConnectionString=<azure-storage-connection-string>
Checkpoint__TableName=SalesforceCheckpoints
Checkpoint__PartitionKey=Salesforce
Checkpoint__RowKey=EventLogPolling
Checkpoint__OverlapMinutes=5
Checkpoint__FallbackHours=24
```

> Se non imposti `Checkpoint__StorageConnectionString`, la function userà un fallback (ultime 24 ore) ma è consigliato abilitare il checkpoint persistente per evitare duplicati/mancate letture.

### 2. Ottenere Credenziali Salesforce

1. Vai a **Setup** → **App Manager** → **New Connected App**
2. Abilita **OAuth Settings**
3. Seleziona OAuth Scopes:
   - `Manage user data via APIs (api)`
   - `Perform requests on your behalf at any time (refresh_token, offline_access)`
4. Copia **Consumer Key** e **Consumer Secret**
5. Genera **Security Token** da **Setup** → **My Personal Information** → **Reset My Security Token**

> Se vuoi usare l'autenticazione con certificato (JWT Bearer Flow), carica il certificato X.509 nella Connected App e imposta `Salesforce__AuthMode=jwt`. La Function utilizza la chiave privata (PEM o base64) per firmare il token JWT e ottenere l'access token senza password/security token.

### Modalità di Autenticazione Supportate

- `Salesforce__AuthMode=password` (default): usa Username + Password (+ Security Token).
- `Salesforce__AuthMode=jwt`: usa il JWT Bearer Flow con certificato. Richiede:
  - `Salesforce__JwtPrivateKey` **oppure** `Salesforce__JwtPrivateKeyPath`
  - `Salesforce__JwtSubject` (utente Salesforce su cui impersonarsi, di default `Salesforce__Username`)
  - `Salesforce__JwtAudience` se usi un domain diverso (es. sandbox)
  - facoltativo `Salesforce__JwtLifetimeSeconds` per personalizzare la durata dell'assertion.

Puoi salvare la chiave privata in Azure Key Vault e referenziarla tramite app setting (Key Vault reference) oppure montare un file durante il deployment.

### 3. Ottenere Credenziali Log Analytics

1. Vai al portale Azure → **Log Analytics workspaces**
2. Seleziona il workspace
3. Vai a **Agents management** → **Log Analytics agent instructions**
4. Copia **Workspace ID** e **Primary key**

### 4. Deployment

#### Opzione A: Azure Portal

1. Crea una nuova Function App nel portale Azure
2. Seleziona **Python** come runtime stack
3. Carica i file della function
4. Configura le variabili d'ambiente

#### Opzione B: Azure Functions Core Tools

```bash
# Installa Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Login ad Azure
az login

# Deploy
func azure functionapp publish <function-app-name>
```

#### Opzione C: VS Code

1. Installa estensione "Azure Functions" per VS Code
2. Apri la cartella della function
3. Clicca su "Deploy to Function App"

## Eventi Supportati

La function estrae i seguenti tipi di eventi da Salesforce:

### Priorità Critica
- **LoginEvent**: Accessi utente
- **LogoutEvent**: Disconnessioni
- **ApiEvent**: Chiamate API

### Priorità Alta
- **UriEvent**: Navigazione e accessi a record
- **ReportEvent**: Accessi a report
- **DashboardEvent**: Accessi a dashboard
- **DataExportEvent**: Esportazioni dati

## Schema Dati

Gli eventi vengono trasformati in formato standard SIEM con i seguenti campi:

### Campi Comuni
- `TimeGenerated`: Timestamp evento (ISO 8601 UTC)
- `EventType`: Tipo di evento (LoginEvent, ApiEvent, ecc.)
- `SourceSystem`: "Salesforce"
- `Environment`: Ambiente applicativo (dev/collaudo/prod) se configurato
- `UserId`: ID utente Salesforce
- `Username`: Username utente
- `SourceIp`: IP di origine

### Campi Specifici per LoginEvent
- `LoginType`: Tipo di login (Web, Mobile, API)
- `Status`: Success/Failure
- `Browser`: Browser utilizzato
- `Platform`: Sistema operativo
- `LoginGeoId`: Geolocalizzazione
- `SessionKey`: Chiave sessione

### Campi Specifici per ApiEvent
- `ApiType`: Tipo API (REST, SOAP, Bulk)
- `ApiVersion`: Versione API
- `Method`: Metodo HTTP (GET, POST, PUT, DELETE)
- `Url`: Endpoint chiamato
- `Status`: Codice risposta HTTP
- `ResponseTime`: Tempo di risposta (ms)
- `Client`: Client utilizzato

## Monitoraggio

### Application Insights

La function integra automaticamente Application Insights per:
- Metriche di esecuzione
- Log di errore
- Performance tracking
- Dependency tracking

### Query KQL per Monitoraggio

```kql
// Verifica eventi inviati
Salesforce_CL
| summarize count() by EventType, bin(TimeGenerated, 5m)
| render timechart

// Errori nella function
traces
| where message contains "salesforce-sentinel-polling"
| where severityLevel >= 3
| project timestamp, message, severityLevel

// Performance
requests
| where name contains "salesforce-sentinel-polling"
| summarize avg(duration), max(duration), count() by bin(timestamp, 1h)
```

## Scaling-Out

Per suggerimenti su piani di esecuzione, timer, batching e pattern con code, consulta `docs/implementation/scaling-out.md`.

## Low Level Design

L’architettura completa (componenti Azure, flussi, sicurezza, CI/CD) è descritta in `docs/implementation/low-level-design.md`.

## CI/CD con Azure DevOps

- La pipeline ufficiale è definita in `azure-pipelines.yml`.
- Configura un Azure Service Connection con permessi sulle Function App dei tre ambienti (`dev`, `test`, `prod`).
- Personalizza le variabili `devFunctionApp`, `testFunctionApp`, `prodFunctionApp` e associa gli ambienti di Azure DevOps per gestire approvazioni/manual gates.

## Limitazioni e Considerazioni

### Limitazioni Salesforce

- **Disponibilità Event Log Files**: 24-48 ore dopo l'evento
- **Rate Limits**: 
  - API Requests: 15.000/giorno (Enterprise)
  - Concurrent Requests: 25 simultanee
- **Polling Interval**: Minimo consigliato 5 minuti per evitare rate limiting

### Limitazioni Log Analytics

- **Payload Size**: Max 30 MB per richiesta
- **API Calls**: 500 richieste/minuto
- **Data Ingestion**: Fino a 6 GB/minuto per workspace

### Ottimizzazioni

- La function invia eventi in batch da 1000 per ottimizzare le chiamate API
- Implementa checkpointing per evitare duplicati (richiede storage persistente)
- Usa retry automatico per gestire errori temporanei

## Troubleshooting

### Errore: "Credenziali Salesforce mancanti"

**Causa**: Variabili d'ambiente non configurate correttamente.

**Soluzione**: Verifica che tutte le variabili `Salesforce__*` siano configurate nella Function App.

### Errore: "401 Unauthorized" da Salesforce

**Causa**: Token OAuth scaduto o credenziali non valide.

**Soluzione**: 
- Verifica Consumer Key/Secret
- Verifica Username/Password
- Verifica Security Token

### Errore: "Nessun Event Log File trovato"

**Causa**: Nessun evento disponibile per il periodo specificato.

**Soluzione**: 
- Event Log Files sono disponibili 24-48 ore dopo l'evento
- Verifica che Event Monitoring sia abilitato in Salesforce
- Verifica i permessi utente per accedere a Event Log Files

### Errore: "Signature non valida" da Log Analytics

**Causa**: Workspace Key errata o algoritmo HMAC non corretto.

**Soluzione**: 
- Verifica Workspace Key
- Verifica che il formato della signature sia corretto

## Sviluppo Locale

### Setup Ambiente

```bash
# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### Test Locale

```bash
# Copia file di configurazione
cp local.settings.json.example local.settings.json

# Modifica local.settings.json con le tue credenziali

# Avvia function localmente
func start
```

### Debug

Usa VS Code con estensione "Azure Functions" per debug locale.

## Prossimi Passi

- [ ] Implementare checkpointing persistente (Azure Table Storage)
- [ ] Aggiungere supporto per più tipi di eventi
- [ ] Implementare enrichment dati (geolocalizzazione IP, ecc.)
- [ ] Aggiungere metriche custom per monitoraggio
- [ ] Implementare dead letter queue per eventi falliti

## Riferimenti

- [Azure Functions Python Documentation](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
- [Salesforce Event Log Files API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_files_api.htm)
- [Log Analytics Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)
- [Azure Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)

## Licenza

Questo progetto fa parte dell'integrazione Salesforce-Sentinel.

