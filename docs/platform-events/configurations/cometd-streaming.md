# Configurazione CometD Streaming

Configurazione per integrare Platform Events con Azure Sentinel usando CometD Streaming API.

## Panoramica

Questa configurazione utilizza CometD (Bayeux Protocol) su WebSocket per una connessione persistente con Salesforce Platform Events.

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

## Caratteristiche

- **Setup**: 3-5 giorni
- **Complessità**: Molto Alta
- **Scalabilità**: Media-Alta
- **Latenza**: < 1 minuto
- **Costi**: Medio

## Vantaggi

- ✅ Connessione persistente
- ✅ Push real-time
- ✅ Efficienza (no overhead HTTP)

## Svantaggi

- ❌ Complessità alta
- ❌ Long-running process
- ❌ Gestione reconnessione manuale
- ❌ Scalabilità limitata

## Quando Usare

- ✅ Connessioni persistenti necessarie
- ✅ Volume eventi continuo
- ✅ Competenze avanzate disponibili

## Componenti Richiesti

1. **Salesforce**:
   - Platform Events configurati
   - Streaming API abilitata

2. **Azure**:
   - Azure Function (Long-Running/Durable)
   - Log Analytics Workspace
   - Azure Sentinel

## Implementazione

Vedi la guida completa: [Implementazione CometD Streaming](../implementation/cometd-streaming.md)

## Casi d'Esempio

Vedi esempi pratici: [Esempio CometD](../examples/cometd-example.md)

## Confronto con Altre Configurazioni

[Vedi confronto completo →](../configurations-comparison.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Streaming API (CometD)](https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)



