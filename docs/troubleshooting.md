# Troubleshooting

Guida per risolvere i problemi comuni nell'integrazione Salesforce-Azure Sentinel.

## Problemi Comuni

### Nessun Dato in Azure Sentinel

**Sintomi**: Non vedi eventi Salesforce in Log Analytics.

**Possibili Cause e Soluzioni**:

1. **Event Monitoring non attivo abbastanza a lungo**
   - Event Monitoring richiede 24-48 ore per generare eventi
   - **Soluzione**: Attendi e verifica dopo 48 ore

2. **Credenziali OAuth non valide**
   - Consumer Key o Secret errati
   - **Soluzione**: Verifica le credenziali nella Connected App

3. **Connector/Function/Logic App non configurato correttamente**
   - Configurazione incompleta o errata
   - **Soluzione**: Rivedi la configurazione passo per passo

4. **Permessi insufficienti**
   - L'utente non ha permessi per Event Log Files
   - **Soluzione**: Verifica Permission Sets e profili

5. **Problemi di rete/firewall**
   - IP bloccati o restrizioni di rete
   - **Soluzione**: Verifica Network Access in Salesforce e range IP Azure

### Errori di Autenticazione

**Sintomi**: Errori 401 Unauthorized o problemi di login.

**Possibili Cause e Soluzioni**:

1. **Token OAuth scaduto**
   - I token hanno una scadenza
   - **Soluzione**: Implementa refresh token automatico

2. **Consumer Secret errato**
   - Secret copiato incorrettamente
   - **Soluzione**: Rigenera il Consumer Secret se necessario

3. **Callback URL non corrispondente**
   - URL nella Connected App non corrisponde
   - **Soluzione**: Verifica e aggiorna il Callback URL

4. **OAuth Scopes insufficienti**
   - Scopes mancanti nella Connected App
   - **Soluzione**: Aggiungi gli scopes necessari

### Dati Incompleti o Mancanti

**Sintomi**: Solo alcuni eventi vengono ricevuti, altri mancano.

**Possibili Cause e Soluzioni**:

1. **Filtri troppo restrittivi**
   - Filtri che escludono eventi
   - **Soluzione**: Rivedi i filtri nella soluzione

2. **Eventi non ancora disponibili**
   - Event Monitoring ha delay
   - **Soluzione**: Verifica la data degli eventi richiesti

3. **Rate Limits raggiunti**
   - Troppe richieste API
   - **Soluzione**: Implementa retry con backoff esponenziale

4. **Errori durante il processing**
   - Errori silenziosi nella trasformazione
   - **Soluzione**: Controlla i log della soluzione

### Errori nella Function/Logic App

**Sintomi**: Errori nelle esecuzioni della Function o Logic App.

**Possibili Cause e Soluzioni**:

1. **Application Settings mancanti**
   - Variabili d'ambiente non configurate
   - **Soluzione**: Verifica tutte le Application Settings

2. **Timeout delle richieste**
   - Richieste che impiegano troppo tempo
   - **Soluzione**: Ottimizza il codice o aumenta il timeout

3. **Errori di parsing JSON**
   - Formato dati non valido
   - **Soluzione**: Verifica lo schema dei dati

4. **Problemi di connessione**
   - Problemi di rete temporanei
   - **Soluzione**: Implementa retry logic robusto

### Costi Elevati

**Sintomi**: Costi Azure più alti del previsto.

**Possibili Cause e Soluzioni**:

1. **Troppa ingestione dati**
   - Volume eventi superiore alle aspettative
   - **Soluzione**: Filtra eventi non necessari, ottimizza la frequenza

2. **Function eseguita troppo spesso**
   - Timer trigger con frequenza eccessiva
   - **Soluzione**: Riduci la frequenza di esecuzione

3. **Retention troppo lunga**
   - Dati conservati più a lungo del necessario
   - **Soluzione**: Riduci il periodo di retention

## Diagnostica

### Verifiche Step-by-Step

1. **Verifica Event Monitoring in Salesforce**
   ```
   Setup → Event Monitoring → Event Log Files
   ```
   - Controlla che ci siano eventi recenti
   - Verifica i tipi di evento disponibili

2. **Verifica Connected App**
   ```
   Setup → App Manager → [Your Connected App]
   ```
   - Verifica che sia attiva
   - Controlla OAuth Settings
   - Verifica Callback URL

3. **Verifica Credenziali**
   - Testa le credenziali con una chiamata API manuale
   - Usa Postman o curl per verificare

4. **Verifica Log Analytics**
   ```kql
   Salesforce_CL
   | take 10
   ```
   - Esegui query per verificare dati
   - Controlla schema e campi

5. **Verifica Function/Logic App Logs**
   - Controlla Application Insights
   - Verifica errori e eccezioni
   - Controlla metriche di esecuzione

### Query di Diagnostica

**Verifica ultimi eventi**:
```kql
Salesforce_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc
| take 10
```

**Conta eventi per tipo**:
```kql
Salesforce_CL
| where TimeGenerated > ago(24h)
| summarize count() by EventType_s
```

**Verifica errori**:
```kql
Salesforce_CL
| where TimeGenerated > ago(24h)
| where isnotempty(Error_s)
| project TimeGenerated, Error_s, UserName_s
```

## Log e Monitoraggio

### Application Insights

Configura Application Insights per:
- Tracciare esecuzioni
- Monitorare errori
- Analizzare performance
- Configurare alert

### Log di Salesforce

Controlla i log in Salesforce:
- Setup → Debug Logs
- Setup → Event Monitoring → Event Log Files

### Log di Azure

Controlla i log in Azure:
- Function App → Log stream
- Logic App → Run history
- Log Analytics → Logs

## Supporto

Se il problema persiste:

1. Raccogli informazioni:
   - Screenshot degli errori
   - Log rilevanti
   - Configurazione (senza credenziali)

2. Consulta:
   - [Link Utili](references/links.md)
   - [API Reference](references/api.md)
   - Community e forum

3. Verifica:
   - Documentazione ufficiale
   - Changelog e aggiornamenti
   - Known issues

## Best Practices per Prevenire Problemi

1. **Monitoraggio Proattivo**: Configura alert per errori
2. **Logging Completo**: Logga tutte le operazioni importanti
3. **Test Regolari**: Verifica periodicamente che l'integrazione funzioni
4. **Documentazione**: Mantieni documentazione aggiornata della configurazione
5. **Backup**: Mantieni backup delle configurazioni
6. **Versioning**: Usa versioning per il codice delle Function

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5)
- [Azure Functions Diagnostics](https://learn.microsoft.com/azure/azure-functions/functions-monitoring)
- [Microsoft Sentinel Troubleshooting](https://learn.microsoft.com/azure/sentinel/troubleshooting)

