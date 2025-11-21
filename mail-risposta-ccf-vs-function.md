# Mail di Risposta: CCF vs Azure Function

**Oggetto:** Integrazione Salesforce-Azure Sentinel: Raccomandazione CCF e Considerazioni sul Polling

---

Gentile [Nome],

in riferimento alla richiesta di integrazione tra Salesforce e Azure Sentinel, ti presento un'analisi comparativa delle soluzioni disponibili, con particolare attenzione ai limiti strutturali di polling imposti da Salesforce.

## Raccomandazione: CodeLess Connector Framework (CCF)

Il **CCF (CodeLess Connector Framework)** è la soluzione che raccomandiamo per la maggior parte dei casi d'uso, per i seguenti motivi:

### Vantaggi del CCF

✅ **Setup Rapido e Zero Manutenzione**
- Configurazione completamente grafica, senza necessità di sviluppo codice
- Connector gestito da Microsoft, con aggiornamenti e manutenzione automatica
- Tempo di setup: 30-60 minuti vs 1-2 giorni per Azure Function

✅ **Costi Ottimizzati**
- Nessun costo di sviluppo iniziale
- Nessun costo di manutenzione del codice
- Costi Azure minimi (solo per l'ingestione dati in Log Analytics)

✅ **Sicurezza e Compliance**
- Gestione automatica delle credenziali
- Supporto per Azure Private Link (se necessario)
- Audit trail completo integrato

✅ **Affidabilità**
- Retry automatico con backoff esponenziale
- Gestione errori integrata
- Monitoraggio nativo tramite Azure Sentinel

### Configurazione Polling CCF

Il CCF offre una configurazione di polling ottimizzata:
- **Intervallo minimo**: 5 minuti
- **Intervallo consigliato**: 15-30 minuti
- **Intervallo massimo**: 24 ore
- **Default**: 15 minuti

## Confronto con Azure Function

L'**Azure Function** rimane una valida alternativa quando sono necessarie personalizzazioni avanzate:

### Quando Preferire Azure Function

- Logica di trasformazione dati complessa e personalizzata
- Integrazione con sistemi aggiuntivi oltre a Azure Sentinel
- Requisiti di elaborazione dati in tempo reale molto specifici
- Necessità di controllo granulare su ogni aspetto del processo

### Svantaggi Azure Function

- **Sviluppo e Manutenzione**: Richiede competenze di sviluppo e manutenzione continua
- **Tempo di Setup**: 1-2 giorni per sviluppo, test e deployment
- **Costi**: Costi di sviluppo iniziale + costi Azure Function + costi di manutenzione
- **Complessità**: Gestione di errori, retry, logging, monitoring da implementare manualmente

### Configurazione Polling Azure Function

Con Azure Function hai maggiore flessibilità, ma con le stesse limitazioni strutturali:
- **Intervallo minimo raccomandato**: 5 minuti
- **Intervallo consigliato**: 5-15 minuti
- **Intervallo massimo consigliato**: 60 minuti

## ⚠️ Limite Strutturale Comune: Disponibilità Event Log Files

**IMPORTANTE**: Entrambe le soluzioni (CCF e Azure Function) sono soggette a un **limite strutturale imposto da Salesforce** che non può essere aggirato:

### Delay di Disponibilità Eventi

- **Event Log Files disponibili dopo**: 24-48 ore dalla generazione dell'evento
- Questo è un limite intrinseco della piattaforma Salesforce Event Monitoring
- Non dipende dalla soluzione di integrazione scelta (CCF o Azure Function)
- Non può essere ridotto o eliminato

### Implicazioni Pratiche

1. **Latenza Totale**:
   - Delay Salesforce: 24-48 ore
   - Latenza polling: 15-30 minuti (CCF) o 5-15 minuti (Function)
   - **Latenza totale**: 24-72 ore dall'evento alla disponibilità in Azure Sentinel

2. **Monitoraggio in Tempo Reale**:
   - Non è possibile ottenere monitoraggio in tempo reale degli eventi Salesforce
   - Gli eventi più recenti potrebbero non essere disponibili per 24-48 ore
   - Questo limite è accettabile per analisi di sicurezza e compliance, ma non per alerting in tempo reale

3. **Strategia di Polling**:
   - Il polling frequente (< 5 minuti) non migliora la disponibilità dei dati
   - Intervalli di 15-30 minuti sono ottimali per bilanciare latenza e consumo API
   - Polling più frequente aumenta solo i costi senza ridurre la latenza effettiva

### Limiti API Salesforce

Entrambe le soluzioni devono rispettare i limiti API di Salesforce:
- **Enterprise**: ~15.000 richieste/24h
- **Unlimited**: ~100.000 richieste/24h
- **Performance**: ~50.000 richieste/24h
- **Concurrent Requests**: Massimo 25 simultanee

## Raccomandazione Finale

Per la maggior parte dei casi d'uso, **raccomandiamo il CCF** perché:

1. **Setup rapido**: Operativo in meno di un'ora
2. **Zero manutenzione**: Gestito completamente da Microsoft
3. **Costi contenuti**: Nessun costo di sviluppo o manutenzione
4. **Affidabilità**: Gestione automatica di errori e retry
5. **Stesse prestazioni**: Il limite strutturale di 24-48 ore è identico per entrambe le soluzioni

L'Azure Function è consigliabile solo se:
- Hai requisiti di personalizzazione molto specifici che il CCF non può soddisfare
- Hai competenze di sviluppo disponibili per manutenzione continua
- Il budget permette costi di sviluppo e manutenzione

## Prossimi Passi

Se confermi la scelta del CCF, possiamo procedere con:
1. Configurazione della Connected App in Salesforce
2. Setup del connector CCF in Azure Sentinel
3. Configurazione del polling ottimale (15-30 minuti)
4. Test e validazione dell'integrazione

Resta inteso che, indipendentemente dalla soluzione scelta, il limite strutturale di 24-48 ore per la disponibilità degli Event Log Files è un vincolo di Salesforce che non può essere modificato.

Sono a disposizione per qualsiasi chiarimento o approfondimento.

Cordiali saluti,

[Nome]
[Ruolo]
[Contatti]

---

**Riferimenti Documentazione:**
- CCF: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/ccf/
- Azure Function: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/azure-function/
- Limitazioni Polling: https://fuscofabio.github.io/salesforce-sentinel-integration/implementation/ccf/#limitazioni-e-limiti-di-polling








