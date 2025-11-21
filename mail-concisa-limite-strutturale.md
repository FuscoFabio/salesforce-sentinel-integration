# Mail Concisa: Limite Strutturale Event Log Files

**Oggetto:** Integrazione Salesforce-Azure Sentinel: Limite Strutturale e Tempi

---

Gentile [Nome],

ti scrivo per chiarire un aspetto fondamentale dell'integrazione Salesforce-Azure Sentinel riguardo ai **tempi di disponibilità dei dati** e al **limite strutturale** che accomuna tutte le soluzioni.

## Tempi Focali

### Setup e Configurazione

- **CCF**: 30-60 minuti (configurazione grafica, zero codice)
- **Azure Function**: 1-2 giorni (sviluppo, test, deployment)

### Polling e Latenza

- **Intervallo polling minimo**: 5 minuti (per entrambe le soluzioni)
- **Intervallo polling consigliato**: 
  - CCF: 15-30 minuti
  - Azure Function: 5-15 minuti
- **Polling ogni 10 minuti**: Tecnicamente possibile con CCF, ma **non consigliato** (vedi sotto)
- **Latenza raccolta dati**: 15-30 minuti (CCF) o 5-15 minuti (Function)

## ⚠️ Limite Strutturale: Disponibilità Event Log Files

### Cosa Sono gli Event Log Files

Gli **Event Log Files** sono file aggregati che Salesforce genera attraverso un processo batch giornaliero. Contengono gli eventi di accesso (login, logout, API calls) in formato strutturato e ottimizzato.

### Il Vincolo Strutturale

**Sia il CCF che Azure Function** si collegano esclusivamente agli **Event Log Files API**, che hanno le seguenti caratteristiche:

- ✅ **Disponibilità**: Eventi disponibili dopo **24-48 ore** dalla generazione
- ✅ **Formato strutturato**: Dati pronti per analisi e reporting
- ✅ **Affidabilità**: Dati consolidati e validati da Salesforce

**Non possono** invece collegarsi a:
- ❌ **Log di Debug**: Disponibili in tempo reale ma non strutturati e non adatti per integrazione
- ❌ **API di Monitoraggio in Tempo Reale**: Permetterebbero controllo real-time ma non sono supportate per integrazione con SIEM

### Implicazioni

Questo significa che:
- **Non è possibile** ottenere monitoraggio in tempo reale (< 24 ore) degli eventi Salesforce
- La **latenza totale** è: 24-48 ore (Salesforce) + 15-30 minuti (polling) = **24-72 ore**
- Questo limite è **identico per CCF e Azure Function**, perché entrambe usano la stessa API

### ⚠️ Polling Ogni 10 Minuti: Possibile ma Inutile

**Domanda frequente**: "È possibile configurare il CCF per polling ogni 10 minuti per avere dati near real-time?"

**Risposta**: 
- ✅ **Tecnicamente possibile**: Il CCF supporta polling ogni 10 minuti (è > 5 minuti minimo)
- ❌ **Praticamente inutile**: Gli Event Log Files non sono disponibili prima di 24-48 ore

**Perché non ha senso**:
- Polling ogni 10 minuti interroga l'API ogni 10 minuti
- Ma gli Event Log Files contengono solo eventi di 24-48 ore fa
- Quindi ogni poll trova gli stessi dati (o nessun dato nuovo)
- **Risultato**: Aumento dei costi Azure senza migliorare la latenza effettiva

**Esempio pratico**:
- **Lunedì 10:00**: Evento login in Salesforce
- **Lunedì 10:10, 10:20, 10:30...**: Polling ogni 10 minuti → **Nessun dato disponibile** (evento non ancora in Event Log Files)
- **Martedì-Mercoledì**: Salesforce elabora il batch
- **Mercoledì 10:00**: Event Log File disponibile → Polling trova l'evento (24-48 ore dopo)

**Conclusione**: Polling ogni 10 minuti non porta a "near real-time" perché il limite strutturale di 24-48 ore rimane invariato. L'intervallo consigliato di 15-30 minuti è ottimale per bilanciare costi e latenza.

### Perché Non Usare Log di Debug o API Real-Time

- **Log di Debug**: Non strutturati, non scalabili, non adatti per integrazione SIEM
- **API Real-Time**: Non supportate da Salesforce per integrazione con sistemi esterni, solo per monitoraggio interno

## Raccomandazione

Per la maggior parte dei casi d'uso, **raccomandiamo il CCF** per:
- Setup rapido (30-60 minuti vs 1-2 giorni)
- Zero manutenzione
- Costi contenuti
- Stesse prestazioni (limite strutturale identico)

**Azure Function** è consigliabile solo se hai requisiti di personalizzazione avanzata (enrichment dati esterni, routing multi-destinazione, logica business complessa).

Sono a disposizione per approfondimenti.

Cordiali saluti,

[Nome]  
[Ruolo]  
[Contatti]

