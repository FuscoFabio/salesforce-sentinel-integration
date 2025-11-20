# Setup GitHub Actions per Deployment Automatico

Guida rapida per configurare il deployment automatico tramite GitHub Actions.

## Prerequisiti

1. Repository GitHub configurato
2. Azure Function App creata su Azure
3. Accesso alle credenziali Salesforce e Log Analytics

## Passo 1: Creare Azure Function App

Se non hai ancora creato la Function App:

```bash
# Login ad Azure
az login

# Crea resource group
az group create --name rg-salesforce-sentinel --location westeurope

# Crea storage account
az storage account create \
  --name stsalesforcesentinel \
  --resource-group rg-salesforce-sentinel \
  --location westeurope \
  --sku Standard_LRS

# Crea Function App
az functionapp create \
  --resource-group rg-salesforce-sentinel \
  --consumption-plan-location westeurope \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name salesforce-sentinel-001 \
  --storage-account stsalesforcesentinel \
  --os-type Linux
```

**Nota**: Sostituisci `salesforce-sentinel-001` con un nome univoco per la tua Function App.

## Passo 2: Ottenere Publish Profile

1. Vai al [Portale Azure](https://portal.azure.com)
2. Cerca la Function App creata
3. Clicca su **Get publish profile** (pulsante in alto)
4. Salva il file XML (lo userai come secret)

## Passo 3: Configurare Secrets su GitHub

1. Vai al repository GitHub
2. Clicca su **Settings** → **Secrets and variables** → **Actions**
3. Clicca su **New repository secret**

Aggiungi i seguenti secrets:

### Azure Secrets

| Secret Name | Valore | Come ottenerlo |
|------------|--------|----------------|
| `AZURE_FUNCTIONAPP_NAME` | Nome della Function App | Es. `salesforce-sentinel-001` |
| `AZURE_RESOURCE_GROUP` | Nome del Resource Group | Es. `rg-salesforce-sentinel` |
| `AZURE_CREDENTIALS` | JSON Service Principal | Vedi istruzioni sotto |
| `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` | Contenuto del file XML | Portale Azure → Function App → Get publish profile |

**Come creare AZURE_CREDENTIALS:**

1. Login ad Azure:
   ```bash
   az login
   ```

2. Crea Service Principal:
   ```bash
   az ad sp create-for-rbac --name "github-actions-salesforce-sentinel" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} \
     --sdk-auth
   ```

3. Sostituisci:
   - `{subscription-id}`: ID della tua sottoscrizione Azure
   - `{resource-group-name}`: Nome del resource group (es. `rg-salesforce-sentinel`)

4. Copia l'output JSON completo e incollalo come valore del secret `AZURE_CREDENTIALS`

**Esempio output:**
```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### Salesforce Secrets

| Secret Name | Valore | Come ottenerlo |
|------------|--------|----------------|
| `SALESFORCE_CONSUMER_KEY` | Consumer Key | Setup → App Manager → Connected App |
| `SALESFORCE_CONSUMER_SECRET` | Consumer Secret | Setup → App Manager → Connected App |
| `SALESFORCE_USERNAME` | Username Salesforce | Il tuo username Salesforce |
| `SALESFORCE_PASSWORD` | Password Salesforce | La tua password Salesforce |
| `SALESFORCE_SECURITY_TOKEN` | Security Token | Setup → My Personal Information → Reset Security Token |

### Log Analytics Secrets

| Secret Name | Valore | Come ottenerlo |
|------------|--------|----------------|
| `LOG_ANALYTICS_WORKSPACE_ID` | Workspace ID | Portale Azure → Log Analytics → Overview → Workspace ID |
| `LOG_ANALYTICS_WORKSPACE_KEY` | Primary Key | Portale Azure → Log Analytics → Agents management → Primary key |

### Opzionale

| Secret Name | Valore | Default |
|------------|--------|---------|
| `LOG_ANALYTICS_LOG_TYPE` | Nome tabella custom | `Salesforce_CL` |

## Passo 4: Verificare Workflow

1. Vai a **Actions** nel repository GitHub
2. Verifica che il workflow `deploy-azure-function.yml` sia presente
3. Il workflow si attiverà automaticamente su push al branch `main`

## Passo 5: Test Deployment

### Opzione A: Push al Branch Main

```bash
# Assicurati di essere sul branch corretto
git checkout main

# Merge del branch feature
git merge feature/salesforce-polling-python-function

# Push
git push origin main
```

### Opzione B: Deployment Manuale

1. Vai a **Actions** → **Deploy Azure Function - Salesforce Sentinel Polling**
2. Clicca su **Run workflow**
3. Seleziona il branch (es. `feature/salesforce-polling-python-function`)
4. Seleziona l'ambiente (`production`)
5. Clicca su **Run workflow**

## Passo 6: Verificare Deployment

1. **Verifica Workflow:**
   - Vai a **Actions** → Seleziona il workflow run
   - Verifica che tutti gli step siano completati con successo (✓)

2. **Verifica Function App:**
   - Portale Azure → Function App
   - Vai a **Functions** → Verifica che `salesforce-sentinel-polling` sia presente
   - Vai a **Configuration** → Verifica che le Application Settings siano configurate

3. **Test Function:**
   - Portale Azure → Function App → Functions → `salesforce-sentinel-polling`
   - Clicca su **Test/Run** per eseguire manualmente
   - Verifica i logs in **Monitor**

4. **Verifica Logs:**
   ```bash
   # Stream logs
   az functionapp log tail \
     --name salesforce-sentinel-001 \
     --resource-group rg-salesforce-sentinel
   ```

## Troubleshooting

### Workflow non si attiva

**Causa**: Il workflow è configurato per attivarsi solo su push al branch `main` o modifiche nella cartella `azure-function/salesforce-sentinel-polling/`.

**Soluzione**: 
- Verifica di essere sul branch corretto
- Verifica che i file modificati siano nella cartella corretta
- Usa deployment manuale se necessario

### Errore: "Publish profile not found"

**Causa**: Secret `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` non configurato correttamente.

**Soluzione**: 
- Verifica che il secret contenga l'intero contenuto del file XML
- Scarica nuovamente il publish profile dalla Function App

### Errore: "Function app not found"

**Causa**: Secret `AZURE_FUNCTIONAPP_NAME` non corrisponde al nome reale della Function App.

**Soluzione**: 
- Verifica il nome esatto della Function App su Azure
- Aggiorna il secret con il nome corretto

### Errore: "Application settings update failed"

**Causa**: Uno o più secrets mancanti o non validi.

**Soluzione**: 
- Verifica che tutti i secrets richiesti siano configurati
- Controlla che i valori siano corretti (senza spazi extra, caratteri speciali, ecc.)

## Prossimi Passi

Dopo il deployment riuscito:

1. ✅ Verifica che la function esegua correttamente
2. ✅ Monitora i logs in Application Insights
3. ✅ Verifica che gli eventi arrivino in Log Analytics
4. ✅ Configura alert in Azure Sentinel
5. ✅ Configura branch protection per `main` (consigliato)

## Riferimenti

- [Workflow README](../../.github/workflows/README.md)
- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [README.md](./README.md)

