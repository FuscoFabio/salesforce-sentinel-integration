# Azure Logic App (Event Log Files)

Soluzione low-code basata su Azure Logic App per l'integrazione Salesforce-Azure Sentinel usando **Event Log Files API**.

## Panoramica

Azure Logic App offre un approccio visuale e low-code per integrare Salesforce con Azure Sentinel, ideale per team che preferiscono configurazione grafica rispetto alla scrittura di codice.

## ⚠️ Approccio: Event Log Files API

**Questa soluzione usa Event Log Files API**, che ha le seguenti caratteristiche:

- ✅ **Copertura Completa**: Tutti gli eventi disponibili (LoginEvent, LogoutEvent, ApiEvent, Audit Trail)
- ✅ **Formato Strutturato**: Dati ottimizzati e validati
- ❌ **Incrementi orari**: I log vengono generati ogni ora e messi a disposizione solo dopo la pubblicazione del blocco (vedi [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm))
- ❌ **Latenza**: 24-48 ore (limite strutturale Salesforce: nessun connettore può anticipare la disponibilità dei file)
- ✅ **Setup Semplice**: Approccio low-code visuale

**Se hai bisogno di near real-time (< 24 ore)**, considera [Platform Events](../../platform-events/overview.md) invece.

## Caratteristiche

- **Low-Code**: Configurazione visuale tramite designer
- **Template ARM**: Deployment rapido con template predefiniti
- **Connettori Integrati**: Connettori nativi per Salesforce e Azure Sentinel
- **Workflow Visuale**: Design del flusso di lavoro tramite interfaccia grafica

## Prerequisiti

- Azure Subscription
- Azure Logic App
- Azure Sentinel Workspace
- Configurazione Salesforce completata
- ⭐ **Raccomandato**: Integration Service Environment (ISE) per connettività privata

## Network e Sicurezza

### ⭐ Approccio Consigliato: Integration Service Environment (ISE)

Per massima sicurezza e connettività privata:

1. **Crea Integration Service Environment**:
   - Azure Portal → Logic Apps → Integration Service Environments → Create
   - Name: `ise-salesforce-integration`
   - Location: Seleziona regione
   - Network: Crea nuova VNet o usa esistente

2. **Vantaggi ISE**:
   - IP privati dedicati e statici
   - Connettività privata nativa
   - Nessuna manutenzione di range IP
   - Maggiore sicurezza e compliance

3. **Configura Salesforce**:
   - Usa gli IP privati dell'ISE
   - In Salesforce, imposta **IP Relaxation**: "Relax IP restrictions" (non necessario con ISE)

**Alternativa - Range IP Pubblici:**
- Vedi [Gestione Network e Sicurezza](../../implementation/network-sicurezza.md) per configurare range IP pubblici
- Richiede manutenzione periodica

## Deployment

Il progetto include template ARM per il deployment rapido della Logic App.

## Link Utili

- [Documentazione Azure Logic Apps](https://learn.microsoft.com/azure/logic-apps/)
- [Logic Apps Connectors](https://learn.microsoft.com/azure/connectors/apis-list)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Azure Logic Apps Documentation](https://learn.microsoft.com/azure/logic-apps/)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

