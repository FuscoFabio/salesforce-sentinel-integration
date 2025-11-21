# Panoramica Soluzioni

Questa pagina fornisce un confronto completo di tutte le soluzioni disponibili per integrare Salesforce con Azure Sentinel.

## ⚠️ Differenza Fondamentale: Event Log Files vs Platform Events

Prima di scegliere una soluzione, è fondamentale comprendere la differenza tra i due approcci di integrazione:

### Event Log Files API (Latenza 24-48 ore)

**Caratteristiche**:
- ✅ **Copertura Completa**: Tutti gli eventi disponibili (LoginEvent, LogoutEvent, ApiEvent, Audit Trail, etc.)
- ✅ **Formato Strutturato**: Dati ottimizzati e validati
- ✅ **Affidabilità**: Dati consolidati da Salesforce
- ❌ **Incrementi orari**: I log vengono generati e pubblicati da Salesforce una volta completato ogni blocco orario (vedi [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm))
- ❌ **Latenza**: 24-48 ore end-to-end per Log Analytics, anche usando connettori ufficiali come il CCF
- ✅ **Setup Semplice**: Soluzioni code-less disponibili

**Quando Usare**: Per analisi di sicurezza, compliance, audit trail, quando la latenza di 24-72 ore è accettabile.

### Platform Events / Event Bus (Near Real-Time)

**Caratteristiche**:
- ✅ **Latenza**: < 1 minuto (near real-time)
- ✅ **Tempo Reale**: Eventi disponibili immediatamente
- ❌ **Copertura Limitata**: Non tutti gli eventi disponibili (es. Audit Trail non disponibile)
- ❌ **Complessità**: Richiede sviluppo custom (Apex + Azure Function)
- ❌ **Manutenzione**: Gestione codice e configurazioni

**Quando Usare**: Quando è necessario monitoraggio in tempo reale (< 24 ore) per eventi critici.

## Soluzioni per Event Log Files API

### 1. CodeLess Connector Framework (CCF) ⭐ Consigliato

**Caratteristiche**:
- Setup: 30-60 minuti (configurazione grafica)
- Manutenzione: Zero (gestito da Microsoft)
- Costo: Basso (solo ingestione dati)
- Personalizzazione: Limitata

**Vantaggi**:
- Zero codice richiesto
- Gestione automatica errori e retry
- Polling ottimizzato (15-30 minuti)

[Vedi dettagli →](ccf.md)

### 2. Azure Function (Event Log Files)

**Caratteristiche**:
- Setup: 1-2 giorni (sviluppo custom)
- Manutenzione: Media-Alta (gestione codice)
- Costo: Medio (sviluppo + Azure)
- Personalizzazione: Alta

**Vantaggi**:
- Controllo completo sulla logica
- Personalizzazione avanzata
- Integrazione con altri sistemi

**Quando Usare**: Quando hai bisogno di personalizzazioni che il CCF non supporta.

[Vedi dettagli →](azure-function.md)

### 3. Azure Logic App (Event Log Files)

**Caratteristiche**:
- Setup: 30-60 minuti (low-code visuale)
- Manutenzione: Bassa
- Costo: Medio
- Personalizzazione: Media

**Vantaggi**:
- Approccio visuale low-code
- Template predefiniti
- Connettori integrati

[Vedi dettagli →](logic-app.md)

## Soluzioni per Platform Events (Near Real-Time)

### 4. Azure Function + Platform Events

**Caratteristiche**:
- Setup: 2-3 giorni (sviluppo Apex + Azure Function)
- Manutenzione: Alta (gestione codice)
- Costo: Medio-Alto (sviluppo + Azure)
- Latenza: < 1 minuto

**Approcci Disponibili**:
- **Webhook HTTP**: Salesforce → Apex Trigger → HTTP → Azure Function
- **Event Hub**: Salesforce → Apex Trigger → Event Hub → Azure Function
- **CometD Streaming**: Salesforce → Platform Events → CometD → Azure Function

**Vantaggi**:
- Near real-time (< 1 minuto)
- Controllo completo
- Scalabilità con Event Hub

**Limitazioni**:
- Copertura eventi limitata
- Richiede sviluppo Apex
- Manutenzione continua

[Vedi dettagli →](../implementation/platform-events.md)

## Confronto Completo

| Soluzione | Approccio | Latenza | Copertura | Complessità | Costo | Setup Time |
|-----------|-----------|---------|-----------|-------------|-------|------------|
| **CCF** | Event Log Files | 24-72h | Completa | Bassa | Basso | 30-60 min |
| **Azure Function** | Event Log Files | 24-72h | Completa | Media | Medio | 1-2 giorni |
| **Logic App** | Event Log Files | 24-72h | Completa | Bassa | Medio | 30-60 min |
| **Function + Platform Events** | Event Bus | < 1 min | Limitata | Alta | Medio-Alto | 2-3 giorni |

## Come Scegliere

### Scegli Event Log Files API se:
- ✅ La latenza di 24-72 ore è accettabile
- ✅ Hai bisogno di copertura completa (incluso Audit Trail)
- ✅ Vuoi setup semplice e zero manutenzione
- ✅ Budget limitato

**Raccomandazione**: **CCF** per il 90% dei casi d'uso.

### Scegli Platform Events se:
- ✅ Hai bisogno di monitoraggio near real-time (< 24 ore)
- ✅ Eventi critici richiedono alerting immediato
- ✅ Hai competenze di sviluppo (Apex + Azure)
- ✅ Budget per sviluppo e manutenzione

**Raccomandazione**: **Azure Function + Event Hub** per scalabilità e affidabilità.

### Approccio Ibrido (Consigliato per Copertura Completa)

Combina entrambi gli approcci:
- **Platform Events** per eventi critici in tempo reale
- **Event Log Files (CCF)** per copertura completa e compliance

## Prossimi Passi

1. **Valuta i requisiti**: Latenza accettabile? Copertura completa necessaria?
2. **Scegli l'approccio**: Event Log Files o Platform Events
3. **Scegli la soluzione**: CCF, Azure Function, Logic App
4. **Consulta la documentazione**: Vai alla sezione [Implementazione](../implementation/) per guide dettagliate

Per maggiori dettagli, consulta le pagine specifiche di ogni soluzione o il [repository GitHub](https://github.com/FuscoFabio/salesforce-sentinel-integration).

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)

