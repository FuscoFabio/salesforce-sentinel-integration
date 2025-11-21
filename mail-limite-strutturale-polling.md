# Mail: Limite Strutturale Polling e Raccomandazioni

**Oggetto:** Integrazione Salesforce-Azure Sentinel: Chiarimento Limite Strutturale Event Log Files e Raccomandazioni

---

Gentile [Nome],

ti scrivo per chiarire un aspetto fondamentale dell'integrazione Salesforce-Azure Sentinel che riguarda il **limite strutturale di polling** imposto dalla piattaforma Salesforce, indipendentemente dalla soluzione di integrazione scelta.

## ⚠️ Limite Strutturale: Disponibilità Event Log Files

### Cosa Significa "Event Log Files Disponibili dopo 24-48 Ore"

È importante comprendere che questo limite non è un vincolo tecnico delle soluzioni di integrazione (CCF o Azure Function), ma un **limite intrinseco del sistema Event Monitoring di Salesforce**.

#### Come Funziona il Processo in Salesforce

1. **Generazione Evento in Tempo Reale**:
   - Quando un utente accede a Salesforce (es. login), l'evento viene registrato immediatamente nel sistema
   - L'evento è visibile in tempo reale tramite i log di debug e le API di monitoraggio in tempo reale

2. **Elaborazione Batch di Salesforce**:
   - Salesforce elabora gli eventi in **batch giornalieri** per creare gli Event Log Files
   - Questo processo di aggregazione e consolidamento avviene **dopo** la generazione dell'evento
   - Il processo batch di Salesforce richiede **24-48 ore** per completare l'elaborazione

3. **Disponibilità Event Log Files**:
   - Solo **dopo** il completamento del batch, gli Event Log Files diventano disponibili tramite l'API Event Log Files
   - Questo è l'unico modo per recuperare eventi storici in modo strutturato e completo
   - **Nessuna soluzione di integrazione può aggirare questo limite**, perché dipende dal processo interno di Salesforce

#### Implicazioni Pratiche

**Scenario Esempio:**
- **Lunedì 10:00** - Un utente effettua il login a Salesforce
- **Lunedì 10:00-10:05** - L'evento è visibile in tempo reale tramite debug log (non strutturato)
- **Martedì-Mercoledì** - Salesforce elabora il batch e crea l'Event Log File
- **Mercoledì 10:00** - L'Event Log File diventa disponibile tramite API (24-48 ore dopo)

**Cosa Significa per l'Integrazione:**
- Non è possibile ottenere eventi "in tempo reale" (< 24 ore) tramite Event Log Files API
- Il polling frequente (< 5 minuti) non migliora la disponibilità dei dati
- La latenza totale è: **24-48 ore (Salesforce) + 15-30 minuti (polling) = 24-72 ore totali**

### Perché Questo Limite Esiste

Salesforce elabora gli eventi in batch per:
- **Performance**: Elaborazione efficiente di milioni di eventi
- **Consolidamento**: Aggregazione e deduplicazione degli eventi
- **Ottimizzazione Storage**: Compressione e ottimizzazione dei file
- **Affidabilità**: Validazione e verifica dell'integrità dei dati

Questo è un **design decision** di Salesforce e non può essere modificato o aggirato.

### Limiti Comuni a Tutte le Soluzioni

Indipendentemente dalla soluzione scelta (CCF, Azure Function, Logic App), tutti devono rispettare:

1. **Delay Event Log Files**: 24-48 ore (limite Salesforce)
2. **Limiti API Salesforce**:
   - Enterprise: ~15.000 richieste/24h
   - Unlimited: ~100.000 richieste/24h
   - Performance: ~50.000 richieste/24h
   - Concurrent Requests: Massimo 25 simultanee

3. **Intervallo Polling Minimo Pratico**: 5 minuti
   - Polling più frequente non migliora la disponibilità dati
   - Aumenta solo i costi e il rischio di rate limiting

## Raccomandazioni Finali: CCF vs Azure Function

### Quando Scegliere CCF (Raccomandato per il 90% dei Casi)

Il **CCF (CodeLess Connector Framework)** è la soluzione consigliata quando:

✅ **Requisiti Standard**:
- Raccolta eventi Salesforce (LoginEvent, LogoutEvent, ApiEvent)
- Invio diretto a Azure Sentinel
- Trasformazione dati base (mapping campi standard)
- Filtri semplici (per tipo evento, data, utente)

✅ **Vantaggi Operativi**:
- Setup in 30-60 minuti (vs 1-2 giorni per Azure Function)
- Zero manutenzione (gestito da Microsoft)
- Costi minimi (solo ingestione dati)
- Affidabilità garantita (retry automatico, gestione errori)

✅ **Casi d'Uso Tipici**:
- Monitoraggio sicurezza e compliance
- Analisi accessi e audit trail
- Rilevamento pattern sospetti
- Reportistica e dashboard

### Quando Scegliere Azure Function (Casi Specifici)

L'**Azure Function** è consigliabile solo quando hai **requisiti di personalizzazione avanzata** che il CCF non può soddisfare. Ecco esempi concreti:

#### Esempio 1: Enrichment Dati con Sistemi Esterni

**Scenario**: Arricchire gli eventi Salesforce con informazioni da sistemi esterni prima di inviarli a Azure Sentinel.

**Requisito Specifico**:
- Recuperare informazioni utente da Active Directory
- Aggiungere dati di geolocalizzazione da servizio esterno
- Integrare con database interno per classificazione utenti
- Aggiungere metadati da sistema di gestione identità

**Perché CCF Non Basta**: Il CCF può solo mappare campi esistenti, non può fare chiamate a sistemi esterni per arricchire i dati.

**Soluzione Azure Function**: Implementare logica custom che:
```csharp
// Esempio pseudocodice
foreach (var evento in eventiSalesforce) {
    var userInfo = await GetUserFromAD(evento.UserId);
    var geoInfo = await GetGeoLocation(evento.SourceIP);
    var classification = await GetUserClassification(evento.UserId);
    
    evento.EnrichedData = new {
        Department = userInfo.Department,
        Country = geoInfo.Country,
        RiskLevel = classification.RiskLevel
    };
}
```

#### Esempio 2: Trasformazione Schema Complessa

**Scenario**: Trasformare lo schema dati in modo complesso o condizionale.

**Requisito Specifico**:
- Normalizzare dati da formati diversi
- Applicare regole di business complesse
- Creare eventi derivati da eventi originali
- Aggregare eventi multipli in un singolo record

**Perché CCF Non Basta**: Il CCF supporta solo mapping 1:1 dei campi, non trasformazioni complesse.

**Soluzione Azure Function**: Implementare logica di trasformazione custom:
```csharp
// Esempio: Creare evento derivato
if (evento.EventType == "LoginEvent" && evento.SourceIP.StartsWith("10.")) {
    var eventoInterno = new {
        Type = "InternalAccess",
        User = evento.UserName,
        Location = "Corporate Network",
        Timestamp = evento.TimeGenerated
    };
    await SendToSentinel(eventoInterno);
}
```

#### Esempio 3: Routing Condizionale Multi-Destinazione

**Scenario**: Inviare eventi a destinazioni diverse in base a criteri complessi.

**Requisito Specifico**:
- Eventi critici → Azure Sentinel + Sistema di ticketing
- Eventi normali → Solo Azure Sentinel
- Eventi specifici → Database interno + Azure Sentinel
- Eventi di compliance → Azure Sentinel + Archivio a lungo termine

**Perché CCF Non Basta**: Il CCF invia solo a Azure Sentinel, non supporta routing condizionale.

**Soluzione Azure Function**: Implementare routing custom:
```csharp
if (evento.IsCritical) {
    await SendToSentinel(evento);
    await CreateTicket(evento);
} else if (evento.RequiresCompliance) {
    await SendToSentinel(evento);
    await ArchiveToLongTermStorage(evento);
} else {
    await SendToSentinel(evento);
}
```

#### Esempio 4: Integrazione con Sistemi Aggiuntivi

**Scenario**: Integrare eventi Salesforce con altri sistemi oltre Azure Sentinel.

**Requisito Specifico**:
- Inviare alert a Slack/Teams quando rilevati accessi sospetti
- Creare ticket automatici in ServiceNow
- Aggiornare dashboard interno in tempo reale
- Sincronizzare con sistema di gestione identità

**Perché CCF Non Basta**: Il CCF è progettato solo per Azure Sentinel.

**Soluzione Azure Function**: Implementare integrazioni multiple:
```csharp
await SendToSentinel(evento);
if (evento.IsSuspicious) {
    await SendSlackAlert(evento);
    await CreateServiceNowTicket(evento);
    await UpdateInternalDashboard(evento);
}
```

#### Esempio 5: Logica di Business Complessa

**Scenario**: Applicare regole di business specifiche dell'organizzazione.

**Requisito Specifico**:
- Calcolare score di rischio basato su pattern complessi
- Applicare regole di whitelist/blacklist dinamiche
- Implementare logica di correlazione tra eventi
- Creare metriche personalizzate

**Perché CCF Non Basta**: Il CCF non supporta logica di business custom.

**Soluzione Azure Function**: Implementare regole custom:
```csharp
var riskScore = CalculateRiskScore(evento, historicalEvents);
if (riskScore > threshold) {
    evento.RiskLevel = "High";
    await TriggerInvestigation(evento);
}
```

#### Esempio 6: Filtri Dinamici e Complessi

**Scenario**: Applicare filtri che cambiano dinamicamente o sono molto complessi.

**Requisito Specifico**:
- Filtri basati su query a database esterno
- Filtri che cambiano in base a configurazione runtime
- Filtri che richiedono correlazione con altri eventi
- Filtri basati su machine learning o AI

**Perché CCF Non Basta**: Il CCF supporta solo filtri statici configurabili.

**Soluzione Azure Function**: Implementare filtri dinamici:
```csharp
var filterConfig = await GetDynamicFilterConfig();
var shouldProcess = await EvaluateComplexFilter(evento, filterConfig);
if (shouldProcess) {
    await SendToSentinel(evento);
}
```

### Riepilogo: Quando Serve Azure Function

| Requisito | CCF | Azure Function |
|-----------|-----|----------------|
| Raccolta eventi standard | ✅ | ✅ |
| Invio a Azure Sentinel | ✅ | ✅ |
| Mapping campi base | ✅ | ✅ |
| Filtri semplici | ✅ | ✅ |
| Enrichment dati esterni | ❌ | ✅ |
| Trasformazione schema complessa | ❌ | ✅ |
| Routing multi-destinazione | ❌ | ✅ |
| Integrazione sistemi multipli | ❌ | ✅ |
| Logica business custom | ❌ | ✅ |
| Filtri dinamici complessi | ❌ | ✅ |

## Conclusione

**Per la maggior parte dei casi d'uso** (circa il 90%), il **CCF è la scelta migliore** perché:
- Soddisfa i requisiti standard di integrazione
- Setup rapido e zero manutenzione
- Costi contenuti
- Affidabilità garantita

**Scegli Azure Function solo se**:
- Hai uno o più dei requisiti di personalizzazione avanzata elencati sopra
- Hai competenze di sviluppo disponibili
- Il budget permette costi di sviluppo e manutenzione

**Importante**: Indipendentemente dalla soluzione scelta, il limite strutturale di **24-48 ore** per la disponibilità degli Event Log Files è un vincolo di Salesforce che **non può essere modificato o aggirato**.

Sono a disposizione per approfondire qualsiasi aspetto o valutare insieme quale soluzione si adatta meglio alle tue esigenze specifiche.

Cordiali saluti,

[Nome]  
[Ruolo]  
[Contatti]

---

**Riferimenti Documentazione:**
- CCF: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/ccf/
- Azure Function: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/azure-function/
- Limitazioni Polling: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/ccf/#limitazioni-e-limiti-di-polling








