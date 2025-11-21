# Architettura

Panoramica dell'architettura dell'integrazione Salesforce-Azure Sentinel.

## Architettura Generale

L'integrazione segue un pattern di raccolta eventi da Salesforce e invio a Azure Sentinel per l'analisi e il monitoraggio della sicurezza.

## Componenti Principali

### Salesforce

- **Event Monitoring**: Genera eventi di accesso (LoginEvent, LogoutEvent, ApiEvent)
- **Connected App**: Autenticazione OAuth per l'accesso alle API
- **Event Log Files API**: API per recuperare i log degli eventi

### Layer di Integrazione

Il layer di integrazione varia in base alla soluzione scelta:

- **CCF**: Connector nativo Azure Sentinel
- **Azure Function**: Funzione serverless per trasformazione e invio
- **Logic App**: Workflow orchestrato per la gestione degli eventi
- **Syslog**: Server Syslog per la raccolta centralizzata

### Azure Sentinel

- **Log Analytics Workspace**: Storage dei log
- **KQL Queries**: Analisi e query sui dati
- **Workbooks**: Dashboard e visualizzazioni
- **Alerting**: Regole di allerta per eventi sospetti

## Flusso dei Dati

```
Salesforce Event Monitoring
    ↓
Event Log Files API
    ↓
Layer di Integrazione (CCF/Function/Logic App)
    ↓
Azure Sentinel / Log Analytics
    ↓
Analisi e Monitoraggio
```

## Pattern di Integrazione

### Pattern Push Real-Time (Platform Events)

Salesforce Platform Events → Streaming API/Webhook → Azure Function/Event Hub → Azure Sentinel

**Caratteristiche**:
- Latenza: < 1 minuto (near real-time)
- Copertura: Limitata (non tutti gli eventi disponibili)
- Complessità: Alta (richiede sviluppo)

### Pattern Push (CCF, Function, Logic App)

Salesforce → API Call → Integrazione → Azure Sentinel

**Caratteristiche**:
- Latenza: 24-72 ore (limite strutturale Event Log Files)
- Copertura: Completa
- Complessità: Bassa (CCF) o Media (Function)

### Pattern Pull (Function, Logic App)

Integrazione → Polling API Salesforce → Trasformazione → Azure Sentinel

**Caratteristiche**:
- Latenza: 24-72 ore + intervallo polling
- Copertura: Completa
- Complessità: Media

### Pattern Syslog

Salesforce → Syslog Server → Azure Monitor Agent → Azure Sentinel

**Caratteristiche**:
- Latenza: Dipende da configurazione
- Copertura: Dipende da configurazione Salesforce
- Complessità: Media

## Considerazioni di Sicurezza

- **Autenticazione OAuth**: Sicurezza delle credenziali
- **HTTPS**: Comunicazione criptata
- **Network Security**: Restrizioni IP e firewall
- **Secrets Management**: Gestione sicura delle credenziali (Key Vault)

## Scalabilità

- **Eventi Volume**: Gestione di picchi di eventi
- **Retry Logic**: Gestione errori e retry
- **Rate Limiting**: Rispetto dei limiti API Salesforce
- **Cost Optimization**: Ottimizzazione dei costi Azure

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

