# Platform Events (Near Real-Time)

Soluzione per integrazione near real-time tra Salesforce e Azure Sentinel usando Platform Events (Event Bus).

## Panoramica

Questa soluzione utilizza **Platform Events** (Event Bus) di Salesforce per ottenere eventi in **tempo reale** (< 1 minuto di latenza) invece dei 24-48 ore degli Event Log Files API.

## ⚠️ Differenza Chiave: Event Bus vs Event Log Files

### Platform Events (Event Bus)
- ✅ **Latenza**: < 1 minuto (near real-time)
- ✅ **Tempo Reale**: Eventi disponibili immediatamente
- ❌ **Copertura Limitata**: Non tutti gli eventi disponibili
- ❌ **Complessità**: Richiede sviluppo custom

### Event Log Files API
- ❌ **Latenza**: 24-48 ore (limite strutturale)
- ✅ **Copertura Completa**: Tutti gli eventi disponibili
- ✅ **Setup Semplice**: Soluzioni code-less disponibili

## Quando Usare Platform Events

**Scegli Platform Events se**:
- ✅ Hai bisogno di monitoraggio near real-time (< 24 ore)
- ✅ Eventi critici richiedono alerting immediato
- ✅ Hai competenze di sviluppo (Apex + Azure Function)
- ✅ Budget per sviluppo e manutenzione

**Non scegliere Platform Events se**:
- ❌ Hai bisogno di Audit Trail (non disponibile)
- ❌ Vuoi setup semplice senza codice
- ❌ Budget limitato
- ❌ Non hai competenze di sviluppo

## Architettura

```
Salesforce Platform Events (Event Bus)
    ↓
Apex Trigger / Process Builder
    ↓
HTTP Callout / Event Hub / CometD
    ↓
Azure Function
    ↓
Log Analytics / Azure Sentinel
```

## Approcci Disponibili

### 1. Webhook HTTP (Più Semplice)

**Architettura**:
- Salesforce → Apex Trigger → HTTP Callout → Azure Function (HTTP Trigger) → Sentinel

**Vantaggi**:
- Implementazione relativamente semplice
- Nessun componente intermedio
- Controllo diretto

**Svantaggi**:
- Gestione timeout e retry
- Limitato da callout limits Salesforce

### 2. Azure Event Hub (⭐ Consigliato)

**Architettura**:
- Salesforce → Apex Trigger → HTTP → Event Hub → Azure Function (Event Hub Trigger) → Sentinel

**Vantaggi**:
- Scalabilità automatica
- Affidabilità (persistenza eventi)
- Decoupling tra Salesforce e Function
- Gestione picchi automatica

**Svantaggi**:
- Componente aggiuntivo (Event Hub)
- Costi aggiuntivi

### 3. CometD Streaming API

**Architettura**:
- Salesforce → Platform Events → CometD WebSocket → Azure Function → Sentinel

**Vantaggi**:
- Connessione persistente
- Push real-time

**Svantaggi**:
- Complessità gestione WebSocket
- Richiede processo long-running

## Limitazioni

### Copertura Eventi

**Eventi Disponibili**:
- ✅ LoginEvent (se configurato)
- ✅ LogoutEvent (se configurato)
- ✅ ApiEvent (se configurato)
- ✅ Eventi custom

**Eventi NON Disponibili**:
- ❌ Audit Trail (solo su Event Log Files)
- ❌ Field History Tracking (solo su Event Log Files)
- ❌ Alcuni eventi di sicurezza avanzati

### Requisiti Tecnici

- **Sviluppo Apex**: Richiesto per trigger e callout
- **Sviluppo Azure Function**: Richiesto per processing
- **Manutenzione**: Gestione continua codice e configurazioni
- **Competenze**: Sviluppatori Apex e Azure Function

### Rate Limits

- **Platform Events pubblicati**: 2.000.000/giorno (Enterprise)
- **API Callouts**: 100.000/giorno (Enterprise)
- **Concurrent Callouts**: 10 simultanee

## Implementazione

Vedi la guida completa: [Implementazione Platform Events](../implementation/platform-events.md)

La guida include:
- Configurazione Platform Events in Salesforce
- Sviluppo Apex Trigger
- Implementazione Azure Function
- Configurazione Event Hub (se usato)
- Gestione errori e retry
- Best practices

## Costi

- **Sviluppo iniziale**: 2-3 giorni di sviluppo
- **Azure Function**: Costi esecuzione (Consumption o Premium Plan)
- **Event Hub** (se usato): ~$10-20/mese base + throughput
- **Log Analytics**: Costi ingestione dati
- **Manutenzione**: Costi continui per aggiornamenti

**Totale stimato**: $50-200/mese + costi sviluppo iniziale

## Confronto con Event Log Files

| Aspetto | Platform Events | Event Log Files (CCF) |
|---------|----------------|----------------------|
| **Latenza** | < 1 minuto | 24-48 ore |
| **Copertura** | Limitata | Completa |
| **Setup** | 2-3 giorni | 30-60 minuti |
| **Manutenzione** | Alta | Zero |
| **Costi** | Medio-Alto | Basso |
| **Audit Trail** | ❌ | ✅ |

## Approccio Ibrido (Consigliato)

Per massimizzare copertura e latenza, combina entrambi:

- **Platform Events**: Eventi critici in tempo reale
- **Event Log Files (CCF)**: Copertura completa e compliance

## Link Utili

- [Implementazione Platform Events](../implementation/platform-events.md)
- [Implementazione Azure Function](../implementation/azure-function.md)
- [Network e Sicurezza](../implementation/network-sicurezza.md)
- [Salesforce Platform Events Documentation](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Salesforce Change Data Capture Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)




