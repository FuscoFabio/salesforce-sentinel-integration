# Platform Events / Event Bus - Panoramica

Panoramica completa dell'approccio Platform Events (Event Bus) per l'integrazione near real-time tra Salesforce e Azure Sentinel.

## Cos'è Platform Events?

Platform Events è la piattaforma di eventi real-time di Salesforce che permette di pubblicare e sottoscriversi a eventi in tempo reale. Gli eventi vengono pubblicati su un "Event Bus" e possono essere consumati da sistemi esterni tramite vari meccanismi.

## Caratteristiche Principali

### ✅ Vantaggi

- **Latenza Bassa**: < 1 minuto (near real-time)
- **Tempo Reale**: Eventi disponibili immediatamente
- **Push-Based**: Eventi inviati quando si verificano
- **Scalabilità**: Gestione automatica del carico
- **Personalizzazione**: Controllo completo sulla logica

### ❌ Limitazioni

- **Copertura Limitata**: Non tutti gli eventi disponibili
- **Sviluppo Richiesto**: Necessario sviluppo Apex
- **Complessità**: Setup e manutenzione complessi
- **Costi**: Sviluppo e manutenzione continui
- **Audit Trail**: Non disponibile su Platform Events

## Come Funziona

### Processo di Generazione Eventi

```
1. Evento Generato in Salesforce
   ↓
2. Apex Trigger / Process Builder Intercetta
   ↓
3. Evento Pubblicato su Platform Event / Event Bus
   ↓
4. Sistema Esterno Consuma (HTTP / Event Hub / CometD)
   ↓
5. Trasformazione e Invio a Azure Sentinel
   ↓
6. Disponibile in Sentinel (< 1 minuto)
```

### Architettura Generale

```
Salesforce Platform Events (Event Bus)
    ↓
Apex Trigger / Process Builder
    ↓
Meccanismo di Consumo (HTTP / Event Hub / CometD)
    ↓
Azure Function / Processing Layer
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Eventi Disponibili

### Eventi Standard Disponibili

- **LoginEvent** (se configurato)
- **LogoutEvent** (se configurato)
- **ApiEvent** (se configurato)
- **Change Data Capture (CDC)** events
- **Platform Events Custom** (personalizzati)

### Eventi NON Disponibili

- ❌ **Audit Trail** (SetupAuditTrail)
- ❌ **Field History Tracking**
- ❌ **ReportEvent**
- ❌ **DashboardEvent**
- ❌ **Data Export Event**
- ❌ Molti altri eventi di sistema

**Copertura**: ~30-40% degli eventi disponibili su Event Log Files

## Configurazioni Disponibili

Tre configurazioni principali sono disponibili:

### 1. Webhook HTTP ⭐ Più Semplice

**Architettura**:
```
Salesforce → Apex Trigger → HTTP Callout → Azure Function (HTTP) → Sentinel
```

**Caratteristiche**:
- Setup: 2-3 giorni
- Complessità: Media
- Scalabilità: Media
- Affidabilità: Media

[Vedi dettagli →](configurations/webhook-http.md)

### 2. Azure Event Hub ⭐ Consigliato

**Architettura**:
```
Salesforce → Apex Trigger → HTTP → Event Hub → Azure Function (Event Hub Trigger) → Sentinel
```

**Caratteristiche**:
- Setup: 3-4 giorni
- Complessità: Alta
- Scalabilità: Alta
- Affidabilità: Alta

[Vedi dettagli →](configurations/event-hub.md)

### 3. CometD Streaming

**Architettura**:
```
Salesforce → Platform Events → CometD WebSocket → Azure Function → Sentinel
```

**Caratteristiche**:
- Setup: 3-5 giorni
- Complessità: Molto Alta
- Scalabilità: Media-Alta
- Affidabilità: Media

[Vedi dettagli →](configurations/cometd-streaming.md)

## Limitazioni

### Copertura Eventi

**Eventi Disponibili**:
- Solo eventi configurati esplicitamente
- Eventi custom (Platform Events personalizzati)
- Change Data Capture (CDC) events

**Eventi NON Disponibili**:
- Audit Trail
- Field History Tracking
- Molti eventi di sistema

### Requisiti Tecnici

- **Sviluppo Apex**: Richiesto per trigger e callout
- **Sviluppo Azure Function**: Richiesto per processing
- **Manutenzione**: Gestione continua codice
- **Competenze**: Sviluppatori Apex e Azure Function

### Rate Limits

- **Platform Events pubblicati**: 2.000.000/giorno (Enterprise)
- **API Callouts**: 100.000/giorno (Enterprise)
- **Concurrent Callouts**: 10 simultanee

## Quando Usare Platform Events

### ✅ Ideale per:

- Monitoraggio near real-time (< 24 ore)
- Eventi critici che richiedono alerting immediato
- Competenze di sviluppo disponibili
- Budget per sviluppo e manutenzione
- Eventi custom specifici

### ❌ Non Ideale per:

- Audit trail completo
- Copertura completa degli eventi
- Setup semplice senza sviluppo
- Budget limitato
- Team senza competenze di sviluppo

## Confronto con Event Log Files

| Aspetto | Platform Events | Event Log Files |
|---------|----------------|-----------------|
| **Latenza** | < 1 minuto | 24-48 ore |
| **Copertura** | Limitata (~30-40%) | Completa (100%) |
| **Setup** | Complesso | Semplice |
| **Sviluppo** | Richiesto | Non richiesto |
| **Audit Trail** | ❌ | ✅ |
| **Manutenzione** | Alta | Bassa/Zero |

[Vedi confronto completo →](../introduction/approaches-comparison.md)

## Approccio Ibrido (Consigliato)

Per massimizzare copertura e latenza, combina entrambi:

- **Platform Events**: Eventi critici in tempo reale
- **Event Log Files (CCF)**: Copertura completa e compliance

[Vedi dettagli approccio ibrido →](../introduction/approaches-comparison.md#approccio-ibrido-consigliato-per-copertura-completa)

## Prossimi Passi

1. **Confronta le configurazioni**: [Confronto Configurazioni](configurations-comparison.md)
2. **Scegli una configurazione**: [Configurazioni Disponibili](configurations/)
3. **Segui la guida di implementazione**: [Implementazione](implementation/)
4. **Vedi casi d'esempio**: [Casi d'Esempio](examples/)

## Fonti

- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Salesforce Change Data Capture Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)



