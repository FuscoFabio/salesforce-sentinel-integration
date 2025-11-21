# Quick Start

Guida rapida per iniziare con l'integrazione Salesforce-Azure Sentinel.

## Panoramica

Questa guida ti aiuterà a configurare l'integrazione in pochi passaggi. Il tempo stimato è di 30-60 minuti.

## Passo 1: Scegliere la Soluzione

Scegli la soluzione più adatta alle tue esigenze:

- **CCF**: Setup più rapido, zero codice (consigliato per iniziare)
- **Azure Function**: Massima personalizzazione
- **Logic App**: Approccio low-code visuale

Vedi [Panoramica Soluzioni](../solutions/overview.md) per il confronto completo.

## Passo 2: Configurare Salesforce

1. Abilita Event Monitoring in Salesforce
2. Crea una Connected App
3. Ottieni Consumer Key e Consumer Secret
4. Verifica che Event Monitoring generi eventi

**Tempo stimato**: 15-20 minuti

Vedi [Configurazione Salesforce](./salesforce.md) per i dettagli completi.

## Passo 3: Configurare Azure Sentinel

1. Crea un Log Analytics Workspace
2. Abilita Azure Sentinel sul workspace
3. Configura il connector o la soluzione scelta
4. Verifica la ricezione dei dati

**Tempo stimato**: 10-15 minuti

Vedi [Configurazione Azure Sentinel](./azure-sentinel.md) per i dettagli completi.

## Passo 4: Verificare l'Integrazione

### Verifica Dati in Azure Sentinel

1. Apri Azure Sentinel → **Logs**
2. Esegui la query:
   ```kql
   Salesforce_CL
   | take 10
   | project TimeGenerated, UserName_s, EventType_s, SourceIP_s
   ```
3. Verifica che i dati siano presenti

### Verifica Eventi Recenti

```kql
Salesforce_CL
| where TimeGenerated > ago(1h)
| summarize count() by EventType_s
| render columnchart
```

## Passo 5: Configurare Query e Alert (Opzionale)

1. Crea query KQL per analisi specifiche
2. Configura regole di allerta per eventi sospetti
3. Crea dashboard per il monitoraggio

Vedi [Query KQL](../implementation/kql-queries.md) per esempi.

## Checklist Completa

- [ ] Event Monitoring abilitato in Salesforce
- [ ] Connected App creata con OAuth
- [ ] Credenziali (Consumer Key/Secret) salvate
- [ ] Log Analytics Workspace creato
- [ ] Azure Sentinel abilitato
- [ ] Connector/Soluzione configurata
- [ ] Dati visibili in Log Analytics
- [ ] Query di verifica eseguite con successo

## Troubleshooting Rapido

### Nessun dato visibile

1. Verifica che Event Monitoring sia attivo da almeno 24-48 ore
2. Controlla le credenziali OAuth
3. Verifica i log della soluzione (Function/Logic App)
4. Controlla i permessi e la configurazione di rete

### Errori di autenticazione

1. Verifica Consumer Key e Secret
2. Controlla Callback URL nella Connected App
3. Verifica OAuth Scopes configurati
4. Controlla che la Connected App sia attiva

### Dati incompleti

1. Verifica che Event Monitoring includa gli eventi necessari
2. Controlla i filtri nella soluzione
3. Verifica i limiti API di Salesforce

## Prossimi Passi

- [Configurare query KQL avanzate](../implementation/kql-queries.md)
- [Gestire Network e Sicurezza](../implementation/network-sicurezza.md)
- [Personalizzare l'implementazione](../implementation/azure-function.md)
- [Risolvere problemi comuni](../troubleshooting.md)

## Supporto

Per problemi o domande:
- Consulta la sezione [Troubleshooting](../troubleshooting.md)
- Verifica i [Link Utili](../references/links.md)
- Controlla la [Documentazione Microsoft](https://learn.microsoft.com/azure/sentinel/)

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5)
- [Microsoft Sentinel Quickstart](https://learn.microsoft.com/azure/sentinel/quickstart-onboard)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

