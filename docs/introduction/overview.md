# Panoramica

## Cos'è questa integrazione?

Questa integrazione permette di trasferire automaticamente i log di accesso generati da Salesforce verso Azure Sentinel, creando un'unica piattaforma centralizzata per il monitoraggio della sicurezza.

## Perché integrare Salesforce con Azure Sentinel?

### Vantaggi

- **Visibilità Centralizzata**: Tutti i log di accesso in un'unico posto
- **Analisi Avanzata**: Query KQL per identificare pattern sospetti
- **Alerting Automatico**: Notifiche per accessi anomali
- **Compliance**: Tracciamento completo degli accessi per audit
- **Correlazione Eventi**: Integrare con altri log di sicurezza

## Cosa viene monitorato?

### Eventi Salesforce Supportati

- **LoginEvent**: Accessi utente a Salesforce
- **LogoutEvent**: Disconnessioni
- **ApiEvent**: Chiamate API (estendibile)
- Altri eventi configurabili

### Dati Inclusi

- Timestamp accesso
- Username e User ID
- Indirizzo IP
- Browser e piattaforma
- Tipo di login
- Geolocalizzazione (se disponibile)

## Soluzioni Disponibili

Il progetto offre **5 soluzioni** diverse per soddisfare ogni esigenza:

1. **CodeLess Connector Framework (CCF)** - Setup rapido, zero manutenzione
2. **Azure Function** - Massima personalizzazione
3. **Azure Logic App** - Low-code visuale
4. **Syslog + Azure Monitor Agent** - Per infrastrutture esistenti
5. **Third-party SIEM Connector** - Per soluzioni enterprise

[Vedi confronto completo →](../solutions/overview.md)

## Prerequisiti

### Salesforce
- Licenza Enterprise, Unlimited o Performance Edition
- Event Monitoring abilitato
- Permessi per creare Connected App

### Azure
- Sottoscrizione Azure attiva
- Azure Sentinel Workspace
- Permessi per creare risorse Azure

## Prossimi Passi

1. [Scegli una soluzione](../solutions/overview.md)
2. [Configura Salesforce](../setup/salesforce.md)
3. [Configura Azure Sentinel](../setup/azure-sentinel.md)
4. [Segui il Quick Start](../setup/quick-start.md)

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)

