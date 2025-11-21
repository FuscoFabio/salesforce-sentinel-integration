# Integrazione Salesforce - Azure Sentinel

Benvenuto nella documentazione completa per integrare i log di accesso di Salesforce con Azure Sentinel.

## Panoramica

Questo progetto fornisce soluzioni complete per trasferire automaticamente i log di accesso generati da Salesforce verso Azure Sentinel, creando un'unica piattaforma centralizzata per il monitoraggio della sicurezza.

## ⚠️ Due Approcci Principali

Prima di scegliere una soluzione, è fondamentale comprendere la differenza tra i due approcci di integrazione:

### 1. Event Log Files API (Latenza 24-48 ore)

**Caratteristiche**:
- ✅ **Copertura Completa**: Tutti gli eventi disponibili (incluso Audit Trail)
- ✅ **Setup Semplice**: Soluzioni code-less disponibili
- ✅ **Zero Sviluppo**: Non richiede codice
- ❌ **Incrementi orari**: Salesforce pubblica i log in blocchi orari come da [Event Log File Hourly Overview](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm)
- ❌ **Latenza**: 24-48 ore (limite strutturale: i connettori possono leggere solo i file già pubblicati)

**Soluzioni Disponibili**:
- [CCF](event-log-files/configurations/ccf.md) ⭐ Consigliato - Setup rapido, zero manutenzione
- [Azure Function](event-log-files/configurations/azure-function.md) - Massima personalizzazione
- [Logic App](event-log-files/configurations/logic-app.md) - Approccio low-code visuale

[Vedi panoramica Event Log Files →](event-log-files/overview.md) | [Confronto soluzioni →](event-log-files/solutions-comparison.md)

### 2. Platform Events / Event Bus (Near Real-Time)

**Caratteristiche**:
- ✅ **Latenza**: < 1 minuto (near real-time)
- ✅ **Tempo Reale**: Eventi disponibili immediatamente
- ❌ **Copertura Limitata**: Non tutti gli eventi disponibili
- ❌ **Complessità**: Richiede sviluppo custom (Apex + Azure)

**Configurazioni Disponibili**:
- [Webhook HTTP](platform-events/configurations/webhook-http.md) - Più semplice
- [Azure Event Hub](platform-events/configurations/event-hub.md) ⭐ Consigliato - Scalabile
- [CometD Streaming](platform-events/configurations/cometd-streaming.md) - WebSocket

[Vedi panoramica Platform Events →](platform-events/overview.md) | [Confronto configurazioni →](platform-events/configurations-comparison.md)

### Confronto Rapido

| Aspetto | Event Log Files | Platform Events |
|---------|----------------|-----------------|
| **Latenza** | 24-48 ore | < 1 minuto |
| **Copertura** | Completa (100%) | Limitata (~30-40%) |
| **Setup** | Semplice | Complesso |
| **Sviluppo** | Non richiesto | Richiesto |
| **Audit Trail** | ✅ | ❌ |

[Vedi confronto completo →](introduction/approaches-comparison.md)

## Inizia Qui

### 🚀 Quick Start
Vuoi iniziare subito? Segui la [guida rapida](setup/quick-start.md) per configurare l'integrazione in pochi minuti.

### 📚 Documentazione

- **[Introduzione](introduction/overview.md)** - Scopri cos'è questa integrazione e perché è utile
- **[Confronto Approcci](introduction/approaches-comparison.md)** - Confronto dettagliato Event Log Files vs Platform Events
- **[Architettura](introduction/architecture.md)** - Architettura delle soluzioni
- **[Setup](setup/quick-start.md)** - Configura Salesforce e Azure Sentinel

## Struttura Documentazione

### Event Log Files API (24-48h)

- **[Panoramica](event-log-files/overview.md)** - Caratteristiche e funzionamento
- **[Confronto Soluzioni](event-log-files/solutions-comparison.md)** - CCF, Azure Function, Logic App
- **[Configurazioni](event-log-files/configurations/)** - Guide di configurazione
- **[Implementazione](event-log-files/implementation/)** - Guide tecniche dettagliate
- **[Casi d'Esempio](event-log-files/examples/)** - Esempi pratici completi

### Platform Events / Event Bus (Near Real-Time)

- **[Panoramica](platform-events/overview.md)** - Caratteristiche e funzionamento
- **[Confronto Configurazioni](platform-events/configurations-comparison.md)** - Webhook, Event Hub, CometD
- **[Configurazioni](platform-events/configurations/)** - Guide di configurazione
- **[Implementazione](platform-events/implementation/)** - Guide tecniche dettagliate
- **[Casi d'Esempio](platform-events/examples/)** - Esempi pratici completi

### SIEM - Azure Sentinel

- **[Campi Real-Time](siem/real-time-fields.md)** ⭐ - Guida completa ai campi estraibili in real-time per SIEM

## Vantaggi Principali

- ✅ **Visibilità Centralizzata**: Tutti i log di accesso in un'unico posto
- ✅ **Analisi Avanzata**: Query KQL per identificare pattern sospetti
- ✅ **Alerting Automatico**: Notifiche per accessi anomali
- ✅ **Compliance**: Tracciamento completo degli accessi per audit
- ✅ **Correlazione Eventi**: Integrare con altri log di sicurezza

## Prerequisiti

### Salesforce
- Licenza Enterprise, Unlimited o Performance Edition
- Event Monitoring abilitato
- Permessi per creare Connected App

### Azure
- Sottoscrizione Azure attiva
- Azure Sentinel Workspace
- Permessi per creare risorse Azure

## Link Utili

- 📖 [Documentazione Completa](introduction/overview.md)
- 🔧 [API Reference](references/api.md)
- 🔗 [Link Utili](references/links.md)
- 🐛 [Troubleshooting](troubleshooting.md)

## Repository

- **GitHub**: [salesforce-sentinel-integration](https://github.com/FuscoFabio/salesforce-sentinel-integration)
- **Documentazione**: [https://FuscoFabio.github.io/salesforce-sentinel-integration/](https://FuscoFabio.github.io/salesforce-sentinel-integration/)

---

**Pronto per iniziare?** Inizia con il [Quick Start](setup/quick-start.md) o esplora le [soluzioni disponibili](solutions/overview.md).

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)

