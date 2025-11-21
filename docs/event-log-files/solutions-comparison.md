# Confronto Soluzioni Event Log Files API

Confronto dettagliato di tutte le soluzioni disponibili per integrare Event Log Files API con Azure Sentinel.

## Panoramica Soluzioni

Tre soluzioni principali sono disponibili per integrare Event Log Files API:

> ℹ️ **Limite comune (documentazione ufficiale Salesforce)**  
> Tutte queste soluzioni consumano gli **Event Log Files** generati in blocchi orari, come descritto da Salesforce nella [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm). Anche con polling aggressivo, i log risultano interrogabili in Sentinel solo dopo 24-48 ore dalla generazione.

1. **CCF (CodeLess Connector Framework)** ⭐ Consigliato
2. **Azure Function**
3. **Azure Logic App**

## Tabella Confronto Completa

| Aspetto | CCF | Azure Function | Logic App |
|---------|-----|----------------|-----------|
| **Setup Time** | 30-60 min | 1-2 giorni | 30-60 min |
| **Complessità Setup** | Bassa | Media-Alta | Bassa |
| **Codice Richiesto** | ❌ No | ✅ Sì | ❌ No |
| **Manutenzione** | Zero | Media-Alta | Bassa |
| **Costi Setup** | Basso | Medio | Medio |
| **Costi Operativi** | Basso | Medio | Medio |
| **Personalizzazione** | Limitata | Alta | Media |
| **Polling Intervallo** | 15-30 min | 5-15 min | 15-30 min |
| **Gestione Errori** | Automatica | Manuale | Semi-automatica |
| **Scalabilità** | Alta | Alta | Media-Alta |
| **Affidabilità** | Alta | Media-Alta | Media-Alta |
| **Network Security** | Private Link | Private Endpoints | ISE |
| **Best For** | Setup rapido | Personalizzazione | Low-code |

## Dettaglio Soluzioni

### 1. CCF (CodeLess Connector Framework) ⭐

**Descrizione**: Soluzione code-less gestita da Microsoft, configurabile tramite interfaccia grafica.

#### Vantaggi

- ✅ **Zero Codice**: Configurazione completamente grafica
- ✅ **Zero Manutenzione**: Gestito completamente da Microsoft
- ✅ **Setup Rapido**: 30-60 minuti
- ✅ **Affidabilità**: Gestione automatica errori e retry
- ✅ **Polling Ottimizzato**: 15-30 minuti (configurabile)
- ✅ **Private Link**: Supporto nativo per Azure Private Link
- ✅ **Costi Contenuti**: Solo costi ingestione dati

#### Svantaggi

- ❌ **Personalizzazione Limitata**: Formato dati predefinito
- ❌ **Configurazione Fissa**: Opzioni limitate
- ❌ **Dipendenze Microsoft**: Gestito da terze parti

#### Quando Usare

- ✅ Setup rapido senza sviluppo
- ✅ Zero manutenzione desiderata
- ✅ Requisiti standard (90% dei casi)
- ✅ Budget limitato
- ✅ Team senza competenze di sviluppo

#### Quando NON Usare

- ❌ Personalizzazioni avanzate richieste
- ❌ Trasformazioni dati complesse
- ❌ Integrazione con altri sistemi

[Vedi Configurazione CCF →](configurations/ccf.md) | [Vedi Implementazione →](implementation/ccf.md) | [Vedi Esempio →](examples/ccf-example.md)

---

### 2. Azure Function

**Descrizione**: Soluzione serverless personalizzabile con controllo completo sulla logica.

#### Vantaggi

- ✅ **Personalizzazione Completa**: Controllo totale sulla logica
- ✅ **Scalabilità**: Gestione automatica del carico
- ✅ **Polling Flessibile**: 5-15 minuti (configurabile)
- ✅ **Integrazione**: Facile integrazione con altri sistemi
- ✅ **Costi Ottimizzati**: Paghi solo per l'esecuzione
- ✅ **Private Endpoints**: Supporto VNet Integration

#### Svantaggi

- ❌ **Sviluppo Richiesto**: Codice necessario
- ❌ **Manutenzione**: Gestione continua codice
- ❌ **Setup Complesso**: 1-2 giorni di sviluppo
- ❌ **Gestione Errori**: Implementazione manuale

#### Quando Usare

- ✅ Personalizzazioni avanzate necessarie
- ✅ Trasformazioni dati complesse
- ✅ Integrazione con altri sistemi
- ✅ Controllo completo richiesto
- ✅ Team con competenze di sviluppo

#### Quando NON Usare

- ❌ Setup rapido necessario
- ❌ Zero manutenzione desiderata
- ❌ Requisiti standard (usa CCF)

[Vedi Configurazione Azure Function →](configurations/azure-function.md) | [Vedi Implementazione →](implementation/azure-function.md) | [Vedi Esempio →](examples/azure-function-example.md)

---

### 3. Azure Logic App

**Descrizione**: Soluzione low-code visuale con workflow configurabile tramite designer.

#### Vantaggi

- ✅ **Low-Code**: Configurazione visuale
- ✅ **Setup Rapido**: 30-60 minuti
- ✅ **Workflow Visuale**: Design grafico del flusso
- ✅ **Connettori Integrati**: Connettori nativi Salesforce e Azure
- ✅ **Template**: Template predefiniti disponibili
- ✅ **ISE Support**: Integration Service Environment per sicurezza

#### Svantaggi

- ❌ **Personalizzazione Limitata**: Rispetto ad Azure Function
- ❌ **Costi**: Più costoso di Azure Function per carichi elevati
- ❌ **Performance**: Meno performante di Azure Function
- ❌ **Debug**: Più difficile debug rispetto a codice

#### Quando Usare

- ✅ Preferenza per approccio visuale
- ✅ Team senza competenze di sviluppo
- ✅ Workflow complessi con logica condizionale
- ✅ Integrazione con altri connettori Azure

#### Quando NON Usare

- ❌ Performance critiche
- ❌ Personalizzazioni molto avanzate
- ❌ Budget limitato (usa CCF)

[Vedi Configurazione Logic App →](configurations/logic-app.md) | [Vedi Implementazione →](implementation/logic-app.md) | [Vedi Esempio →](examples/logic-app-example.md)

## Confronto Configurazioni Network

| Soluzione | Approccio Consigliato | Alternativa |
|-----------|----------------------|-------------|
| **CCF** | Azure Private Link | Range IP Pubblici |
| **Azure Function** | Private Endpoints + VNet | Range IP Pubblici |
| **Logic App** | Integration Service Environment (ISE) | Range IP Pubblici |

[Vedi dettagli Network e Sicurezza →](../implementation/network-sicurezza.md)

## Confronto Polling

| Soluzione | Intervallo Minimo | Intervallo Consigliato | Intervallo Massimo |
|-----------|------------------|------------------------|-------------------|
| **CCF** | 15 min | 15-30 min | 60 min |
| **Azure Function** | 1 min | 5-15 min | 60 min |
| **Logic App** | 1 min | 15-30 min | 60 min |

**Nota**: Polling più frequente non riduce la latenza di 24-48 ore degli Event Log Files.

## Confronto Costi (Stima Mensile)

### Scenario: 100.000 eventi/giorno

| Soluzione | Setup | Operativo | Totale |
|-----------|-------|-----------|--------|
| **CCF** | $0 | $50-100 | $50-100 |
| **Azure Function** | $500-1000 | $30-80 | $530-1080 |
| **Logic App** | $200-500 | $50-150 | $250-650 |

*Stime indicative, costi reali dipendono da volume e configurazione*

## Decision Tree

```
Hai bisogno di personalizzazione avanzata?
├─ NO → Hai bisogno di zero manutenzione?
│   ├─ SÌ → CCF ⭐
│   └─ NO → Preferisci approccio visuale?
│       ├─ SÌ → Logic App
│       └─ NO → CCF ⭐
└─ SÌ → Hai competenze di sviluppo?
    ├─ SÌ → Azure Function
    └─ NO → Logic App
```

## Raccomandazioni

### Per il 90% dei Casi d'Uso

**Usa CCF** - Setup rapido, zero manutenzione, costi contenuti.

### Per Personalizzazioni Avanzate

**Usa Azure Function** - Controllo completo, massima flessibilità.

### Per Approccio Low-Code

**Usa Logic App** - Workflow visuale, connettori integrati.

## Prossimi Passi

1. **Scegli una soluzione** basata sul confronto
2. **Consulta la configurazione** specifica: [Configurazioni](configurations/)
3. **Segui la guida di implementazione**: [Implementazione](implementation/)
4. **Vedi un caso d'esempio**: [Casi d'Esempio](examples/)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [CodeLess Connector Framework (Microsoft Sentinel)](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)


