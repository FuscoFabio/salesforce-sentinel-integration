# Implementazione Logic App

Guida completa per implementare l'integrazione Salesforce-Azure Sentinel usando Azure Logic App con Event Log Files API.

## Panoramica

Azure Logic App offre un approccio visuale e low-code per integrare Salesforce con Azure Sentinel, ideale per team che preferiscono configurazione grafica rispetto alla scrittura di codice.

## Architettura

```
Salesforce Event Log Files API
    ↓
Azure Logic App (Timer Trigger)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Prerequisiti

- Azure Subscription
- Azure Logic App
- Log Analytics Workspace con Azure Sentinel
- Credenziali Salesforce (Consumer Key/Secret)
- Workspace ID e Primary Key di Log Analytics
- ⭐ **Raccomandato**: Integration Service Environment (ISE) per connettività privata

## Implementazione

Vedi la guida dettagliata nella sezione Logic App del documento principale.

## Caratteristiche

- Workflow visuale
- Connettori nativi
- Template ARM
- ISE per sicurezza

## Prossimi Passi

- [Configurazione Logic App](../configurations/logic-app.md)
- [Esempio Logic App](../examples/logic-app-example.md)
- [Confronto Soluzioni](../solutions-comparison.md)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Azure Logic Apps Documentation](https://learn.microsoft.com/azure/logic-apps/)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)



