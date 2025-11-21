# Caso d'Esempio: CCF

Esempio completo di implementazione CCF per integrazione Salesforce-Azure Sentinel.

## Scenario

Un'organizzazione vuole monitorare tutti gli accessi a Salesforce per:
- Rilevare accessi sospetti
- Tracciare accessi da IP non usuali
- Monitorare attività fuori orario
- Generare alert per tentativi di login falliti

## Requisiti

- Licenza Salesforce Enterprise
- Azure Subscription
- Azure Sentinel Workspace
- Tempo setup: 30-60 minuti

## Implementazione Completa

Vedi la guida dettagliata: [Implementazione CCF](../implementation/ccf.md)

## Risultati Attesi

- Eventi disponibili in Azure Sentinel dopo 24-48 ore
- Query KQL per analisi eventi
- Alert configurati per eventi sospetti
- Dashboard per monitoraggio

## Query KQL di Esempio

```kql
// Accessi da IP non usuali
Salesforce_CL
| where EventType_s == "LoginEvent"
| summarize count() by ClientIP_s, UserName_s
| where count_ > 10
```

## Prossimi Passi

- [Implementazione CCF](../implementation/ccf.md)
- [Configurazione CCF](../configurations/ccf.md)
- [Query KQL](../../implementation/kql-queries.md)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [CodeLess Connector Framework (Microsoft Sentinel)](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)



