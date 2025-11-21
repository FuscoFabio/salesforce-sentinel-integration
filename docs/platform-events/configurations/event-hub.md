# Configurazione Azure Event Hub

Configurazione per integrare Platform Events con Azure Sentinel usando Azure Event Hub.

## Panoramica

Questa configurazione utilizza Azure Event Hub come buffer intermedio tra Salesforce e Azure Function, offrendo scalabilità e persistenza.

## Architettura

```
Salesforce Platform Event
    ↓
Apex Trigger
    ↓
HTTP Callout
    ↓
Azure Event Hub (Ingestione)
    ↓
Azure Function (Event Hub Trigger)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Caratteristiche

- **Setup**: 3-4 giorni
- **Complessità**: Alta
- **Scalabilità**: Alta
- **Latenza**: < 1 minuto
- **Costi**: Medio-Alto

## Vantaggi

- ✅ Scalabilità automatica
- ✅ Persistenza eventi
- ✅ Affidabilità alta
- ✅ Decoupling Salesforce-Function
- ✅ Throughput elevato

## Svantaggi

- ❌ Componente aggiuntivo (Event Hub)
- ❌ Costi aggiuntivi
- ❌ Setup complesso
- ❌ Più componenti da gestire

## Quando Usare

- ✅ Produzione enterprise
- ✅ Volume eventi elevato
- ✅ Requisiti alta affidabilità
- ✅ Necessità persistenza

## Componenti Richiesti

1. **Salesforce**:
   - Platform Events configurati
   - Apex Trigger
   - HTTP Callout

2. **Azure**:
   - Azure Event Hub
   - Azure Function (Event Hub Trigger)
   - Log Analytics Workspace
   - Azure Sentinel

## Implementazione

Vedi la guida completa: [Implementazione Event Hub](../implementation/event-hub.md)

## Casi d'Esempio

Vedi esempi pratici: [Esempio Event Hub](../examples/event-hub-example.md)

## Confronto con Altre Configurazioni

[Vedi confronto completo →](../configurations-comparison.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)



