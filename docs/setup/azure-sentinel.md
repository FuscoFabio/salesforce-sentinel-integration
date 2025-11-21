# Configurazione Azure Sentinel

La configurazione di Azure Sentinel **varia in base alla soluzione** scelta.

## Prerequisiti

- Sottoscrizione Azure attiva
- Permessi di Contributor o Owner sulla sottoscrizione
- Log Analytics Workspace esistente o da creare
- Azure Sentinel abilitato sul workspace

## Passo 1: Creare Log Analytics Workspace

1. Accedi al [Portale Azure](https://portal.azure.com)
2. Cerca "Log Analytics workspaces"
3. Clicca su **Create**
4. Compila i campi:
   - **Subscription**: Seleziona la sottoscrizione
   - **Resource Group**: Crea o seleziona un resource group
   - **Name**: Nome del workspace (es. "salesforce-sentinel-ws")
   - **Region**: Seleziona una regione
5. Clicca su **Review + Create** → **Create**

## Passo 2: Abilitare Azure Sentinel

1. Nel portale Azure, cerca "Azure Sentinel"
2. Clicca su **Create**
3. Seleziona il Log Analytics Workspace creato
4. Clicca su **Add**

## Passo 3: Configurazione per Soluzione

### Per CCF (CodeLess Connector Framework)

1. In Azure Sentinel, vai a **Data connectors**
2. Cerca "Salesforce" o il connector specifico
3. Segui la procedura guidata del connector
4. Configura le credenziali Salesforce ottenute dalla configurazione
5. Abilita il connector

### Per Azure Function

1. Crea un'Azure Function App (vedi [Implementazione Azure Function](../implementation/azure-function.md))
2. Configura Application Settings con:
   - Credenziali Salesforce
   - Workspace ID e Key di Log Analytics
3. Configura la Function per inviare dati a Log Analytics

### Per Logic App

1. Crea un'Azure Logic App
2. Configura i connettori Salesforce e Azure Monitor
3. Imposta il workflow per l'integrazione
4. Configura le credenziali necessarie

## Passo 4: Verificare Ricezione Dati

1. In Azure Sentinel, vai a **Logs**
2. Esegui una query per verificare i dati:
   ```kql
   Salesforce_CL
   | take 10
   ```
3. Se non vedi dati, verifica:
   - Configurazione del connector/function/logic app
   - Credenziali e permessi
   - Rete e firewall

## Passo 5: Configurare Tabelle Custom (se necessario)

Se usi Azure Function o Logic App, potresti dover creare tabelle custom:

1. Vai a **Log Analytics workspace** → **Tables**
2. Crea una tabella custom se necessario
3. Configura lo schema dei dati

## Configurazioni Avanzate

### Data Retention

1. Vai a **Log Analytics workspace** → **Usage and estimated costs**
2. Configura la retention dei dati (default 30 giorni, fino a 2 anni)

### Network Security

- Configura **Private Endpoints** se necessario
- Restringi l'accesso tramite **Network Access Control**
- Configura **IP Restrictions** se applicabile

### Cost Management

- Monitora l'ingestione dati in **Usage and estimated costs**
- Configura **Data Collection Rules** per ottimizzare i costi
- Considera **Commitment Tiers** per volumi elevati

## Link Utili

- [Documentazione Azure Sentinel](https://learn.microsoft.com/azure/sentinel/)
- [Log Analytics Workspace](https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-workspace-overview)
- [Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)

## Fonti

- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [Azure Monitor Log Analytics Workspace](https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-workspace-overview)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

