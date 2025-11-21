# Campi Real-Time per SIEM - Azure Sentinel

Guida completa ai campi Salesforce estraibili in real-time per sistemi SIEM, con focus su Azure Sentinel.

## Panoramica

Questa guida descrive tutti i campi e gli eventi che possono essere estratti da Salesforce in **real-time** (< 1 minuto) per l'integrazione con sistemi SIEM come Azure Sentinel.

## ⚠️ Approccio Real-Time

**Meccanismo**: Platform Events / Change Data Capture (CDC) / Real-Time Event Monitoring

**Latenza**: < 1 minuto (tipicamente 5-30 secondi)

**Non disponibile in real-time**: Audit Trail, Field History Tracking, molti eventi di sistema (vedi [Limitazioni Real-Time](#limitazioni-real-time))

## Eventi di Autenticazione e Accesso

### LoginEvent (Priorità: Critica)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "Login",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "SourceIp": "192.168.1.100",
  "LoginUrl": "https://login.salesforce.com",
  "Browser": "Chrome",
  "Platform": "Windows",
  "LoginType": "Web",
  "Status": "Success",
  "LoginGeoId": "US",
  "LoginLatitude": 37.7749,
  "LoginLongitude": -122.4194,
  "SessionKey": "abc123",
  "SessionLevel": "STANDARD",
  "Timestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `UserId` - ID utente Salesforce
- `Username` - Username utente
- `SourceIp` - IP di origine
- `Status` - Success/Failure
- `LoginType` - Web/Mobile/API
- `LoginGeoId` - Geolocalizzazione
- `Browser` - Browser utilizzato
- `Platform` - Sistema operativo
- `Timestamp` - Data/ora evento

**Utilizzo SIEM**:
- Rilevare accessi sospetti
- Identificare accessi da IP anomali
- Tracciare accessi da geolocalizzazioni insolite
- Monitorare tentativi di login falliti
- Correlare con altri eventi di sicurezza

---

### LogoutEvent (Priorità: Critica)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "Logout",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "SourceIp": "192.168.1.100",
  "LogoutUrl": "https://login.salesforce.com",
  "SessionKey": "abc123",
  "Timestamp": "2024-01-15T18:00:00Z"
}
```

**Campi prioritari**:
- `UserId` - ID utente Salesforce
- `Username` - Username utente
- `SourceIp` - IP di origine
- `SessionKey` - Chiave sessione
- `Timestamp` - Data/ora evento

**Utilizzo SIEM**:
- Tracciare disconnessioni
- Identificare sessioni terminate anormalmente
- Correlare con eventi di sicurezza
- Analisi pattern di utilizzo

---

## Eventi API e Accesso Esterno

### ApiEvent (Priorità: Critica)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "API",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "ApiType": "REST",
  "ApiVersion": "58.0",
  "Client": "Postman",
  "Method": "GET",
  "Url": "/services/data/v58.0/sobjects/Account",
  "Status": "200",
  "ResponseTime": 150,
  "RequestSize": 1024,
  "ResponseSize": 2048,
  "SourceIp": "192.168.1.100",
  "Timestamp": "2024-01-15T10:35:00Z"
}
```

**Campi prioritari**:
- `UserId` - ID utente Salesforce
- `Username` - Username utente
- `ApiType` - REST/SOAP/Bulk
- `Method` - GET/POST/PUT/DELETE
- `Url` - Endpoint chiamato
- `Status` - Codice risposta HTTP
- `ResponseTime` - Tempo di risposta (ms)
- `SourceIp` - IP di origine
- `Client` - Client utilizzato
- `Timestamp` - Data/ora evento

**Utilizzo SIEM**:
- Rilevare chiamate API anomale
- Identificare accessi non autorizzati
- Monitorare performance API
- Tracciare accessi esterni
- Rilevare pattern di attacco
- Correlare con eventi di sicurezza

---

## Modifiche a Dati Sensibili (Change Data Capture)

### Account (Priorità: Alta)

**Disponibilità**: Change Data Capture (CDC) - configurabile per qualsiasi oggetto

**Campi essenziali per SIEM**:

```json
{
  "changeType": "UPDATE",
  "entityName": "Account",
  "recordId": "001xx000003DGbQAAW",
  "changeFields": {
    "Name": {
      "oldValue": "Old Name",
      "newValue": "New Name"
    },
    "AnnualRevenue": {
      "oldValue": 1000000,
      "newValue": 2000000
    },
    "BillingAddress": {
      "oldValue": "Old Address",
      "newValue": "New Address"
    },
    "OwnerId": {
      "oldValue": "005xx000001XKnoAAG",
      "newValue": "005xx000001XKnoBAG"
    }
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "committedTimestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `entityName` - Nome oggetto
- `recordId` - ID record modificato
- `changeFields` - Campi modificati (oldValue/newValue)
- `UserId` - ID utente che ha modificato
- `Username` - Username utente
- `committedTimestamp` - Data/ora modifica

**Campi sensibili da monitorare**:
- `AnnualRevenue` - Dati finanziari
- `OwnerId` - Cambio ownership
- `BillingAddress` - Dati aziendali
- `Name` - Modifiche nome account

**Utilizzo SIEM**:
- Rilevare modifiche non autorizzate
- Tracciare cambi di ownership
- Monitorare modifiche a dati finanziari
- Identificare accessi privilegiati
- Compliance e audit

---

### Contact (Priorità: Alta)

**Disponibilità**: Change Data Capture (CDC)

**Campi essenziali per SIEM**:

```json
{
  "changeType": "UPDATE",
  "entityName": "Contact",
  "recordId": "003xx000004DGbQAAW",
  "changeFields": {
    "Email": {
      "oldValue": "old@example.com",
      "newValue": "new@example.com"
    },
    "Phone": {
      "oldValue": "+1-555-1234",
      "newValue": "+1-555-5678"
    },
    "AccountId": {
      "oldValue": "001xx000003DGbQAAW",
      "newValue": "001xx000003DGbCAAW"
    }
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "committedTimestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `recordId` - ID record modificato
- `changeFields` - Campi modificati
- `UserId` - ID utente che ha modificato
- `Username` - Username utente
- `committedTimestamp` - Data/ora modifica

**Campi sensibili da monitorare**:
- `Email` - Dati personali (GDPR)
- `Phone` - Dati personali
- `AccountId` - Relazioni account

**Utilizzo SIEM**:
- Rilevare modifiche a dati personali (GDPR)
- Tracciare modifiche a contatti critici
- Monitorare accessi a dati sensibili
- Compliance privacy

---

### Lead (Priorità: Alta)

**Disponibilità**: Change Data Capture (CDC)

**Campi essenziali per SIEM**:

```json
{
  "changeType": "CREATE",
  "entityName": "Lead",
  "recordId": "00Qxx000004DGbQAAW",
  "changeFields": {
    "Email": "lead@example.com",
    "Company": "New Corp",
    "LeadSource": "Web",
    "Status": "Open"
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "committedTimestamp": "2024-01-15T12:00:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `recordId` - ID record
- `changeFields` - Campi modificati
- `UserId` - ID utente
- `Username` - Username utente
- `committedTimestamp` - Data/ora

**Utilizzo SIEM**:
- Tracciare creazione lead
- Monitorare accessi a lead
- Rilevare pattern di spam/frode
- Analisi conversioni

---

### Opportunity (Priorità: Alta)

**Disponibilità**: Change Data Capture (CDC)

**Campi essenziali per SIEM**:

```json
{
  "changeType": "UPDATE",
  "entityName": "Opportunity",
  "recordId": "006xx000004DGbQAAW",
  "changeFields": {
    "Amount": {
      "oldValue": 50000,
      "newValue": 100000
    },
    "StageName": {
      "oldValue": "Prospecting",
      "newValue": "Closed Won"
    },
    "CloseDate": {
      "oldValue": "2024-03-31",
      "newValue": "2024-01-31"
    },
    "OwnerId": {
      "oldValue": "005xx000001XKnoAAG",
      "newValue": "005xx000001XKnoBAG"
    }
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "committedTimestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `recordId` - ID record
- `changeFields` - Campi modificati
- `UserId` - ID utente
- `Username` - Username utente
- `committedTimestamp` - Data/ora

**Campi sensibili da monitorare**:
- `Amount` - Valore opportunità
- `StageName` - Stage opportunità
- `OwnerId` - Cambio ownership
- `CloseDate` - Data chiusura

**Utilizzo SIEM**:
- Rilevare modifiche a opportunità critiche
- Tracciare cambi di stage/amount
- Monitorare accessi privilegiati
- Identificare frodi
- Analisi performance vendite

---

### Case (Priorità: Alta)

**Disponibilità**: Change Data Capture (CDC)

**Campi essenziali per SIEM**:

```json
{
  "changeType": "UPDATE",
  "entityName": "Case",
  "recordId": "500xx000004DGbQAAW",
  "changeFields": {
    "Status": {
      "oldValue": "New",
      "newValue": "Closed"
    },
    "Priority": {
      "oldValue": "Low",
      "newValue": "High"
    },
    "OwnerId": {
      "oldValue": "005xx000001XKnoAAG",
      "newValue": "005xx000001XKnoBAG"
    }
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "committedTimestamp": "2024-01-15T14:00:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `recordId` - ID record
- `changeFields` - Campi modificati
- `UserId` - ID utente
- `Username` - Username utente
- `committedTimestamp` - Data/ora

**Campi sensibili da monitorare**:
- `Status` - Stato case
- `Priority` - Priorità case
- `OwnerId` - Cambio ownership

**Utilizzo SIEM**:
- Tracciare modifiche a case critici
- Monitorare accessi a dati sensibili
- Rilevare pattern di accesso anomalo
- Analisi performance supporto

---

## Modifiche a Utenti e Permessi

### User (Priorità: Critica)

**Disponibilità**: Change Data Capture (CDC)

**Campi essenziali per SIEM**:

```json
{
  "changeType": "UPDATE",
  "entityName": "User",
  "recordId": "005xx000001XKnoAAG",
  "changeFields": {
    "IsActive": {
      "oldValue": true,
      "newValue": false
    },
    "ProfileId": {
      "oldValue": "00exx000001XKnoAAG",
      "newValue": "00exx000001XKnoBAG"
    },
    "UserRoleId": {
      "oldValue": "00Exx000001XKnoAAG",
      "newValue": "00Exx000001XKnoBAG"
    },
    "Email": {
      "oldValue": "old@example.com",
      "newValue": "new@example.com"
    }
  },
  "UserId": "005xx000001XKnoAAG",
  "Username": "admin@example.com",
  "committedTimestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `changeType` - CREATE/UPDATE/DELETE/UNDELETE
- `recordId` - ID utente modificato
- `changeFields` - Campi modificati
- `UserId` - ID utente che ha modificato
- `Username` - Username utente che ha modificato
- `committedTimestamp` - Data/ora modifica

**Campi critici da monitorare**:
- `IsActive` - Attivazione/disattivazione utente
- `ProfileId` - Cambio profilo (permessi)
- `UserRoleId` - Cambio ruolo (gerarchia)
- `Email` - Modifica email

**Utilizzo SIEM**:
- Rilevare modifiche a permessi utente
- Tracciare cambi di profilo/ruolo
- Monitorare disattivazioni utente
- Identificare escalation privilegi
- Alerting critico per sicurezza

---

## Eventi di Navigazione e Utilizzo

### UriEvent (Priorità: Media)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "URI",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "Uri": "/001xx000003DGbQAAW",
  "PageUrl": "https://instance.salesforce.com/001xx000003DGbQAAW",
  "Duration": 5000,
  "SourceIp": "192.168.1.100",
  "Timestamp": "2024-01-15T10:30:00Z"
}
```

**Campi prioritari**:
- `UserId` - ID utente
- `Username` - Username utente
- `Uri` - URI visitato
- `PageUrl` - URL completo
- `Duration` - Tempo su pagina (ms)
- `SourceIp` - IP di origine
- `Timestamp` - Data/ora

**Utilizzo SIEM**:
- Tracciare navigazione utente
- Identificare accessi a record sensibili
- Monitorare pattern di utilizzo
- Rilevare comportamenti anomali
- Analisi user behavior

---

### ReportEvent (Priorità: Media)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "Report",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "ReportId": "00Oxx000001XKnoAAG",
  "ReportName": "Sales Report",
  "Duration": 500,
  "RowsReturned": 100,
  "Timestamp": "2024-01-15T10:30:00Z"
}
```

**Utilizzo SIEM**:
- Tracciare accessi a report
- Monitorare esportazioni dati
- Rilevare accessi non autorizzati

---

### DashboardEvent (Priorità: Media)

**Disponibilità**: Real-Time Event Monitoring (richiede configurazione)

**Campi essenziali per SIEM**:

```json
{
  "EventType": "Dashboard",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "DashboardId": "01Zxx000001XKnoAAG",
  "DashboardName": "Sales Dashboard",
  "Duration": 300,
  "Timestamp": "2024-01-15T10:30:00Z"
}
```

**Utilizzo SIEM**:
- Tracciare accessi a dashboard
- Monitorare utilizzo dashboard
- Analisi pattern di utilizzo

---

## Eventi Custom per Sicurezza

### Platform Event Custom - Security Event

**Disponibilità**: Platform Events custom (da creare)

**Esempio struttura**:

```json
{
  "EventType": "SecurityEvent",
  "EventSubType": "FailedLogin",
  "UserId": "005xx000001XKnoAAG",
  "Username": "user@example.com",
  "SourceIp": "192.168.1.100",
  "UserAgent": "Mozilla/5.0...",
  "Reason": "Invalid Password",
  "AttemptCount": 3,
  "Timestamp": "2024-01-15T10:30:00Z"
}
```

**Utilizzo SIEM**:
- Eventi custom di sicurezza
- Tentativi di accesso falliti
- Violazioni policy
- Eventi business-specific
- Integrazione con logica custom

---

## Riepilogo Priorità

### Priorità Critica (Estrarre Sempre)

1. **LoginEvent** - Accessi utente
2. **LogoutEvent** - Disconnessioni
3. **ApiEvent** - Chiamate API
4. **User (CDC)** - Modifiche permessi utente

### Priorità Alta (Estrarre se Rilevanti)

5. **Account (CDC)** - Modifiche account
6. **Contact (CDC)** - Modifiche contatti
7. **Opportunity (CDC)** - Modifiche opportunità
8. **Case (CDC)** - Modifiche case
9. **Lead (CDC)** - Modifiche lead

### Priorità Media (Estrarre se Necessario)

10. **UriEvent** - Navigazione
11. **ReportEvent** - Accessi report
12. **DashboardEvent** - Accessi dashboard

---

## Query KQL per Azure Sentinel

### Alert: Accessi Sospetti

```kql
SalesforcePlatformEvents_CL
| where EventType_s == "Login"
| where SourceIp_s !in (allowedIPs)
| where TimeGenerated > ago(5m)
| project TimeGenerated, Username_s, SourceIp_s, Status_s, LoginGeoId_s
```

### Alert: Modifiche a Permessi Utente

```kql
SalesforceCDC_CL
| where EntityName_s == "User"
| where ChangeType_s == "UPDATE"
| where ChangeFields_s contains "ProfileId" or ChangeFields_s contains "UserRoleId"
| where TimeGenerated > ago(5m)
| project TimeGenerated, Username_s, RecordId_s, ChangeFields_s
```

### Alert: Chiamate API Anomale

```kql
SalesforcePlatformEvents_CL
| where EventType_s == "API"
| where Status_s != "200"
| where TimeGenerated > ago(5m)
| project TimeGenerated, Username_s, Method_s, Url_s, Status_s, SourceIp_s
```

### Alert: Modifiche a Dati Finanziari

```kql
SalesforceCDC_CL
| where EntityName_s == "Account" or EntityName_s == "Opportunity"
| where ChangeType_s == "UPDATE"
| where ChangeFields_s contains "AnnualRevenue" or ChangeFields_s contains "Amount"
| where TimeGenerated > ago(5m)
| project TimeGenerated, Username_s, EntityName_s, RecordId_s, ChangeFields_s
```

### Alert: Disattivazione Utente

```kql
SalesforceCDC_CL
| where EntityName_s == "User"
| where ChangeType_s == "UPDATE"
| where ChangeFields_s contains "IsActive"
| where TimeGenerated > ago(5m)
| project TimeGenerated, Username_s, RecordId_s, ChangeFields_s
```

---

## Limitazioni Real-Time

### Non Disponibile in Real-Time

I seguenti eventi **non sono disponibili** in real-time e richiedono Event Log Files API (latenza 24-48 ore):

- **SetupAuditTrail** - Modifiche configurazione Salesforce
- **FieldHistoryTracking** - Storia modifiche campi
- **DataExportEvent** - Esportazioni dati
- **BulkApiResultEvent** - Risultati Bulk API
- **ApexExecutionEvent** - Esecuzione codice Apex
- **ApexUnexpectedExceptionEvent** - Eccezioni Apex
- **FlowExecutionEvent** - Esecuzione Flow
- E molti altri eventi di sistema

**Perché**: Questi eventi sono generati internamente da Salesforce e non esposti tramite Platform Events o CDC. Sono disponibili solo tramite Event Log Files API dopo elaborazione batch.

**Soluzione**: Usa approccio ibrido - real-time per eventi critici, Event Log Files per audit/compliance completa.

Vedi [Confronto Approcci](../introduction/approaches-comparison.md) per dettagli.

---

## Configurazione Real-Time Event Monitoring

Per abilitare eventi di monitoraggio in real-time:

1. **Abilita Real-Time Event Monitoring** in Salesforce Setup
2. **Configura Platform Events** per eventi specifici
3. **Abilita Change Data Capture** per oggetti da monitorare
4. **Configura integrazione** con Azure Function/Sentinel

Vedi [Implementazione Platform Events](../platform-events/implementation/event-hub.md) per dettagli.

---

## Best Practices SIEM

### 1. Campi Chiave da Includere Sempre

- `UserId` - Identificazione utente
- `Username` - Username utente
- `SourceIp` - IP di origine
- `Timestamp` - Data/ora evento
- `Status` / `ChangeType` - Tipo evento
- `changeFields` - Dettagli modifiche (per CDC)

### 2. Normalizzazione Dati

Normalizza i dati prima di inviare a Sentinel:
- Formato timestamp consistente
- Naming convention campi
- Valori standardizzati

### 3. Enrichment

Arricchisci eventi con:
- Informazioni utente (profilo, ruolo)
- Geolocalizzazione IP
- Contesto business
- Correlazioni con altri eventi

### 4. Alerting

Configura alert per:
- Accessi sospetti
- Modifiche a permessi
- Chiamate API anomale
- Modifiche a dati critici

---

## Prossimi Passi

1. **Configura Real-Time Event Monitoring** in Salesforce
2. **Abilita Change Data Capture** per oggetti critici
3. **Implementa integrazione** con Azure Function
4. **Configura query KQL** in Azure Sentinel
5. **Crea alert e playbook** per incident response

Vedi:
- [Implementazione Platform Events](../platform-events/implementation/event-hub.md)
- [Query KQL](../implementation/kql-queries.md)
- [Configurazione Avanzata](../implementation/network-sicurezza.md)

## Fonti

- [Salesforce Real-Time Event Monitoring](https://developer.salesforce.com/docs/platform/security/guide/real-time-event-monitoring.html)
- [Salesforce Platform Events Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
- [Salesforce Change Data Capture Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
- [Microsoft Sentinel Data Connectors](https://learn.microsoft.com/azure/sentinel/connect-data-sources)
- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)

