# API Reference

Riferimento alle API utilizzate nell'integrazione Salesforce-Azure Sentinel.

## Salesforce APIs

### Event Log Files API

Endpoint per recuperare i log degli eventi Salesforce.

**Base URL**: `https://<instance>.salesforce.com/services/data/v<version>/sobjects/EventLogFile/`

#### Metodi Principali

**GET /EventLogFile**

Recupera la lista dei file di log disponibili.

**Parametri**:
- `q`: Query SOQL (es. `SELECT Id, EventType, LogDate FROM EventLogFile WHERE LogDate = TODAY`)

**Esempio**:
```http
GET /services/data/v58.0/sobjects/EventLogFile/?q=SELECT+Id,EventType,LogDate+FROM+EventLogFile+WHERE+LogDate=TODAY
Authorization: Bearer <access_token>
```

**GET /EventLogFile/{Id}/LogFile**

Scarica il contenuto di un file di log specifico.

**Esempio**:
```http
GET /services/data/v58.0/sobjects/EventLogFile/{Id}/LogFile
Authorization: Bearer <access_token>
```

### OAuth 2.0 Authentication

**Token Endpoint**: `https://<instance>.salesforce.com/services/oauth2/token`

**Grant Type**: Username-Password Flow

**Request**:
```http
POST /services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&client_id=<consumer_key>
&client_secret=<consumer_secret>
&username=<username>
&password=<password><security_token>
```

**Response**:
```json
{
  "access_token": "00D...",
  "instance_url": "https://yourinstance.salesforce.com",
  "id": "https://login.salesforce.com/id/...",
  "token_type": "Bearer",
  "issued_at": "1234567890",
  "signature": "..."
}
```

## Azure Log Analytics Data Collector API

Endpoint per inviare dati a Log Analytics.

**Base URL**: `https://<workspace-id>.ods.opinsights.azure.com/api/logs?api-version=2016-04-01`

### POST /api/logs

Invia dati a Log Analytics.

**Headers**:
- `Log-Type`: Nome della tabella custom (es. `Salesforce_CL`)
- `x-ms-date`: Data/ora in formato RFC 1123
- `Authorization`: Signature HMAC-SHA256
- `Content-Type`: `application/json`

**Request Body**:
```json
[
  {
    "TimeGenerated": "2024-01-15T10:30:00Z",
    "EventType": "LoginEvent",
    "UserName": "user@example.com",
    "SourceIP": "192.168.1.1"
  }
]
```

**Esempio**:
```http
POST /api/logs?api-version=2016-04-01
Log-Type: Salesforce_CL
x-ms-date: Mon, 15 Jan 2024 10:30:00 GMT
Authorization: SharedKey <workspace-id>:<signature>
Content-Type: application/json

[{"TimeGenerated":"2024-01-15T10:30:00Z","EventType":"LoginEvent","UserName":"user@example.com","SourceIP":"192.168.1.1"}]
```

### Generazione Signature

```csharp
string signature = BuildSignature(
    jsonContent,
    workspaceKey,
    "POST",
    contentLength,
    "application/json",
    date,
    "/api/logs"
);

string BuildSignature(string content, string key, string method, int contentLength, string contentType, string date, string resource)
{
    string stringToSign = $"{method}\n{contentLength}\n{contentType}\nx-ms-date:{date}\n{resource}";
    byte[] keyBytes = Convert.FromBase64String(key);
    byte[] messageBytes = Encoding.UTF8.GetBytes(stringToSign);
    using (var hmac = new HMACSHA256(keyBytes))
    {
        byte[] hash = hmac.ComputeHash(messageBytes);
        return Convert.ToBase64String(hash);
    }
}
```

## Azure Service Management API

### Get Service Tags

Recupera i range IP di Azure.

**Endpoint**: `https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Network/locations/{location}/serviceTagDetails?api-version=2021-05-01`

**Esempio**:
```http
GET /subscriptions/{subscriptionId}/providers/Microsoft.Network/locations/westeurope/serviceTagDetails?api-version=2021-05-01
Authorization: Bearer <access_token>
```

## Rate Limits

### Salesforce

- **API Requests**: 15,000 per 24 ore (varia per licenza)
- **Concurrent Requests**: 25 simultanee
- **Event Log Files**: Disponibili dopo 24-48 ore

### Azure Log Analytics

- **Data Ingestion**: Fino a 6 GB/minuto per workspace
- **API Calls**: 500 richieste/minuto
- **Payload Size**: Max 30 MB per richiesta

## Error Handling

### Salesforce API Errors

**401 Unauthorized**:
- Token scaduto o non valido
- Soluzione: Rinnova il token OAuth

**403 Forbidden**:
- Permessi insufficienti
- Soluzione: Verifica Permission Sets

**429 Too Many Requests**:
- Rate limit superato
- Soluzione: Implementa retry con backoff esponenziale

### Azure Log Analytics Errors

**400 Bad Request**:
- Formato dati non valido
- Soluzione: Verifica schema JSON

**401 Unauthorized**:
- Signature non valida
- Soluzione: Verifica workspace key e algoritmo HMAC

## Link Utili

- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Event Log Files API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/event_log_files_api.htm)
- [Log Analytics Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)
- [Azure Service Tags API](https://learn.microsoft.com/azure/virtual-network/service-tags-overview)

## Fonti

- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Salesforce Event Log File REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)
- [Azure Service Tags Overview](https://learn.microsoft.com/azure/virtual-network/service-tags-overview)

