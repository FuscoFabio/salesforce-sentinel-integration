# Implementazione CometD Streaming

Guida completa per implementare l'integrazione Platform Events con Azure Sentinel usando CometD Streaming API.

## Panoramica

Questa implementazione utilizza CometD (Bayeux Protocol) su WebSocket per una connessione persistente con Salesforce Platform Events.

## Architettura

```
Salesforce Platform Event
    ↓
CometD Streaming API (WebSocket)
    ↓
Azure Function (Long-Running)
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
- Streaming API abilitata
- Azure Subscription
- Azure Function App (Long-Running/Durable)
- Log Analytics Workspace con Azure Sentinel
- Competenze avanzate sviluppo

## Implementazione Completa

Vedi la guida dettagliata nella sezione "Implementazione: Approccio 2 - CometD Streaming API" del documento principale: [Implementazione Platform Events](../implementation/event-hub.md#implementazione-approccio-2---cometd-streaming-api)

## Componenti Principali

### 1. CometD Client

Client per connessione WebSocket persistente.

### 2. Azure Function (Long-Running)

Function che mantiene connessione WebSocket e processa eventi.

## Limitazioni

- Complessità alta
- Long-running process richiesto
- Gestione reconnessione manuale
- Scalabilità limitata

## Prossimi Passi

- [Configurazione CometD Streaming](../configurations/cometd-streaming.md)
- [Esempio CometD Streaming](../examples/cometd-example.md)
- [Confronto Configurazioni](../configurations-comparison.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Streaming API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)



