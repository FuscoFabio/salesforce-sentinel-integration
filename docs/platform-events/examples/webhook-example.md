# Caso d'Esempio: Webhook HTTP

Esempio completo di implementazione Webhook HTTP per integrazione Platform Events con Azure Sentinel.

## Scenario

Un'organizzazione ha bisogno di monitoraggio near real-time per eventi critici:
- LoginEvent in tempo reale
- Alert immediati per accessi sospetti
- Volume eventi moderato

## Requisiti

- Licenza Salesforce Enterprise
- Azure Subscription
- Azure Function App
- Competenze sviluppo Apex e Azure
- Tempo setup: 2-3 giorni

## Implementazione Completa

Vedi la guida dettagliata: [Implementazione Webhook HTTP](../implementation/webhook-http.md)

## Caratteristiche

- Latenza < 1 minuto
- Setup relativamente semplice
- Costi contenuti
- Nessun componente intermedio

## Risultati Attesi

- Eventi disponibili in Azure Sentinel in < 1 minuto
- Alert real-time per eventi critici
- Monitoraggio continuo

## Prossimi Passi

- [Implementazione Webhook HTTP](../implementation/webhook-http.md)
- [Configurazione Webhook HTTP](../configurations/webhook-http.md)
- [Query KQL](../../implementation/kql-queries.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Functions HTTP Trigger](https://learn.microsoft.com/azure/azure-functions/functions-bindings-http-webhook)



