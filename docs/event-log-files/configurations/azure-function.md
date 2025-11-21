# Azure Function (Event Log Files)

Soluzione basata su Azure Function per l'integrazione Salesforce-Azure Sentinel usando **Event Log Files API** con massima personalizzazione.

## Panoramica

Azure Function è la soluzione consigliata quando hai bisogno di controllo completo sul processo di integrazione e personalizzazione avanzata della logica di trasformazione dei dati.

## ⚠️ Approccio: Event Log Files API

**Questa soluzione usa Event Log Files API**, che ha le seguenti caratteristiche:

- ✅ **Copertura Completa**: Tutti gli eventi disponibili (LoginEvent, LogoutEvent, ApiEvent, Audit Trail)
- ✅ **Formato Strutturato**: Dati ottimizzati e validati
- ❌ **Incrementi orari**: I file vengono generati da Salesforce ogni ora e sono accessibili solo dopo la pubblicazione del blocco (vedi [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm))
- ❌ **Latenza**: 24-48 ore (limite strutturale Salesforce: il connettore può leggere i file solo quando Salesforce li rende disponibili)
- ✅ **Personalizzazione**: Controllo completo sulla logica

**Se hai bisogno di near real-time (< 24 ore)**, considera [Platform Events](../../platform-events/overview.md) invece.

## Caratteristiche

- **Massima Personalizzazione**: Controllo completo sulla logica di trasformazione
- **Scalabilità**: Gestione automatica del carico di lavoro
- **Costi Ottimizzati**: Paghi solo per l'esecuzione
- **Monitoraggio Integrato**: Log e metriche in Azure Monitor
- **Polling Configurabile**: 5-15 minuti (consigliato)

## Quando Usare Azure Function (Event Log Files)

**Scegli Azure Function se**:
- ✅ Hai bisogno di personalizzazioni avanzate che il CCF non supporta
- ✅ Vuoi controllo completo sulla logica di trasformazione
- ✅ Hai competenze di sviluppo
- ✅ La latenza di 24-72 ore è accettabile

**Non scegliere questa soluzione se**:
- ❌ Hai bisogno di near real-time (< 24 ore) → Usa [Platform Events](../../platform-events/overview.md)
- ❌ Vuoi setup semplice senza codice → Usa [CCF](ccf.md)

## Differenza con Platform Events

| Aspetto | Azure Function (Event Log Files) | Azure Function (Platform Events) |
|---------|----------------------------------|----------------------------------|
| **API Usata** | Event Log Files API | Platform Events (Event Bus) |
| **Latenza** | 24-48 ore | < 1 minuto |
| **Copertura** | Completa | Limitata |
| **Sviluppo Salesforce** | Non richiesto | Richiesto (Apex) |
| **Complessità** | Media | Alta |

## Implementazione

Vedi la guida completa: [Implementazione Azure Function](../implementation/azure-function.md)

## Casi d'Esempio

Vedi esempi pratici: [Esempio Azure Function](../examples/azure-function-example.md)

## Link Utili

- [Implementazione Azure Function](../implementation/azure-function.md)
- [Platform Events (Near Real-Time)](../../platform-events/overview.md)
- [Documentazione Azure Functions](https://learn.microsoft.com/azure/azure-functions/)
- [Azure Function Pricing](https://azure.microsoft.com/pricing/details/functions/)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

