# Implementazione CCF

Guida completa passo-passo per implementare l'integrazione Salesforce-Azure Sentinel usando il CodeLess Connector Framework (CCF).

## Panoramica

Il CodeLess Connector Framework (CCF) è la soluzione più semplice per integrare Salesforce con Azure Sentinel. Non richiede codice, solo configurazione tramite interfaccia grafica.

## Architettura

```
Salesforce Event Monitoring
    ↓
CCF Connector (Azure Sentinel)
    ↓
Log Analytics Workspace
    ↓
Azure Sentinel
```

## Prerequisiti

- Sottoscrizione Azure attiva
- Azure Sentinel Workspace configurato
- Licenza Salesforce Enterprise, Unlimited o Performance Edition
- Event Monitoring abilitato in Salesforce
- Connected App creata in Salesforce con OAuth
- Consumer Key e Consumer Secret di Salesforce

## Caso d'Esempio Completo

### Scenario
Un'organizzazione vuole monitorare tutti gli accessi a Salesforce per:
- Rilevare accessi sospetti
- Tracciare accessi da IP non usuali
- Monitorare attività fuori orario
- Generare alert per tentativi di login falliti

### Passo 1: Preparazione Salesforce

#### 1.1 Abilitare Event Monitoring

1. Accedi a Salesforce come amministratore
2. Vai a **Setup** → Cerca "Event Monitoring"
3. Vai a **Event Monitoring Settings**
4. Abilita **Event Monitoring** se non già attivo
5. Verifica che **Event Log Files** sia abilitato

#### 1.2 Creare Connected App

1. Vai a **Setup** → **App Manager**
2. Clicca su **New Connected App**
3. Compila i campi:
   ```
   Connected App Name: Azure Sentinel Integration
   API Name: Azure_Sentinel_Integration
   Contact Email: admin@example.com
   ```
4. Abilita **Enable OAuth Settings**
5. Configura **Callback URL**: 
   ```
   https://login.microsoftonline.com/common/oauth2/nativeclient
   ```
   (Questo sarà aggiornato dopo la configurazione del connector)
6. Seleziona **OAuth Scopes**:
   - `Manage user data via APIs (api)`
   - `Perform requests on your behalf at any time (refresh_token, offline_access)`
   - `Access the identity URL service (id, profile, email, address, phone)`
7. Abilita **Require Secret for Web Server Flow**
8. Salva e attendi 2-5 minuti per la propagazione

#### 1.3 Ottenere Credenziali

1. Vai alla Connected App appena creata
2. Clicca su **Manage** → **Edit Policies**
3. Configura:
   - **Permitted Users**: "All users may self-authorize"
   - **IP Relaxation**: 
     - Se usi **Private Endpoints**: "Relax IP restrictions" (non necessario)
     - Se usi **Range IP pubblici**: "Enforce IP restrictions" e configura Trusted IP Ranges
4. Vai a **API (Enable OAuth Settings)** → **View**
5. **Salva immediatamente**:
   - **Consumer Key** (Client ID): `3MVG9...` (esempio)
   - **Consumer Secret** (Client Secret): `ABC123...` (esempio)
   
   ⚠️ **IMPORTANTE**: Il Consumer Secret viene mostrato solo una volta!

#### 1.4 Configurare Network Access (Se Necessario)

**⭐ Raccomandazione**: Se possibile, usa **Azure Private Link** per Log Analytics invece di configurare range IP pubblici.

**Opzione A: Usa Private Link (Consigliato)**
1. Configura Azure Private Link per il Log Analytics Workspace
2. Il CCF invierà dati tramite Private Link
3. In Salesforce, imposta **IP Relaxation**: "Relax IP restrictions"
4. Nessuna configurazione di range IP necessaria

**Opzione B: Configura Range IP Pubblici**
1. Vai a **Setup** → **Network Access**
2. Clicca su **New** per aggiungere range IP
3. Aggiungi i range IP di Azure Cloud per la tua regione
   - Vedi [Gestione Network e Sicurezza](../../implementation/network-sicurezza.md) per dettagli
4. **Nota**: I range IP cambiano settimanalmente, richiede manutenzione periodica

#### 1.5 Configurare Permessi

1. Vai a **Setup** → **Users** → **Permission Sets**
2. Crea un nuovo Permission Set chiamato "Azure Sentinel Integration"
3. Aggiungi i permessi:
   - **API Enabled**
   - **View Event Log Files**
4. Assegna il Permission Set all'utente che eseguirà l'integrazione

### Passo 2: Preparazione Azure Sentinel

#### 2.1 Verificare Log Analytics Workspace

1. Accedi al [Portale Azure](https://portal.azure.com)
2. Cerca "Log Analytics workspaces"
3. Verifica che esista un workspace (o creane uno nuovo)
4. Annota il **Workspace ID** (lo trovi in **Overview** → **Workspace ID**)

#### 2.2 Abilitare Azure Sentinel

1. Nel portale Azure, cerca "Azure Sentinel"
2. Se non già abilitato, clicca su **Create**
3. Seleziona il Log Analytics Workspace
4. Clicca su **Add**

### Passo 3: Configurare il Connector CCF

#### 3.1 Accedere al Connector

1. In Azure Sentinel, vai a **Data connectors**
2. Cerca "Salesforce" nella barra di ricerca
3. Seleziona il connector Salesforce (se disponibile) oppure usa un connector CCF generico
4. Clicca su **Open connector page**

#### 3.2 Configurare Autenticazione OAuth

1. Nella pagina del connector, clicca su **Configure OAuth**
2. Compila i campi:
   ```
   Client ID: <Consumer Key da Salesforce>
   Client Secret: <Consumer Secret da Salesforce>
   Authorization URL: https://login.salesforce.com/services/oauth2/authorize
   Token URL: https://login.salesforce.com/services/oauth2/token
   Scope: api refresh_token offline_access id profile email
   ```
3. Clicca su **Authorize** o **Test Connection**
4. Verrai reindirizzato a Salesforce per autorizzare l'app
5. Accetta le autorizzazioni
6. Verifica che la connessione sia riuscita

#### 3.3 Configurare Parametri di Raccolta

1. Nella configurazione del connector, imposta:
   ```
   Event Types: LoginEvent, LogoutEvent, ApiEvent
   Start Date: <Data di inizio raccolta, es. 2024-01-01>
   Polling Interval: 15 minutes
   ```
2. Configura i filtri (opzionale):
   ```
   Include Events: All
   Exclude Events: (lascia vuoto o specifica eventi da escludere)
   ```

#### 3.4 Configurare Mapping Dati

Il connector mapperà automaticamente i campi Salesforce ai campi Log Analytics:

```
Salesforce Field          → Log Analytics Field
─────────────────────────────────────────────────
EventType                 → EventType_s
LogDate                   → TimeGenerated
UserId                    → UserId_s
Username                  → UserName_s
SourceIp                  → SourceIP_s
Browser                   → Browser_s
Platform                  → Platform_s
LoginType                 → LoginType_s
Status                    → Status_s
```

#### 3.5 Abilitare il Connector

1. Verifica tutte le configurazioni
2. Clicca su **Enable** o **Activate**
3. Attendi la conferma che il connector è attivo
4. Il connector inizierà a raccogliere dati entro 15-30 minuti

> ℹ️ **Tempistiche realistiche**  
> Anche se la connessione è attiva subito, Salesforce rende disponibili gli Event Log Files solo dopo l'elaborazione dei blocchi orari descritta nella [documentazione ufficiale](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_file_hourly_overview.htm). In produzione gli eventi arrivano tipicamente in Sentinel con 24-48 ore di ritardo rispetto al verificarsi effettivo.

### Passo 4: Verificare l'Integrazione

#### 4.1 Verificare Ricezione Dati

1. In Azure Sentinel, vai a **Logs**
2. Esegui la query:
   ```kql
   Salesforce_CL
   | where TimeGenerated > ago(1h)
   | take 10
   | project TimeGenerated, UserName_s, EventType_s, SourceIP_s
   ```
3. Verifica che i dati siano presenti

#### 4.2 Verificare Schema Dati

```kql
Salesforce_CL
| where TimeGenerated > ago(24h)
| summarize count() by EventType_s
| render columnchart
```

#### 4.3 Verificare Eventi Recenti

```kql
Salesforce_CL
| where TimeGenerated > ago(1h)
| where EventType_s == "LoginEvent"
| project TimeGenerated, UserName_s, SourceIP_s, Browser_s, Platform_s
| order by TimeGenerated desc
```

### Passo 5: Configurare Query e Alert

#### 5.1 Query per Login Falliti

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where Status_s == "Failed" or Status_s contains "Failure"
| project TimeGenerated, UserName_s, SourceIP_s, Status_s
| order by TimeGenerated desc
```

#### 5.2 Alert per Troppi Login Falliti

1. Vai a **Analytics** → **Rules**
2. Clicca su **Create** → **Scheduled query rule**
3. Configura:
   ```
   Name: Salesforce - Multiple Failed Logins
   Query:
   Salesforce_CL
   | where EventType_s == "LoginEvent"
   | where Status_s == "Failed"
   | where TimeGenerated > ago(1h)
   | summarize FailedAttempts = count() by UserName_s
   | where FailedAttempts > 5
   
   Entity mapping: UserName_s → Account
   Alert threshold: Greater than 0
   ```
4. Salva e abilita la regola

#### 5.3 Query per Accessi da IP Non Usuali

```kql
let KnownIPs = Salesforce_CL
| where TimeGenerated between (ago(30d) .. ago(1h))
| where EventType_s == "LoginEvent"
| summarize KnownIPSet = make_set(SourceIP_s) by UserName_s;
Salesforce_CL
| where TimeGenerated > ago(1h)
| where EventType_s == "LoginEvent"
| join kind=inner (KnownIPs) on UserName_s
| where SourceIP_s !in (KnownIPSet)
| project TimeGenerated, UserName_s, SourceIP_s
```

### Passo 6: Monitoraggio e Manutenzione

#### 6.1 Verificare Stato Connector

1. Vai a **Data connectors**
2. Verifica lo stato del connector Salesforce
3. Controlla eventuali errori o avvisi
4. Verifica l'ultima sincronizzazione

#### 6.2 Monitorare Volume Dati

```kql
Salesforce_CL
| where TimeGenerated > ago(24h)
| summarize 
    TotalEvents = count(),
    EventsByType = count() by EventType_s
| render piechart
```

#### 6.3 Verificare Latenza

```kql
Salesforce_CL
| where TimeGenerated > ago(1h)
| extend Latency = datetime_diff('minute', TimeGenerated, _IngestionTime)
| summarize 
    AvgLatency = avg(Latency),
    MaxLatency = max(Latency),
    MinLatency = min(Latency)
```

## Troubleshooting

### Problema: Nessun Dato Ricevuto

**Possibili Cause:**
- Event Monitoring non attivo da almeno 24-48 ore
- Credenziali OAuth non valide
- Connector non abilitato correttamente
- Permessi insufficienti in Salesforce

**Soluzione:**
1. Verifica che Event Monitoring sia attivo da almeno 48 ore
2. Testa le credenziali OAuth manualmente
3. Verifica lo stato del connector
4. Controlla i log del connector per errori

### Problema: Errori di Autenticazione

**Possibili Cause:**
- Consumer Secret errato o scaduto
- Callback URL non corrispondente
- OAuth Scopes insufficienti

**Soluzione:**
1. Rigenera il Consumer Secret se necessario
2. Verifica il Callback URL nella Connected App
3. Aggiungi tutti gli OAuth Scopes necessari

### Problema: Dati Incompleti

**Possibili Cause:**
- Filtri troppo restrittivi
- Eventi non ancora disponibili
- Rate limits raggiunti

**Soluzione:**
1. Rivedi i filtri nella configurazione
2. Verifica la data degli eventi richiesti
3. Controlla i rate limits di Salesforce

## Limitazioni e Limiti di Polling

### Limiti di Polling del CCF

Il CCF ha limitazioni specifiche sul polling che è importante conoscere:

#### Intervallo di Polling

- **Intervallo Minimo**: 5 minuti
- **Intervallo Massimo**: 24 ore
- **Intervallo Consigliato**: 15-30 minuti
- **Intervallo Default**: 15 minuti

⚠️ **Nota**: Intervalli troppo brevi (< 5 minuti) non sono supportati e possono causare:
- Rate limiting da parte di Salesforce
- Aumento dei costi Azure
- Carico eccessivo sul sistema

#### Limiti di Volume Dati

- **Dimensione Massima per Richiesta**: 10 MB
- **Numero Massimo di Eventi per Poll**: 10.000 eventi
- **Timeout Richiesta**: 5 minuti

Se il volume di eventi supera questi limiti:
- Il connector effettuerà più richieste in batch
- Potrebbe essere necessario aumentare l'intervallo di polling
- Considera di filtrare eventi non essenziali

#### Limiti di Rate Limiting

Il CCF rispetta i limiti API di Salesforce:

- **API Requests per 24h**: Dipende dalla licenza Salesforce
  - Enterprise: ~15.000 richieste/24h
  - Unlimited: ~100.000 richieste/24h
  - Performance: ~50.000 richieste/24h
- **Concurrent Requests**: Massimo 25 simultanee
- **Event Log Files**: Disponibili dopo 24-48 ore dalla generazione

#### Calcolo Intervallo Ottimale

Per calcolare l'intervallo di polling ottimale:

```
Intervallo (minuti) = (Eventi Giornalieri / Eventi per Poll) × 1440 / Numero Richieste Disponibili
```

**Esempio**:
- 50.000 eventi/giorno
- 10.000 eventi per poll
- 15.000 richieste disponibili/24h

```
Intervallo = (50.000 / 10.000) × 1440 / 15.000 = 0.48 minuti
```

In questo caso, usa l'intervallo minimo di **5 minuti** e considera:
- Filtrare eventi non essenziali
- Aumentare l'intervallo a 15-30 minuti
- Usare una soluzione alternativa (Azure Function) per maggiore controllo

#### Limitazioni Temporali

- **Delay Eventi**: Gli eventi sono disponibili in Salesforce dopo 24-48 ore
- **Latenza Raccolta**: Il CCF può avere una latenza di 15-30 minuti dall'evento alla raccolta
- **Latenza Totale**: Fino a 48-72 ore per eventi molto recenti

#### Limitazioni di Connettività

- **Timeout Connessione**: 5 minuti
- **Retry Automatico**: 3 tentativi con backoff esponenziale
- **Intervallo Retry**: 1 minuto, 5 minuti, 15 minuti

### Gestione dei Limiti

#### Monitoraggio Utilizzo API

```kql
// Verifica numero di richieste effettuate
Salesforce_CL
| where TimeGenerated > ago(24h)
| summarize 
    TotalEvents = count(),
    Requests = dcount(bin(TimeGenerated, 1h))
| extend AvgEventsPerRequest = TotalEvents / Requests
```

#### Alert per Limiti Raggiunti

Configura alert per:
- Volume eventi superiore alla capacità
- Errori di rate limiting
- Timeout frequenti
- Latenza eccessiva

#### Ottimizzazione Polling

1. **Aumenta Intervallo**: Se non hai bisogno di dati in tempo reale
2. **Filtra Eventi**: Raccogli solo eventi essenziali
3. **Usa Batch**: Raggruppa richieste quando possibile
4. **Monitora Costi**: Intervalli brevi aumentano i costi Azure

## Best Practices

1. **Monitoraggio Proattivo**: Configura alert per errori del connector
2. **Retention Dati**: Configura retention appropriata in Log Analytics
3. **Sicurezza**: Usa Key Vault per memorizzare credenziali sensibili
4. **Documentazione**: Mantieni traccia delle configurazioni
5. **Test**: Testa sempre in ambiente di sviluppo prima della produzione
6. **Polling Ottimale**: Usa intervalli di 15-30 minuti per bilanciare latenza e costi
7. **Monitoraggio Limiti**: Monitora regolarmente l'utilizzo API per evitare rate limiting

## Configurazione Avanzata

### Filtri Personalizzati

Puoi configurare filtri avanzati per raccogliere solo eventi specifici:

```
Event Types: LoginEvent
Filters:
  - Status: Success
  - SourceIP: !contains "10.0.0.0/8"
  - LoginType: Web
```

### Trasformazione Dati

Il CCF supporta trasformazioni base dei dati:
- Rinomina campi
- Aggiungi campi calcolati
- Filtra valori

### Integrazione con Altri Connector

Combina i dati Salesforce con altri log:
- Azure AD Sign-in Logs
- Office 365 Activity Logs
- Altri log di sicurezza

## Link Utili

- [Documentazione CCF Microsoft](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)
- [Salesforce Event Monitoring](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Azure Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [Troubleshooting Guide](../../troubleshooting.md)

## Esempio di Configurazione Completa

### File di Configurazione (JSON)

```json
{
  "connector": {
    "name": "Salesforce-CCF",
    "type": "codeless",
    "enabled": true
  },
  "authentication": {
    "type": "oauth2",
    "clientId": "3MVG9...",
    "clientSecret": "ABC123...",
    "authorizationUrl": "https://login.salesforce.com/services/oauth2/authorize",
    "tokenUrl": "https://login.salesforce.com/services/oauth2/token",
    "scope": "api refresh_token offline_access"
  },
  "dataCollection": {
    "eventTypes": ["LoginEvent", "LogoutEvent", "ApiEvent"],
    "startDate": "2024-01-01T00:00:00Z",
    "pollingInterval": 15,
    "filters": {
      "include": ["*"],
      "exclude": []
    }
  },
  "mapping": {
    "tableName": "Salesforce_CL",
    "fields": {
      "EventType": "EventType_s",
      "LogDate": "TimeGenerated",
      "UserId": "UserId_s",
      "Username": "UserName_s",
      "SourceIp": "SourceIP_s"
    }
  }
}
```

---

**Prossimi Passi:**
- [Configurare Query KQL avanzate](../../implementation/kql-queries.md)
- [Gestire Network e Sicurezza](../../implementation/network-sicurezza.md)
- [Risolvere problemi comuni](../../troubleshooting.md)

## Fonti

- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [CodeLess Connector Framework (Microsoft Sentinel)](https://learn.microsoft.com/azure/sentinel/create-codeless-connector)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)


