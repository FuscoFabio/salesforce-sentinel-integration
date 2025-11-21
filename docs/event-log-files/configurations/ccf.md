# CodeLess Connector Framework (CCF)

Soluzione code-less per integrazione Salesforce-Azure Sentinel usando **Event Log Files API**.

## Panoramica

Il CodeLess Connector Framework (CCF) è la soluzione raccomandata per setup rapido senza codice. Utilizza **Event Log Files API** per recuperare eventi da Salesforce.

## ⚠️ Approccio: Event Log Files API

**Questa soluzione usa Event Log Files API**, che ha le seguenti caratteristiche:

- ✅ **Copertura Completa**: Tutti gli eventi disponibili (LoginEvent, LogoutEvent, ApiEvent, Audit Trail)
- ✅ **Formato Strutturato**: Dati ottimizzati e validati
- ❌ **Incrementi orari**: Salesforce genera i log una volta per ogni ora e li rende disponibili solo dopo l'elaborazione del blocco (vedi [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm))
- ❌ **Latenza effettiva**: 24-48 ore prima che i dati arrivino su Sentinel, anche se il polling viene eseguito più spesso
- ✅ **Setup Semplice**: Configurazione grafica, zero codice

**Se hai bisogno di near real-time (< 24 ore)**, considera [Platform Events](../../platform-events/overview.md) invece.

## Caratteristiche

- **Setup Rapido**: 30-60 minuti (configurazione grafica)
- **Zero Manutenzione**: Gestito completamente da Microsoft
- **Costi Contenuti**: Solo costi ingestione dati
- **Affidabilità**: Gestione automatica errori e retry
- **Polling Ottimizzato**: 15-30 minuti (configurabile)

## Quando Usare CCF

**Scegli CCF se**:
- ✅ La latenza di 24-72 ore è accettabile
- ✅ Hai bisogno di copertura completa (incluso Audit Trail)
- ✅ Vuoi setup semplice senza codice
- ✅ Budget limitato
- ✅ Zero manutenzione desiderata

**Non scegliere CCF se**:
- ❌ Hai bisogno di monitoraggio near real-time (< 24 ore)
- ❌ Hai requisiti di personalizzazione avanzata che CCF non supporta

## Implementazione

Vedi la guida completa: [Implementazione CCF](../implementation/ccf.md)

## Casi d'Esempio

Vedi esempi pratici: [Esempio CCF](../examples/ccf-example.md)

## Link Utili

- [Implementazione CCF](../implementation/ccf.md)
- [Documentazione Microsoft CCF](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)
- [Platform Events (Near Real-Time)](../../platform-events/overview.md) - Alternativa per real-time

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [CodeLess Connector Framework (Microsoft Sentinel)](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

