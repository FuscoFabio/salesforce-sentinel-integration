# Implementazione Webhook HTTP

Guida completa per implementare l'integrazione Platform Events con Azure Sentinel usando Webhook HTTP.

## Panoramica

Questa implementazione utilizza HTTP callout da Salesforce per inviare eventi direttamente a un Azure Function con trigger HTTP.

## Architettura

```
Salesforce Platform Event
    ↓
Apex Trigger
    ↓
HTTP Callout
    ↓
Azure Function (HTTP Trigger)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Prerequisiti

- Licenza Salesforce Enterprise, Unlimited o Performance Edition
- Platform Events abilitato in Salesforce
- Azure Subscription
- Azure Function App
- Log Analytics Workspace con Azure Sentinel
- Competenze sviluppo Apex e Azure Function

## Implementazione Completa

Vedi la guida dettagliata nella sezione "Implementazione: Approccio 1 - Webhook da Salesforce" del documento principale: [Implementazione Platform Events](../implementation/event-hub.md#implementazione-approccio-1---webhook-da-salesforce)

## Componenti Principali

### 1. Salesforce Apex Trigger

Trigger per intercettare eventi e inviarli via HTTP.

### 2. Azure Function (HTTP Trigger)

Function che riceve eventi e li invia a Log Analytics.

## Limitazioni

- Timeout callout Salesforce: 120 secondi
- Gestione retry manuale
- Nessuna persistenza eventi
- Scalabilità limitata

## Prossimi Passi

- [Configurazione Webhook HTTP](../configurations/webhook-http.md)
- [Esempio Webhook HTTP](../examples/webhook-example.md)
- [Confronto Configurazioni](../configurations-comparison.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Functions HTTP Trigger](https://learn.microsoft.com/azure/azure-functions/functions-bindings-http-webhook)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)



