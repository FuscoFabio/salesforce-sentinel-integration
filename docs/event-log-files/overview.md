# Event Log Files API - Panoramica

Panoramica completa dell'approccio Event Log Files API per l'integrazione Salesforce-Azure Sentinel.

## Cos'è Event Log Files API?

Event Log Files API è l'API ufficiale di Salesforce per recuperare eventi di monitoraggio in formato aggregato e strutturato. Gli eventi vengono processati e consolidati da Salesforce e resi disponibili tramite API REST.

## Caratteristiche Principali

### ✅ Vantaggi

- **Copertura Completa**: Tutti gli eventi disponibili in Salesforce
- **Formato Strutturato**: Dati ottimizzati e validati
- **Affidabilità**: Dati consolidati da Salesforce
- **Setup Semplice**: Soluzioni code-less disponibili
- **Zero Sviluppo**: Non richiede codice Apex
- **Manutenzione Bassa**: Gestione automatica da parte delle soluzioni

### ❌ Limitazioni

- **Incrementi orari**: I log vengono generati e resi disponibili solo per blocchi orari, come descritto nella [documentazione ufficiale Salesforce Event Log File Hourly](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm)
- **Latenza**: 24-48 ore (limite strutturale Salesforce dovuto all'elaborazione e pubblicazione dei file orari)
- **Personalizzazione Limitata**: Formato dati predefinito
- **Polling Necessario**: Richiede polling periodico

## Come Funziona

### Processo di Generazione Eventi

```
1. Evento Generato in Salesforce
   ↓
2. Salesforce Processa e Consolida (24-48 ore)
   ↓
3. Event Log File Creato
   ↓
4. Disponibile via API
   ↓
5. Soluzione di Integrazione Recupera (Polling)
   ↓
6. Trasformazione e Invio a Azure Sentinel
```

### Architettura Generale

```
Salesforce Event Monitoring
    ↓
Event Log Files API
    ↓
Soluzione di Integrazione (CCF / Function / Logic App)
    ↓
Trasformazione Dati
    ↓
Log Analytics Data Collector API
    ↓
Azure Sentinel
```

## Eventi Disponibili

### Eventi di Accesso

- **LoginEvent**: Accessi utente a Salesforce
- **LogoutEvent**: Disconnessioni utente
- **SessionHijackingEvent**: Tentativi di hijacking sessione

### Eventi API

- **ApiEvent**: Chiamate API a Salesforce
- **RestApiEvent**: Chiamate REST API
- **SoapApiEvent**: Chiamate SOAP API

### Eventi di Utilizzo

- **ReportEvent**: Visualizzazioni report
- **DashboardEvent**: Visualizzazioni dashboard
- **ListViewEvent**: Visualizzazioni liste
- **SearchEvent**: Ricerche eseguite
- **UriEvent**: Navigazione tra pagine

### Eventi di Sicurezza

- **SetupAuditTrail**: Audit trail completo (modifiche configurazione)
- **FieldHistoryTracking**: Storia modifiche campi
- **DataExportEvent**: Esportazioni dati
- **BulkApiResultEvent**: Risultati Bulk API

### Altri Eventi

- **ApexExecutionEvent**: Esecuzione codice Apex
- **ApexUnexpectedExceptionEvent**: Eccezioni Apex
- **FlowExecutionEvent**: Esecuzione Flow
- E molti altri...

**Totale**: Oltre 50 tipi di eventi disponibili

## Soluzioni Disponibili

### 1. CCF (CodeLess Connector Framework) ⭐ Consigliato

**Caratteristiche**:
- Setup: 30-60 minuti (configurazione grafica)
- Manutenzione: Zero (gestito da Microsoft)
- Costo: Basso (solo ingestione dati)
- Personalizzazione: Limitata

**Quando Usare**: Per il 90% dei casi d'uso standard.

[Vedi dettagli →](solutions-comparison.md#1-ccf-codeless-connector-framework-)

### 2. Azure Function

**Caratteristiche**:
- Setup: 1-2 giorni (sviluppo custom)
- Manutenzione: Media-Alta (gestione codice)
- Costo: Medio (sviluppo + Azure)
- Personalizzazione: Alta

**Quando Usare**: Quando hai bisogno di personalizzazioni avanzate.

[Vedi dettagli →](solutions-comparison.md#2-azure-function)

### 3. Azure Logic App

**Caratteristiche**:
- Setup: 30-60 minuti (low-code visuale)
- Manutenzione: Bassa
- Costo: Medio
- Personalizzazione: Media

**Quando Usare**: Quando preferisci un approccio visuale low-code.

[Vedi dettagli →](solutions-comparison.md#3-azure-logic-app)

## Limitazioni Strutturali

### Latenza 24-48 Ore

**Incrementi orari obbligatori**

- Il connettore (CCF, Function o Logic App) scarica esclusivamente gli **Event Log Files** che Salesforce pubblica una volta completata l'elaborazione del blocco orario
- Anche se i file vengono suddivisi per ore, Salesforce può impiegare fino a 24-48 ore per renderli disponibili tramite API
- L'intervallo orario è quindi la cadenza minima di generazione, **non** la reale latenza end-to-end

**Perché esiste questa latenza?**

Salesforce processa e consolida gli eventi prima di renderli disponibili tramite Event Log Files API. Questo processo include:
- Validazione eventi
- Consolidamento dati
- Ottimizzazione formato
- Verifica integrità

**Implicazioni**:
- Non adatto per alerting real-time
- Adatto per analisi storica e compliance
- Polling più frequente non riduce la latenza
- Tutti i connettori basati su Event Log Files (incluso il CCF ufficiale Microsoft Sentinel) ereditano automaticamente questo ritardo strutturale

### Rate Limiting

Salesforce impone limiti sulle chiamate API:
- **API Calls per giorno**: Dipende dalla licenza
- **Concurrent Requests**: Limitato
- **Polling Ottimale**: 15-30 minuti (CCF), 5-15 minuti (Function)

## Quando Usare Event Log Files API

### ✅ Ideale per:

- Analisi di sicurezza e compliance
- Audit trail completo
- Monitoraggio storico
- Reportistica e analisi
- Quando la latenza di 24-72 ore è accettabile
- Setup rapido senza sviluppo

### ❌ Non Ideale per:

- Alerting real-time (< 24 ore)
- Monitoraggio critico immediato
- Eventi che richiedono risposta immediata

## Confronto con Platform Events

| Aspetto | Event Log Files | Platform Events |
|---------|----------------|-----------------|
| **Latenza** | 24-48 ore | < 1 minuto |
| **Copertura** | Completa (100%) | Limitata (~30-40%) |
| **Setup** | Semplice | Complesso |
| **Sviluppo** | Non richiesto | Richiesto |
| **Audit Trail** | ✅ | ❌ |

[Vedi confronto completo →](../introduction/approaches-comparison.md)

## Prossimi Passi

1. **Confronta le soluzioni**: [Confronto Soluzioni Event Log Files](solutions-comparison.md)
2. **Scegli una configurazione**: [Configurazioni Disponibili](configurations/)
3. **Segui la guida di implementazione**: [Implementazione](implementation/)
4. **Vedi casi d'esempio**: [Casi d'Esempio](examples/)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)


