# Implementazione Platform Events (Event Bus) - Near Real-Time

Guida completa per implementare l'integrazione Salesforce-Azure Sentinel usando Platform Events (Event Bus) per ottenere monitoraggio near real-time.

## Panoramica

I **Platform Events** (Event Bus) di Salesforce permettono di ottenere eventi in **tempo reale** (< 1 minuto di latenza) invece dei 24-48 ore degli Event Log Files. Questa soluzione è ideale quando è necessario monitoraggio near real-time.

## ⚠️ Limitazioni Importanti

Prima di procedere, è fondamentale comprendere le limitazioni:

### Copertura Eventi

**Eventi Disponibili su Platform Events**:
- ✅ **LoginEvent**: Accessi utente (se configurato)
- ✅ **LogoutEvent**: Disconnessioni (se configurato)
- ✅ **ApiEvent**: Chiamate API (se configurato)
- ✅ Eventi custom definiti dall'organizzazione

**Eventi NON Disponibili su Platform Events**:
- ❌ **Audit Trail**: Azioni amministrative (solo su Event Log Files)
- ❌ **Field History Tracking**: Modifiche ai campi (solo su Event Log Files)
- ❌ Alcuni eventi di sicurezza avanzati

**Implicazione**: Se hai bisogno di **tutti** gli eventi, potrebbe essere necessario un approccio **ibrido** (Platform Events + Event Log Files).

### Requisiti Tecnici

- **Sviluppo Custom**: Richiede sviluppo di codice (Apex, Azure Function)
- **Manutenzione**: Gestione continua del codice e delle configurazioni
- **Complessità**: Maggiore complessità rispetto a Event Log Files API
- **Costi**: Costi di sviluppo e manutenzione

## Architettura

```
Salesforce Platform Events (Event Bus)
    ↓
Apex Trigger / Process Builder
    ↓
CometD Streaming API (WebSocket)
    ↓
Azure Function (Event Hub Trigger o HTTP Trigger)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Componenti dell'Architettura

### 1. Salesforce Platform Events

**Cosa sono**: Eventi pubblicati in tempo reale su un bus eventi interno di Salesforce.

**Caratteristiche**:
- Eventi disponibili in tempo reale (< 1 secondo)
- Accessibili tramite Streaming API (CometD)
- Supporto per eventi standard e custom

### 2. Streaming API (CometD)

**Protocollo**: CometD (Bayeux Protocol) su WebSocket

**Funzionamento**:
- Connessione persistente WebSocket
- Push di eventi in tempo reale
- Sottoscrizione a canali specifici (channels)

### 3. Azure Function

**Trigger Options**:
- **HTTP Trigger**: Salesforce chiama Function via webhook
- **Event Hub Trigger**: Eventi via Azure Event Hub
- **Timer Trigger**: Polling CometD (meno efficiente)

## Implementazione: Approccio 1 - Webhook da Salesforce

### Architettura

```
Salesforce Platform Event
    ↓
Apex Trigger
    ↓
Callout HTTP → Azure Function (HTTP Trigger)
    ↓
Log Analytics
    ↓
Azure Sentinel
```

### Passo 1: Configurare Platform Events in Salesforce

#### 1.1 Abilitare Platform Events

1. Vai a **Setup** → **Platform Events**
2. Verifica che Platform Events sia abilitato
3. Se necessario, abilita "Enable Platform Events"

#### 1.2 Creare Platform Event Custom (se necessario)

1. Vai a **Setup** → **Platform Events** → **New Platform Event**
2. Crea un Platform Event per gli eventi di sicurezza:
   ```
   API Name: Security_Event__e
   Label: Security Event
   ```
3. Aggiungi campi necessari:
   - `EventType__c` (Text)
   - `UserName__c` (Text)
   - `SourceIP__c` (Text)
   - `Timestamp__c` (DateTime)
   - `EventData__c` (Long Text Area) - JSON

### Passo 2: Creare Apex Trigger per Pubblicare Eventi

#### 2.1 Trigger per LoginEvent

```apex
trigger LoginEventTrigger on EventBusSubscriber (after insert) {
    List<Security_Event__e> events = new List<Security_Event__e>();
    
    for (EventBusSubscriber ebs : Trigger.new) {
        if (ebs.Type == 'LoginEvent') {
            Security_Event__e event = new Security_Event__e();
            event.EventType__c = 'LoginEvent';
            event.UserName__c = ebs.UserId;
            event.SourceIP__c = ebs.SourceIp;
            event.Timestamp__c = DateTime.now();
            event.EventData__c = JSON.serialize(ebs);
            events.add(event);
        }
    }
    
    if (!events.isEmpty()) {
        List<Database.SaveResult> results = EventBus.publish(events);
    }
}
```

#### 2.2 Apex Class per Callout HTTP

```apex
public class AzureSentinelIntegration {
    private static final String FUNCTION_URL = 'https://your-function.azurewebsites.net/api/SalesforceEvent';
    
    @future(callout=true)
    public static void sendToAzureSentinel(String eventData) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(FUNCTION_URL);
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(eventData);
        req.setTimeout(12000);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() != 200) {
            // Log error
            System.debug('Error: ' + res.getStatusCode() + ' - ' + res.getBody());
        }
    }
}
```

#### 2.3 Trigger per Invio a Azure Function

```apex
trigger SecurityEventTrigger on Security_Event__e (after insert) {
    for (Security_Event__e event : Trigger.new) {
        String eventJson = JSON.serialize(event);
        AzureSentinelIntegration.sendToAzureSentinel(eventJson);
    }
}
```

### Passo 3: Configurare Azure Function (HTTP Trigger)

#### 3.1 Creare Function App

1. Crea Azure Function App (vedi [Implementazione Webhook HTTP](../implementation/webhook-http.md) per dettagli su Azure Function)
2. Crea una Function con **HTTP Trigger**

#### 3.2 Implementare Function

```csharp
[FunctionName("SalesforceEvent")]
public static async Task<IActionResult> Run(
    [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
    ILogger log)
{
    try {
        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        var salesforceEvent = JsonConvert.DeserializeObject<SalesforceEvent>(requestBody);
        
        // Trasforma evento
        var logEntry = new {
            TimeGenerated = DateTime.UtcNow,
            EventType = salesforceEvent.EventType__c,
            UserName = salesforceEvent.UserName__c,
            SourceIP = salesforceEvent.SourceIP__c,
            Timestamp = salesforceEvent.Timestamp__c,
            EventData = salesforceEvent.EventData__c
        };
        
        // Invia a Log Analytics
        await SendToLogAnalytics(new[] { logEntry });
        
        return new OkResult();
    }
    catch (Exception ex) {
        log.LogError(ex, "Error processing Salesforce event");
        return new StatusCodeResult(500);
    }
}
```

## Implementazione: Approccio 2 - CometD Streaming API

### Architettura

```
Salesforce Platform Events
    ↓
CometD Streaming API (WebSocket)
    ↓
Azure Function (Long-running process)
    ↓
Log Analytics
    ↓
Azure Sentinel
```

### Passo 1: Configurare Azure Function per CometD

#### 1.1 Function con Timer Trigger (Polling CometD)

```csharp
[FunctionName("SalesforceCometDListener")]
public static async Task Run(
    [TimerTrigger("0 */1 * * * *")] TimerInfo myTimer,
    ILogger log)
{
    // Connessione CometD
    var cometDClient = new CometDClient();
    await cometDClient.Connect(salesforceUrl, accessToken);
    
    // Sottoscrivi a canale
    await cometDClient.Subscribe("/event/Security_Event__e", (message) => {
        // Processa evento
        ProcessEvent(message);
    });
    
    // Mantieni connessione attiva
    await Task.Delay(TimeSpan.FromMinutes(5));
    await cometDClient.Disconnect();
}
```

#### 1.2 Libreria CometD per .NET

```bash
dotnet add package CometD.NetCore
```

### Passo 2: Autenticazione Salesforce per Streaming API

```csharp
public class SalesforceAuth {
    public async Task<string> GetAccessToken() {
        var client = new HttpClient();
        var content = new FormUrlEncodedContent(new[] {
            new KeyValuePair<string, string>("grant_type", "password"),
            new KeyValuePair<string, string>("client_id", consumerKey),
            new KeyValuePair<string, string>("client_secret", consumerSecret),
            new KeyValuePair<string, string>("username", username),
            new KeyValuePair<string, string>("password", password + securityToken)
        });
        
        var response = await client.PostAsync(
            "https://login.salesforce.com/services/oauth2/token", 
            content);
        
        var result = await response.Content.ReadAsStringAsync();
        var token = JsonConvert.DeserializeObject<OAuthToken>(result);
        return token.access_token;
    }
}
```

## Implementazione: Approccio 3 - Azure Event Hub (Consigliato)

### Architettura

```
Salesforce Platform Events
    ↓
Apex Trigger → HTTP Callout
    ↓
Azure Event Hub
    ↓
Azure Function (Event Hub Trigger)
    ↓
Log Analytics
    ↓
Azure Sentinel
```

### Vantaggi Event Hub

- **Scalabilità**: Gestione automatica di picchi di eventi
- **Affidabilità**: Persistenza eventi, retry automatico
- **Performance**: Throughput elevato
- **Decoupling**: Disaccoppiamento tra Salesforce e Function

### Passo 1: Creare Azure Event Hub

1. Azure Portal → **Event Hubs** → **Create**
2. Configura:
   - **Namespace**: `salesforce-events-ns`
   - **Event Hub**: `salesforce-security-events`
   - **Partition Count**: 4-8 (per scalabilità)
   - **Message Retention**: 1-7 giorni

### Passo 2: Modificare Apex per Event Hub

```apex
public class AzureEventHubIntegration {
    private static final String EVENT_HUB_URL = 'https://salesforce-events-ns.servicebus.windows.net/salesforce-security-events/messages';
    private static final String SAS_TOKEN = 'SharedAccessSignature ...';
    
    @future(callout=true)
    public static void sendToEventHub(String eventData) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(EVENT_HUB_URL + '?timeout=60&api-version=2014-01');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/atom+xml;type=entry;charset=utf-8');
        req.setHeader('Authorization', SAS_TOKEN);
        req.setBody(eventData);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
    }
}
```

### Passo 3: Azure Function con Event Hub Trigger

```csharp
[FunctionName("ProcessSalesforceEvents")]
public static async Task Run(
    [EventHubTrigger("salesforce-security-events", Connection = "EventHubConnection")] 
    EventData[] events,
    ILogger log)
{
    var logEntries = new List<object>();
    
    foreach (EventData eventData in events) {
        var salesforceEvent = JsonConvert.DeserializeObject<SalesforceEvent>(
            Encoding.UTF8.GetString(eventData.Body.Array));
        
        logEntries.Add(new {
            TimeGenerated = DateTime.UtcNow,
            EventType = salesforceEvent.EventType__c,
            UserName = salesforceEvent.UserName__c,
            SourceIP = salesforceEvent.SourceIP__c
        });
    }
    
    // Invia batch a Log Analytics
    await SendToLogAnalytics(logEntries);
}
```

## Configurazione Network e Sicurezza

### Opzione 1: Webhook HTTP (Approccio 1)

**Configurazione Salesforce**:
- Aggiungi IP/URL Azure Function in **Remote Site Settings**
- Configura **Callout Limits** se necessario

**Configurazione Azure Function**:
- Usa **Private Endpoints** per sicurezza (vedi [Network e Sicurezza](../../implementation/network-sicurezza.md))
- Configura **IP Restrictions** se necessario
- Usa **HTTPS** obbligatorio

### Opzione 2: Event Hub (Approccio 3)

**Configurazione Event Hub**:
- **Shared Access Policy** con permessi Send
- **SAS Token** per autenticazione da Salesforce
- **Private Endpoints** per sicurezza (consigliato)

## Limitazioni e Considerazioni

### Limitazioni Platform Events

1. **Copertura Eventi**:
   - Non tutti gli eventi sono disponibili
   - Audit Trail non disponibile
   - Alcuni eventi richiedono configurazione custom

2. **Rate Limits**:
   - **Platform Events pubblicati**: 2.000.000/giorno (Enterprise)
   - **API Callouts**: 100.000/giorno (Enterprise)
   - **Concurrent Callouts**: 10 simultanee

3. **Complessità**:
   - Richiede sviluppo Apex
   - Gestione errori e retry
   - Monitoraggio connessioni

### Considerazioni Operative

1. **Affidabilità**:
   - Gestire timeout e retry
   - Dead letter queue per eventi falliti
   - Monitoring e alerting

2. **Costi**:
   - Costi Azure Function (esecuzioni)
   - Costi Event Hub (se usato)
   - Costi Log Analytics (ingestione)

3. **Manutenzione**:
   - Aggiornamenti codice Apex
   - Gestione credenziali
   - Monitoraggio performance

## Confronto: Platform Events vs Event Log Files

| Aspetto | Platform Events | Event Log Files |
|---------|----------------|-----------------|
| **Latenza** | < 1 minuto | 24-48 ore |
| **Copertura** | Limitata | Completa |
| **Setup** | Complesso (sviluppo) | Semplice (CCF) |
| **Manutenzione** | Alta | Zero (CCF) |
| **Costi** | Sviluppo + Azure | Solo Azure |
| **Affidabilità** | Richiede gestione | Gestita (CCF) |
| **Audit Trail** | ❌ Non disponibile | ✅ Disponibile |

## Raccomandazione: Approccio Ibrido

Per massimizzare copertura e latenza, considera un **approccio ibrido**:

1. **Platform Events** per eventi critici in tempo reale:
   - LoginEvent
   - LogoutEvent
   - Eventi custom critici

2. **Event Log Files API** (CCF) per:
   - Audit Trail
   - Eventi storici completi
   - Backup e compliance

### Architettura Ibrida

```
Salesforce
    ↓
    ├─→ Platform Events → Event Hub → Function → Sentinel (Real-time)
    └─→ Event Log Files → CCF → Sentinel (24-48h, completo)
```

## Best Practices

1. **Filtraggio Eventi**: Pubblica solo eventi critici su Platform Events
2. **Batch Processing**: Raggruppa eventi prima di inviare a Log Analytics
3. **Error Handling**: Implementa retry con exponential backoff
4. **Monitoring**: Monitora connessioni, errori, latenza
5. **Testing**: Testa in ambiente sandbox prima di produzione
6. **Documentation**: Documenta trigger Apex e configurazioni

## Troubleshooting

### Problema: Eventi Non Ricevuti

**Possibili Cause**:
- Trigger Apex non attivo
- Callout limits raggiunti
- Timeout connessione
- Errori in Azure Function

**Soluzione**:
1. Verifica trigger Apex in Setup → Apex Triggers
2. Controlla Debug Logs in Salesforce
3. Verifica log Azure Function
4. Controlla Remote Site Settings

### Problema: Latenza Elevata

**Possibili Cause**:
- Callout timeout
- Function cold start
- Event Hub throttling

**Soluzione**:
1. Aumenta timeout callout (max 120 secondi)
2. Usa Premium Plan per Function (no cold start)
3. Aumenta throughput Event Hub

## Link Utili

## Fonti

- [Salesforce Platform Events Documentation](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Streaming API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/)
- [Azure Event Hubs](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Functions HTTP Trigger](https://learn.microsoft.com/azure/azure-functions/functions-bindings-http-webhook)
- [Implementazione Webhook HTTP](../implementation/webhook-http.md)
- [Network e Sicurezza](../../implementation/network-sicurezza.md)

---

**Nota**: Questo approccio richiede competenze di sviluppo Apex e Azure Function. Se non hai questi requisiti, considera l'approccio Event Log Files con CCF.

