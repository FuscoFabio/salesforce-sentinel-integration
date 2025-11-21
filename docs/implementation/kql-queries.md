# Query KQL per Azure Sentinel

Raccolta di query KQL (Kusto Query Language) per analizzare gli eventi Salesforce in Azure Sentinel.

## Query Base

### Visualizzare Tutti gli Eventi Recenti

```kql
Salesforce_CL
| where TimeGenerated > ago(24h)
| project TimeGenerated, UserName_s, EventType_s, SourceIP_s, Browser_s, Platform_s
| order by TimeGenerated desc
```

### Contare Eventi per Tipo

```kql
Salesforce_CL
| where TimeGenerated > ago(7d)
| summarize count() by EventType_s
| render columnchart
```

### Eventi per Utente

```kql
Salesforce_CL
| where TimeGenerated > ago(7d)
| summarize EventCount = count() by UserName_s
| order by EventCount desc
| take 20
```

## Query di Sicurezza

### Login Falliti

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where Success_b == false
| project TimeGenerated, UserName_s, SourceIP_s, FailureReason_s
| order by TimeGenerated desc
```

### Accessi da IP Sospetti

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where SourceIP_s !startswith "10." and SourceIP_s !startswith "192.168."
| summarize count() by SourceIP_s, UserName_s
| order by count_ desc
```

### Accessi Multipli da IP Diversi

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where TimeGenerated > ago(1h)
| summarize IPCount = dcount(SourceIP_s), IPs = make_set(SourceIP_s) by UserName_s
| where IPCount > 3
| project UserName_s, IPCount, IPs
```

### Accessi Fuori Orario

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where TimeGenerated > ago(7d)
| extend Hour = datetime_part("hour", TimeGenerated)
| where Hour < 6 or Hour > 22
| summarize count() by UserName_s, Hour
| order by count_ desc
```

### Accessi da Browser/Device Non Usuali

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where TimeGenerated > ago(30d)
| summarize 
    CommonBrowsers = make_set(Browser_s) by UserName_s
| extend BrowserCount = array_length(CommonBrowsers)
| where BrowserCount > 3
| project UserName_s, BrowserCount, CommonBrowsers
```

## Query di Analisi

### Attività per Ora del Giorno

```kql
Salesforce_CL
| where TimeGenerated > ago(7d)
| extend Hour = datetime_part("hour", TimeGenerated)
| summarize EventCount = count() by Hour
| order by Hour asc
| render timechart
```

### Top 10 Utenti per Attività

```kql
Salesforce_CL
| where TimeGenerated > ago(7d)
| summarize 
    LoginCount = countif(EventType_s == "LoginEvent"),
    ApiCallCount = countif(EventType_s == "ApiEvent"),
    TotalEvents = count()
    by UserName_s
| order by TotalEvents desc
| take 10
```

### Distribuzione Geografica (se disponibile)

```kql
Salesforce_CL
| where TimeGenerated > ago(7d)
| where isnotempty(Country_s)
| summarize count() by Country_s
| order by count_ desc
| render piechart
```

### Pattern di Accesso Giornaliero

```kql
Salesforce_CL
| where TimeGenerated > ago(30d)
| where EventType_s == "LoginEvent"
| summarize DailyLogins = count() by bin(TimeGenerated, 1d), UserName_s
| render timechart
```

## Query per Alerting

### Alert: Troppi Login Falliti

```kql
Salesforce_CL
| where EventType_s == "LoginEvent"
| where Success_b == false
| where TimeGenerated > ago(1h)
| summarize FailedAttempts = count() by UserName_s
| where FailedAttempts > 5
```

### Alert: Nuovo IP per Utente

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
| project TimeGenerated, UserName_s, SourceIP_s, KnownIPSet
```

### Alert: Accesso da Paese Non Usuale

```kql
let UsualCountries = Salesforce_CL
| where TimeGenerated between (ago(30d) .. ago(1h))
| where EventType_s == "LoginEvent"
| summarize CountrySet = make_set(Country_s) by UserName_s;
Salesforce_CL
| where TimeGenerated > ago(1h)
| where EventType_s == "LoginEvent"
| where isnotempty(Country_s)
| join kind=inner (UsualCountries) on UserName_s
| where Country_s !in (CountrySet)
| project TimeGenerated, UserName_s, Country_s, CountrySet
```

## Query di Correlazione

### Correlazione con Altri Log (esempio con SigninLogs)

```kql
let SalesforceLogins = Salesforce_CL
| where EventType_s == "LoginEvent"
| where TimeGenerated > ago(1h)
| project TimeGenerated, UserName_s, SourceIP_s, EventType_s;
SigninLogs
| where TimeGenerated > ago(1h)
| project TimeGenerated, UserPrincipalName, IPAddress, AppDisplayName
| join kind=inner (SalesforceLogins) 
    on $left.IPAddress == $right.SourceIP_s
| project TimeGenerated, UserPrincipalName, IPAddress, UserName_s
```

## Query di Compliance e Audit

### Report Accessi per Audit

```kql
Salesforce_CL
| where TimeGenerated between (startofday(ago(30d)) .. endofday(now()))
| where EventType_s == "LoginEvent"
| summarize 
    FirstLogin = min(TimeGenerated),
    LastLogin = max(TimeGenerated),
    LoginCount = count(),
    UniqueIPs = dcount(SourceIP_s),
    Platforms = make_set(Platform_s)
    by UserName_s
| order by LoginCount desc
```

### Attività API per Utente

```kql
Salesforce_CL
| where EventType_s == "ApiEvent"
| where TimeGenerated > ago(7d)
| summarize 
    ApiCallCount = count(),
    UniqueEndpoints = dcount(Endpoint_s)
    by UserName_s
| order by ApiCallCount desc
```

## Note

- Sostituisci `Salesforce_CL` con il nome della tua tabella custom se diverso
- I nomi dei campi (es. `UserName_s`, `EventType_s`) potrebbero variare in base alla tua implementazione
- Aggiusta i filtri temporali (`ago(7d)`) in base alle tue esigenze
- Testa le query prima di usarle per alerting in produzione

## Link Utili

- [Documentazione KQL](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [KQL Quick Reference](https://learn.microsoft.com/azure/data-explorer/kql-quick-reference)
- [Azure Sentinel Query Examples](https://learn.microsoft.com/azure/sentinel/hunting)

## Fonti

- [Kusto Query Language (KQL) Documentation](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
- [Microsoft Sentinel Hunting Queries](https://learn.microsoft.com/azure/sentinel/hunting)
- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)

