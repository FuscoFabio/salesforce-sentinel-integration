# Checklist Secrets GitHub Actions

Lista completa dei secrets da configurare su GitHub per il deployment automatico.

## 📋 Lista Secrets

### 🔵 Azure Secrets (4 secrets)

#### 1. `AZURE_FUNCTIONAPP_NAME`
- **Descrizione**: Nome della Function App su Azure
- **Esempio**: `salesforce-sentinel-001`
- **Come ottenerlo**: 
  - Portale Azure → Function App → Nome della Function App
  - Oppure dal comando: `az functionapp list --query "[].name" -o table`

#### 2. `AZURE_RESOURCE_GROUP`
- **Descrizione**: Nome del Resource Group che contiene la Function App
- **Esempio**: `rg-salesforce-sentinel`
- **Come ottenerlo**: 
  - Portale Azure → Resource Groups → Nome del Resource Group
  - Oppure dal comando: `az group list --query "[].name" -o table`

#### 3. `AZURE_CREDENTIALS` ⚠️ IMPORTANTE
- **Descrizione**: Credenziali Azure Service Principal (JSON completo)
- **Formato**: JSON completo con tutte le proprietà
- **Come crearlo**:
  ```bash
  # Login ad Azure
  az login
  
  # Sostituisci {subscription-id} e {resource-group-name} con i tuoi valori
  az ad sp create-for-rbac --name "github-actions-salesforce-sentinel" \
    --role contributor \
    --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} \
    --sdk-auth
  ```
- **Output esempio**:
  ```json
  {
    "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
    "resourceManagerEndpointUrl": "https://management.azure.com/",
    "activeDirectoryGraphResourceId": "https://graph.windows.net/",
    "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
    "galleryEndpointUrl": "https://gallery.azure.com/",
    "managementEndpointUrl": "https://management.core.windows.net/"
  }
  ```
- **⚠️ IMPORTANTE**: Copia l'intero JSON come valore del secret (senza formattazione)

#### 4. `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
- **Descrizione**: Publish Profile della Function App (contenuto XML)
- **Formato**: Contenuto completo del file XML
- **Come ottenerlo**:
  1. Portale Azure → Function App
  2. Clicca su **Get publish profile** (pulsante in alto)
  3. Si scarica un file `.PublishSettings`
  4. Apri il file e copia tutto il contenuto XML
- **⚠️ IMPORTANTE**: Copia tutto il contenuto XML, non solo una parte

---

### 🟢 Salesforce Secrets (5 secrets)

#### 5. `SALESFORCE_CONSUMER_KEY`
- **Descrizione**: Consumer Key (Client ID) della Connected App Salesforce
- **Come ottenerlo**:
  1. Salesforce → Setup → App Manager
  2. Trova la Connected App creata (o creane una nuova)
  3. Clicca sulla Connected App
  4. Vai a **API (Enable OAuth Settings)** → **View**
  5. Copia il valore di **Consumer Key**

#### 6. `SALESFORCE_CONSUMER_SECRET`
- **Descrizione**: Consumer Secret (Client Secret) della Connected App Salesforce
- **Come ottenerlo**:
  1. Salesforce → Setup → App Manager
  2. Trova la Connected App
  3. Clicca sulla Connected App
  4. Vai a **API (Enable OAuth Settings)** → **View**
  5. Clicca su **Click to reveal** accanto a **Consumer Secret**
  6. Copia il valore

#### 7. `SALESFORCE_USERNAME`
- **Descrizione**: Username Salesforce per l'autenticazione
- **Formato**: Email o username Salesforce
- **Esempio**: `user@example.com` o `username@company.com.sandbox`

#### 8. `SALESFORCE_PASSWORD`
- **Descrizione**: Password Salesforce
- **⚠️ IMPORTANTE**: Password in chiaro (non includere il Security Token qui)

#### 9. `SALESFORCE_SECURITY_TOKEN`
- **Descrizione**: Security Token Salesforce
- **Come ottenerlo**:
  1. Salesforce → Setup → My Personal Information → Reset My Security Token
  2. Clicca su **Reset Security Token**
  3. Il token verrà inviato via email all'indirizzo associato all'account
  4. Copia il token dall'email
- **⚠️ NOTA**: Se non ricevi l'email, verifica le impostazioni email in Salesforce

---

### 🟡 Log Analytics Secrets (3 secrets)

#### 10. `LOG_ANALYTICS_WORKSPACE_ID`
- **Descrizione**: Workspace ID di Azure Log Analytics
- **Formato**: GUID (es. `12345678-1234-1234-1234-123456789012`)
- **Come ottenerlo**:
  1. Portale Azure → Log Analytics workspaces
  2. Seleziona il workspace
  3. Vai a **Overview**
  4. Copia il valore di **Workspace ID**

#### 11. `LOG_ANALYTICS_WORKSPACE_KEY`
- **Descrizione**: Primary Key (Workspace Key) di Azure Log Analytics
- **Come ottenerlo**:
  1. Portale Azure → Log Analytics workspaces
  2. Seleziona il workspace
  3. Vai a **Agents management** → **Log Analytics agent instructions**
  4. Copia il valore di **Primary key**
- **⚠️ ALTERNATIVA**: 
  ```bash
  az monitor log-analytics workspace get-shared-keys \
    --resource-group {resource-group} \
    --workspace-name {workspace-name} \
    --query primarySharedKey -o tsv
  ```

#### 12. `LOG_ANALYTICS_LOG_TYPE` (OPZIONALE)
- **Descrizione**: Nome della tabella custom in Log Analytics
- **Default**: `Salesforce_CL` (se non specificato)
- **Esempio**: `Salesforce_CL`, `SalesforceEvents_CL`, ecc.
- **⚠️ NOTA**: Questo secret è opzionale. Se non lo configuri, verrà usato `Salesforce_CL`

---

## 📝 Riepilogo Totale

| # | Secret Name | Obbligatorio | Categoria |
|---|-------------|--------------|-----------|
| 1 | `AZURE_FUNCTIONAPP_NAME` | ✅ Sì | Azure |
| 2 | `AZURE_RESOURCE_GROUP` | ✅ Sì | Azure |
| 3 | `AZURE_CREDENTIALS` | ✅ Sì | Azure |
| 4 | `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` | ✅ Sì | Azure |
| 5 | `SALESFORCE_CONSUMER_KEY` | ✅ Sì | Salesforce |
| 6 | `SALESFORCE_CONSUMER_SECRET` | ✅ Sì | Salesforce |
| 7 | `SALESFORCE_USERNAME` | ✅ Sì | Salesforce |
| 8 | `SALESFORCE_PASSWORD` | ✅ Sì | Salesforce |
| 9 | `SALESFORCE_SECURITY_TOKEN` | ✅ Sì | Salesforce |
| 10 | `LOG_ANALYTICS_WORKSPACE_ID` | ✅ Sì | Log Analytics |
| 11 | `LOG_ANALYTICS_WORKSPACE_KEY` | ✅ Sì | Log Analytics |
| 12 | `LOG_ANALYTICS_LOG_TYPE` | ❌ No | Log Analytics |

**Totale**: 11 secrets obbligatori + 1 opzionale

---

## 🚀 Come Configurare i Secrets

1. Vai al repository GitHub
2. Clicca su **Settings** (in alto nel repository)
3. Nel menu laterale, clicca su **Secrets and variables** → **Actions**
4. Clicca su **New repository secret**
5. Per ogni secret:
   - **Name**: Inserisci esattamente il nome del secret (es. `AZURE_FUNCTIONAPP_NAME`)
   - **Secret**: Incolla il valore
   - Clicca su **Add secret**
6. Ripeti per tutti i secrets

---

## ✅ Verifica Configurazione

Dopo aver configurato tutti i secrets, puoi verificare:

1. Vai a **Settings** → **Secrets and variables** → **Actions**
2. Dovresti vedere tutti i secrets nella lista
3. Verifica che i nomi siano esatti (case-sensitive)

---

## 🔒 Sicurezza

⚠️ **IMPORTANTE**:
- Non committare mai i secrets nel codice
- Non condividere i secrets pubblicamente
- Usa sempre GitHub Secrets per valori sensibili
- Considera l'uso di Azure Key Vault per gestire i secrets in produzione
- Ruota periodicamente i secrets (specialmente `AZURE_CREDENTIALS` e `SALESFORCE_CONSUMER_SECRET`)

---

## 🆘 Troubleshooting

### Secret non riconosciuto
- Verifica che il nome del secret sia esatto (case-sensitive)
- Verifica che non ci siano spazi extra nel nome

### Deployment fallisce con errore di autenticazione
- Verifica che `AZURE_CREDENTIALS` contenga l'intero JSON
- Verifica che `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` contenga tutto il contenuto XML

### Errore "Function app not found"
- Verifica che `AZURE_FUNCTIONAPP_NAME` corrisponda esattamente al nome della Function App
- Verifica che `AZURE_RESOURCE_GROUP` sia corretto

### Errore "Invalid credentials" da Salesforce
- Verifica che `SALESFORCE_USERNAME` e `SALESFORCE_PASSWORD` siano corretti
- Verifica che `SALESFORCE_SECURITY_TOKEN` sia valido (potrebbe essere scaduto)
- Verifica che la Connected App sia configurata correttamente

---

## 📚 Riferimenti

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure Service Principal](https://learn.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal)
- [Salesforce Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm)
- [Log Analytics Workspace Keys](https://learn.microsoft.com/azure/azure-monitor/logs/access-workspace-authentication)




