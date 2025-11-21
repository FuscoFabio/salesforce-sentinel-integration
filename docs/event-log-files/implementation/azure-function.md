# Implementazione Azure Function

Guida completa per implementare l'integrazione Salesforce-Azure Sentinel usando Azure Function.

## Panoramica

Azure Function permette di creare una soluzione serverless personalizzata per recuperare eventi da Salesforce e inviarli a Azure Sentinel tramite Log Analytics.

## Architettura

```
Salesforce Event Log Files API
    ↓
Azure Function (Timer Trigger)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Prerequisiti

- Azure Subscription
- Azure Function App (Consumption o Premium Plan)
- Log Analytics Workspace con Azure Sentinel
- Credenziali Salesforce (Consumer Key/Secret)
- Workspace ID e Primary Key di Log Analytics
- ⭐ **Raccomandato**: Virtual Network per Private Endpoints (vedi [Gestione Network e Sicurezza](../../implementation/network-sicurezza.md))

## Passo 1: Creare Azure Function App

1. Nel portale Azure, cerca "Function App"
2. Clicca su **Create**
3. Configura:
   - **Subscription**: Seleziona la sottoscrizione
   - **Resource Group**: Crea o seleziona un resource group
   - **Function App name**: Nome univoco
   - **Publish**: Code
   - **Runtime stack**: .NET, Node.js, Python o PowerShell
   - **Version**: Versione più recente
   - **Region**: Seleziona una regione
   - **Plan Type**: 
     - Consumption (per iniziare)
     - Premium (per Private Endpoints e VNet Integration)
4. Clicca su **Review + Create** → **Create**

### ⭐ Configurazione Network (Consigliato)

**Per massima sicurezza, configura Private Endpoints:**

1. **Crea Virtual Network** (se non esiste):
   - Azure Portal → Virtual Networks → Create
   - Name: `vnet-salesforce-integration`
   - Address Space: `10.0.0.0/16`
   - Subnet: `subnet-functions` (10.0.1.0/24)

2. **Configura VNet Integration**:
   - Function App → Networking → VNet integration
   - Seleziona la VNet e subnet create
   - Abilita "Route All" se necessario

3. **Crea Private Endpoint**:
   - Function App → Networking → Private endpoints → Add
   - Connetti alla VNet
   - Configura Azure Private DNS Zone

4. **Configura Salesforce**:
   - Usa l'IP privato del Private Endpoint
   - In Salesforce, imposta **IP Relaxation**: "Relax IP restrictions" (non necessario con Private Endpoint)

**Alternativa - Range IP Pubblici:**
- Vedi [Gestione Network e Sicurezza](../../implementation/network-sicurezza.md) per configurare range IP pubblici
- Richiede manutenzione periodica (range IP cambiano settimanalmente)

## Passo 2: Configurare Application Settings

Nella Function App, vai a **Configuration** → **Application settings** e aggiungi:

```
Salesforce__ConsumerKey=<your-consumer-key>
Salesforce__ConsumerSecret=<your-consumer-secret>
Salesforce__Username=<salesforce-username>
Salesforce__Password=<salesforce-password>
Salesforce__SecurityToken=<security-token>
LogAnalytics__WorkspaceId=<workspace-id>
LogAnalytics__WorkspaceKey=<workspace-key>
```

**Nota**: Per sicurezza, usa **Key Vault References** invece di valori in chiaro.

## Passo 3: Implementare la Function

### Timer Trigger Function

Crea una Function con Timer Trigger che esegue periodicamente (es. ogni 15 minuti):

```csharp
[FunctionName("SalesforceToSentinel")]
public static async Task Run(
    [TimerTrigger("0 */15 * * * *")] TimerInfo myTimer,
    ILogger log)
{
    // Recupera eventi da Salesforce
    // Trasforma i dati
    // Invia a Log Analytics
}
```

### Logica di Recupero Eventi

1. Autenticazione OAuth con Salesforce
2. Recupero Event Log Files tramite API
3. Filtraggio eventi già processati (usando timestamp)
4. Trasformazione dati in formato Log Analytics

### Invio a Log Analytics

Usa l'API Data Collector di Log Analytics per inviare i dati:

```csharp
var json = JsonConvert.SerializeObject(logEntries);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var signature = BuildSignature(json, workspaceKey);
client.DefaultRequestHeaders.Add("Log-Type", "Salesforce_CL");
client.DefaultRequestHeaders.Add("x-ms-date", DateTime.UtcNow.ToString("r"));
client.DefaultRequestHeaders.Add("Authorization", signature);
await client.PostAsync(workspaceUrl, content);
```

## Passo 4: Gestione Errori e Retry

Implementa:
- **Retry Logic**: Per errori temporanei
- **Dead Letter Queue**: Per eventi non processabili
- **Logging**: Per monitoraggio e troubleshooting
- **Checkpointing**: Per tracciare eventi già processati

## Passo 5: Monitoraggio

Configura:
- **Application Insights**: Per metriche e log
- **Alert**: Per errori e problemi
- **Dashboard**: Per visualizzare lo stato dell'integrazione

## Esempio di Schema Dati

```json
{
  "TimeGenerated": "2024-01-15T10:30:00Z",
  "EventType": "LoginEvent",
  "UserName": "user@example.com",
  "SourceIP": "192.168.1.1",
  "Browser": "Chrome",
  "Platform": "Windows",
  "LoginType": "Web",
  "Success": true
}
```

## Ottimizzazioni

- **Batch Processing**: Raggruppa più eventi in una singola chiamata
- **Parallel Processing**: Processa più eventi in parallelo
- **Caching**: Cache token OAuth per ridurre chiamate
- **Cost Optimization**: Usa Consumption Plan per costi ottimali

## Limitazioni e Polling

### Timer Trigger (Azure Function)

- **Intervallo minimo supportato**: 1 minuto (`0 */1 * * * *`) su Consumption e Premium Plan  
- **Intervalli inferiori al minuto**: Richiedono App Service Plan dedicato con `TimerTrigger` in modalità Continuous (sconsigliato per Salesforce)  
- **Intervallo massimo consigliato**: 60 minuti (per evitare ingestione massiva di backlog)  
- **Accuratezza**: Il timer non garantisce esecuzione al millisecondo; può avere ritardi di 1-2 minuti

### Strategia di Polling per Salesforce

- **Intervallo consigliato**: 5-15 minuti (allinea latenza e consumo API)  
- **Intervallo minimo raccomandato**: 5 minuti per evitare rate limiting  
- **Intervallo massimo raccomandato**: 30 minuti se il volume di eventi è moderato

### Calcolo dell'Intervallo Ottimale

```
Intervallo (min) = (Eventi_giornalieri / Eventi_per_poll) × (1440 / Richieste_API_disponibili)
```

**Esempio**:
- Eventi giornalieri: 40.000  
- Eventi elaborati per poll: 8.000  
- Limite API disponibile: 15.000 richieste/24h

```
Intervallo = (40.000 / 8.000) × (1440 / 15.000) = 0,48 minuti
```

In questo scenario:
- Usa l'intervallo minimo di **5 minuti** (limite pratico consigliato)  
- Abilita filtri sugli eventi non necessari  
- Valuta l'uso di una Function dedicata in Premium Plan

### Limiti Salesforce da Considerare

- **API Requests** (24h rolling):  
  - Enterprise: ~15.000  
  - Unlimited: ~100.000  
  - Performance: ~50.000  
- **Request simultanee**: 25  
- **Disponibilità Event Log Files**: 24-48 ore dopo l'evento

### Suggerimenti Operativi

1. **Logica di checkpoint**: salva l'ultimo `LogDate` processato per evitare duplicati  
2. **Backoff esponenziale**: in caso di `HTTP 429` o `REQUEST_LIMIT_EXCEEDED` aumenta temporaneamente l'intervallo  
3. **Monitoraggio**: usa Application Insights per verificare la durata effettiva del timer  
4. **Alert**: crea alert se la Function non gira entro l'intervallo previsto (heart-beat)

## Troubleshooting

- **Errori di autenticazione**: Verifica credenziali e token
- **Nessun dato**: Controlla timer trigger e log
- **Errori API**: Verifica rate limits e retry logic
- **Costi elevati**: Ottimizza frequenza esecuzione e batch size

## Link Utili

- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Log Analytics Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)
- [Salesforce Event Log Files API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_files_api.htm)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

