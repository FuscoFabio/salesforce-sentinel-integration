# Confronto Configurazioni Platform Events

Confronto dettagliato di tutte le configurazioni disponibili per integrare Platform Events (Event Bus) con Azure Sentinel.

## Panoramica Configurazioni

Tre configurazioni principali sono disponibili per integrare Platform Events:

1. **Webhook HTTP** ⭐ Più Semplice
2. **Azure Event Hub** ⭐ Consigliato
3. **CometD Streaming**

## Tabella Confronto Completa

| Aspetto | Webhook HTTP | Azure Event Hub | CometD Streaming |
|---------|--------------|-----------------|------------------|
| **Setup Time** | 2-3 giorni | 3-4 giorni | 3-5 giorni |
| **Complessità** | Media | Alta | Molto Alta |
| **Scalabilità** | Media | Alta | Media-Alta |
| **Affidabilità** | Media | Alta | Media |
| **Latenza** | < 1 minuto | < 1 minuto | < 1 minuto |
| **Persistenza** | ❌ No | ✅ Sì | ❌ No |
| **Gestione Picchi** | Manuale | Automatica | Manuale |
| **Costi** | Basso-Medio | Medio-Alto | Medio |
| **Manutenzione** | Media | Media-Alta | Alta |
| **Best For** | Setup rapido | Produzione | Connessioni persistenti |

## Dettaglio Configurazioni

### 1. Webhook HTTP ⭐ Più Semplice

**Architettura**:
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

#### Vantaggi

- ✅ **Setup Relativamente Semplice**: Nessun componente intermedio
- ✅ **Controllo Diretto**: Comunicazione diretta Salesforce → Azure
- ✅ **Costi Contenuti**: Nessun componente aggiuntivo
- ✅ **Debug Semplice**: Facile tracciamento richieste HTTP

#### Svantaggi

- ❌ **Gestione Timeout**: Limitato da timeout callout Salesforce (120s)
- ❌ **Gestione Retry**: Implementazione manuale
- ❌ **Scalabilità Limitata**: Gestione picchi manuale
- ❌ **Nessuna Persistenza**: Eventi persi se Function non disponibile

#### Quando Usare

- ✅ Setup rapido per proof of concept
- ✅ Volume eventi moderato
- ✅ Budget limitato
- ✅ Nessun requisito di persistenza

#### Quando NON Usare

- ❌ Volume eventi elevato
- ❌ Requisiti di alta affidabilità
- ❌ Necessità di persistenza eventi
- ❌ Gestione automatica picchi

[Vedi Configurazione →](configurations/webhook-http.md) | [Vedi Implementazione →](implementation/webhook-http.md) | [Vedi Esempio →](examples/webhook-example.md)

---

### 2. Azure Event Hub ⭐ Consigliato

**Architettura**:
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

#### Vantaggi

- ✅ **Scalabilità Automatica**: Gestione automatica picchi
- ✅ **Persistenza**: Eventi salvati anche se Function non disponibile
- ✅ **Affidabilità**: Retry automatico e gestione errori
- ✅ **Decoupling**: Salesforce disaccoppiato da Function
- ✅ **Throughput Elevato**: Supporta milioni di eventi/secondo

#### Svantaggi

- ❌ **Componente Aggiuntivo**: Event Hub richiesto
- ❌ **Costi Aggiuntivi**: Costi Event Hub (~$10-20/mese base)
- ❌ **Setup Complesso**: Configurazione Event Hub + Function
- ❌ **Complessità**: Più componenti da gestire

#### Quando Usare

- ✅ Produzione enterprise
- ✅ Volume eventi elevato
- ✅ Requisiti di alta affidabilità
- ✅ Necessità di persistenza
- ✅ Gestione automatica picchi

#### Quando NON Usare

- ❌ Proof of concept
- ❌ Volume eventi molto basso
- ❌ Budget limitato
- ❌ Setup semplice richiesto

[Vedi Configurazione →](configurations/event-hub.md) | [Vedi Implementazione →](implementation/event-hub.md) | [Vedi Esempio →](examples/event-hub-example.md)

---

### 3. CometD Streaming

**Architettura**:
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

#### Vantaggi

- ✅ **Connessione Persistente**: WebSocket long-running
- ✅ **Push Real-Time**: Eventi inviati immediatamente
- ✅ **Efficienza**: Nessun overhead HTTP per ogni evento

#### Svantaggi

- ❌ **Complessità Alta**: Gestione WebSocket complessa
- ❌ **Long-Running Process**: Richiede processo sempre attivo
- ❌ **Gestione Reconnessione**: Implementazione manuale
- ❌ **Scalabilità Limitata**: Meno scalabile di Event Hub

#### Quando Usare

- ✅ Connessioni persistenti necessarie
- ✅ Volume eventi continuo
- ✅ Competenze avanzate disponibili

#### Quando NON Usare

- ❌ Setup semplice richiesto
- ❌ Volume eventi sporadico
- ❌ Team senza competenze avanzate

[Vedi Configurazione →](configurations/cometd-streaming.md) | [Vedi Implementazione →](implementation/cometd-streaming.md) | [Vedi Esempio →](examples/cometd-example.md)

## Confronto Architetture

### Webhook HTTP
```
┌─────────────┐      HTTP       ┌──────────────┐
│ Salesforce  │ ──────────────> │ Azure        │
│ (Apex)      │                 │ Function     │
└─────────────┘                 └──────────────┘
```

### Azure Event Hub
```
┌─────────────┐      HTTP       ┌──────────────┐      ┌──────────────┐
│ Salesforce  │ ──────────────> │ Event Hub    │ ───> │ Azure        │
│ (Apex)      │                 │              │      │ Function     │
└─────────────┘                 └──────────────┘      └──────────────┘
```

### CometD Streaming
```
┌─────────────┐   WebSocket     ┌──────────────┐
│ Salesforce  │ <=============> │ Azure        │
│ (CometD)    │   (Persistent)  │ Function     │
└─────────────┘                 └──────────────┘
```

## Confronto Costi (Stima Mensile)

### Scenario: 100.000 eventi/giorno

| Configurazione | Setup | Operativo | Totale |
|----------------|-------|-----------|--------|
| **Webhook HTTP** | $1000-2000 | $30-80 | $1030-2080 |
| **Event Hub** | $1500-2500 | $50-150 | $1550-2650 |
| **CometD** | $2000-3000 | $40-100 | $2040-3100 |

*Stime indicative, costi reali dipendono da volume e configurazione*

## Confronto Performance

| Configurazione | Throughput | Latenza | Affidabilità |
|----------------|------------|---------|--------------|
| **Webhook HTTP** | Media | < 1 min | Media |
| **Event Hub** | Alta | < 1 min | Alta |
| **CometD** | Media-Alta | < 1 min | Media |

## Decision Tree

```
Hai bisogno di persistenza eventi?
├─ SÌ → Azure Event Hub ⭐
└─ NO → Volume eventi elevato?
    ├─ SÌ → Azure Event Hub ⭐
    └─ NO → Connessione persistente necessaria?
        ├─ SÌ → CometD Streaming
        └─ NO → Webhook HTTP ⭐
```

## Raccomandazioni

### Per Proof of Concept

**Usa Webhook HTTP** - Setup rapido, costi contenuti.

### Per Produzione Enterprise

**Usa Azure Event Hub** - Scalabilità, affidabilità, persistenza.

### Per Connessioni Persistenti

**Usa CometD Streaming** - WebSocket long-running.

## Prossimi Passi

1. **Scegli una configurazione** basata sul confronto
2. **Consulta la configurazione** specifica: [Configurazioni](configurations/)
3. **Segui la guida di implementazione**: [Implementazione](implementation/)
4. **Vedi un caso d'esempio**: [Casi d'Esempio](examples/)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Salesforce Change Data Capture Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)



