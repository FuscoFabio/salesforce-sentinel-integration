# Configurazione Webhook HTTP

Configurazione per integrare Platform Events con Azure Sentinel usando Webhook HTTP.

## Panoramica

Questa configurazione utilizza HTTP callout da Salesforce per inviare eventi direttamente a un Azure Function con trigger HTTP.

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

## Caratteristiche

- **Setup**: 2-3 giorni
- **Complessità**: Media
- **Scalabilità**: Media
- **Latenza**: < 1 minuto
- **Costi**: Basso-Medio

## Vantaggi

- ✅ Setup relativamente semplice
- ✅ Nessun componente intermedio
- ✅ Controllo diretto
- ✅ Costi contenuti

## Svantaggi

- ❌ Gestione timeout (120s limit Salesforce)
- ❌ Gestione retry manuale
- ❌ Scalabilità limitata
- ❌ Nessuna persistenza eventi

## Quando Usare

- ✅ Proof of concept
- ✅ Volume eventi moderato
- ✅ Budget limitato
- ✅ Setup rapido

## Componenti Richiesti

1. **Salesforce**:
   - Platform Events configurati
   - Apex Trigger
   - HTTP Callout

2. **Azure**:
   - Azure Function (HTTP Trigger)
   - Log Analytics Workspace
   - Azure Sentinel

## Implementazione

Vedi la guida completa: [Implementazione Webhook HTTP](../implementation/webhook-http.md)

## Casi d'Esempio

Vedi esempi pratici: [Esempio Webhook HTTP](../examples/webhook-example.md)

## Confronto con Altre Configurazioni

[Vedi confronto completo →](../configurations-comparison.md)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Azure Functions HTTP Trigger](https://learn.microsoft.com/azure/azure-functions/functions-bindings-http-webhook)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)



