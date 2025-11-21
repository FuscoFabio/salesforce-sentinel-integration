# Confronto Approcci di Integrazione

Questa pagina fornisce un confronto completo tra i due approcci principali per integrare Salesforce con Azure Sentinel.

## I Due Approcci Principali

### 1. Event Log Files API

**Caratteristiche**:
- ✅ **Copertura Completa**: Tutti gli eventi disponibili (LoginEvent, LogoutEvent, ApiEvent, Audit Trail, Field History Tracking)
- ✅ **Formato Strutturato**: Dati ottimizzati e validati da Salesforce
- ✅ **Affidabilità**: Dati consolidati e verificati
- ✅ **Setup Semplice**: Soluzioni code-less disponibili
- ❌ **Generazione oraria**: Salesforce produce gli Event Log Files in blocchi orari come indicato nella [documentazione ufficiale](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm)
- ❌ **Latenza**: 24-48 ore (limite strutturale: i connettori possono leggere i file solo dopo che il blocco orario è stato pubblicato)
- ✅ **Zero Sviluppo**: Non richiede codice Apex

**Quando Usare**:
- Analisi di sicurezza e compliance
- Audit trail completo
- Quando la latenza di 24-72 ore è accettabile
- Setup rapido senza sviluppo

### 2. Platform Events / Event Bus

**Caratteristiche**:
- ✅ **Latenza**: < 1 minuto (near real-time)
- ✅ **Tempo Reale**: Eventi disponibili immediatamente
- ❌ **Copertura Limitata**: Non tutti gli eventi disponibili (es. Audit Trail non disponibile)
- ❌ **Complessità**: Richiede sviluppo custom (Apex + Azure Function)
- ❌ **Manutenzione**: Gestione continua codice e configurazioni
- ❌ **Sviluppo Richiesto**: Necessario sviluppo Apex per trigger

**Quando Usare**:
- Monitoraggio in tempo reale (< 24 ore)
- Eventi critici che richiedono alerting immediato
- Competenze di sviluppo disponibili (Apex + Azure)
- Budget per sviluppo e manutenzione

## Confronto Dettagliato

| Aspetto | Event Log Files API | Platform Events / Event Bus |
|---------|---------------------|----------------------------|
| **Latenza** | 24-48 ore | < 1 minuto |
| **Copertura Eventi** | Completa (100%) | Limitata (~30-40%) |
| **Audit Trail** | ✅ Disponibile | ❌ Non disponibile |
| **Field History Tracking** | ✅ Disponibile | ❌ Non disponibile |
| **Setup** | Semplice (code-less) | Complesso (richiede sviluppo) |
| **Sviluppo Richiesto** | ❌ No | ✅ Sì (Apex + Azure) |
| **Manutenzione** | Bassa/Zero | Alta |
| **Costi Setup** | Basso | Medio-Alto |
| **Costi Operativi** | Basso | Medio |
| **Scalabilità** | Alta | Media-Alta |
| **Affidabilità** | Alta | Media (gestione errori custom) |
| **Personalizzazione** | Limitata | Completa |

## Eventi Disponibili

### Event Log Files API

**Eventi Disponibili**:
- ✅ LoginEvent
- ✅ LogoutEvent
- ✅ ApiEvent
- ✅ ReportEvent
- ✅ DashboardEvent
- ✅ ListViewEvent
- ✅ SearchEvent
- ✅ UriEvent
- ✅ Audit Trail (SetupAuditTrail)
- ✅ Field History Tracking
- ✅ Data Export Event
- ✅ E molti altri...

**Copertura**: ~100% degli eventi Salesforce

### Platform Events / Event Bus

**Eventi Disponibili**:
- ✅ LoginEvent (se configurato)
- ✅ LogoutEvent (se configurato)
- ✅ ApiEvent (se configurato)
- ✅ Eventi custom (Platform Events personalizzati)
- ✅ Change Data Capture (CDC) events
- ❌ Audit Trail (non disponibile)
- ❌ Field History Tracking (non disponibile)
- ❌ Molti eventi di sistema

**Copertura**: ~30-40% degli eventi Salesforce

## Soluzioni Disponibili per Approccio

### Event Log Files API

1. **CCF (CodeLess Connector Framework)** ⭐ Consigliato
   - Setup: 30-60 minuti
   - Manutenzione: Zero
   - Costo: Basso

2. **Azure Function**
   - Setup: 1-2 giorni
   - Manutenzione: Media
   - Costo: Medio

3. **Azure Logic App**
   - Setup: 30-60 minuti
   - Manutenzione: Bassa
   - Costo: Medio

### Platform Events / Event Bus

1. **Azure Function + Webhook HTTP**
   - Setup: 2-3 giorni
   - Manutenzione: Alta
   - Costo: Medio-Alto

2. **Azure Function + Event Hub** ⭐ Consigliato
   - Setup: 3-4 giorni
   - Manutenzione: Alta
   - Costo: Medio-Alto

3. **Azure Function + CometD Streaming**
   - Setup: 3-5 giorni
   - Manutenzione: Alta
   - Costo: Medio-Alto

## Scelta dell'Approccio

### Scegli Event Log Files API se:

- ✅ La latenza di 24-72 ore è accettabile
- ✅ Hai bisogno di copertura completa (incluso Audit Trail)
- ✅ Vuoi setup semplice e zero manutenzione
- ✅ Budget limitato
- ✅ Non hai competenze di sviluppo Apex

**Raccomandazione**: Inizia con **CCF** per il 90% dei casi d'uso.

### Scegli Platform Events se:

- ✅ Hai bisogno di monitoraggio near real-time (< 24 ore)
- ✅ Eventi critici richiedono alerting immediato
- ✅ Hai competenze di sviluppo (Apex + Azure Function)
- ✅ Budget per sviluppo e manutenzione
- ✅ Puoi accettare copertura limitata degli eventi

**Raccomandazione**: Usa **Azure Function + Event Hub** per scalabilità e affidabilità.

## Approccio Ibrido (Consigliato per Copertura Completa)

Per massimizzare copertura e latenza, combina entrambi gli approcci:

### Architettura Ibrida

```
┌─────────────────────────────────────────────────────────┐
│                    Salesforce                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐      ┌──────────────────────┐   │
│  │  Platform Events │      │  Event Log Files API │   │
│  │  (Event Bus)     │      │                      │   │
│  └────────┬─────────┘      └──────────┬───────────┘   │
│           │                            │                │
└───────────┼────────────────────────────┼────────────────┘
            │                            │
            │ Near Real-Time             │ 24-48h
            │ (< 1 minuto)               │
            │                            │
┌───────────▼────────────────────────────▼───────────────┐
│                  Azure Sentinel                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐      ┌──────────────────────┐   │
│  │  Eventi Critici  │      │  Copertura Completa  │   │
│  │  (Real-Time)     │      │  (Compliance)        │   │
│  │                  │      │                      │   │
│  │  - LoginEvent    │      │  - Tutti gli eventi  │   │
│  │  - ApiEvent      │      │  - Audit Trail       │   │
│  │  - Eventi Custom │      │  - Field History     │   │
│  └──────────────────┘      └──────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Vantaggi Approccio Ibrido

- ✅ **Copertura Completa**: Event Log Files per tutti gli eventi
- ✅ **Latenza Bassa**: Platform Events per eventi critici
- ✅ **Compliance**: Audit Trail completo
- ✅ **Alerting Real-Time**: Per eventi critici
- ✅ **Analisi Storica**: Dati completi per analisi

### Quando Usare Approccio Ibrido

- Organizzazioni enterprise con requisiti complessi
- Necessità di compliance completa + monitoraggio real-time
- Budget per entrambe le soluzioni
- Team con competenze tecniche

## Prossimi Passi

1. **Valuta i requisiti**: Latenza accettabile? Copertura completa necessaria?
2. **Scegli l'approccio**: Event Log Files o Platform Events (o ibrido)
3. **Scegli la soluzione**: Consulta le pagine specifiche per ogni approccio
4. **Consulta le guide**: Vai alle sezioni di implementazione per guide dettagliate

- [Event Log Files API - Panoramica](../event-log-files/overview.md)
- [Platform Events - Panoramica](../platform-events/overview.md)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)


