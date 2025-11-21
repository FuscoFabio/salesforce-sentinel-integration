# GitHub Actions Workflows

Questo repository contiene workflow GitHub Actions per il deployment automatico dell'Azure Function.

## Workflow Disponibili

### deploy-azure-function.yml

Workflow per il deployment automatico dell'Azure Function `salesforce-sentinel-polling` su Azure.

**Trigger:**
- Push su branch `main` o `feature/salesforce-polling-python-function`
- Modifiche ai file nella cartella `azure-function/salesforce-sentinel-polling/`
- Esecuzione manuale tramite GitHub Actions UI

**Ambienti:**
- `production`: Ambiente di produzione
- `staging`: Ambiente di staging (se configurato)

## Configurazione Secrets

Per utilizzare questo workflow, configura i seguenti secrets nel repository GitHub:

### Secrets Richiesti

1. **AZURE_FUNCTIONAPP_NAME**
   - Nome della Function App su Azure
   - Esempio: `salesforce-sentinel-001`

2. **AZURE_RESOURCE_GROUP**
   - Nome del Resource Group che contiene la Function App
   - Esempio: `rg-salesforce-sentinel`

3. **AZURE_CREDENTIALS**
   - Credenziali Azure per l'autenticazione (Service Principal)
   - Come crearlo:
     ```bash
     az ad sp create-for-rbac --name "github-actions-sp" \
       --role contributor \
       --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
       --sdk-auth
     ```
   - Copia l'output JSON completo come secret

4. **AZURE_FUNCTIONAPP_PUBLISH_PROFILE**
   - Publish Profile della Function App
   - Come ottenerlo:
     1. Portale Azure → Function App
     2. Clicca su "Get publish profile"
     3. Copia il contenuto del file XML

3. **SALESFORCE_CONSUMER_KEY**
   - Consumer Key (Client ID) della Connected App Salesforce

4. **SALESFORCE_CONSUMER_SECRET**
   - Consumer Secret (Client Secret) della Connected App Salesforce

5. **SALESFORCE_USERNAME**
   - Username Salesforce per l'autenticazione

6. **SALESFORCE_PASSWORD**
   - Password Salesforce

7. **SALESFORCE_SECURITY_TOKEN**
   - Security Token Salesforce

8. **LOG_ANALYTICS_WORKSPACE_ID**
   - Workspace ID di Azure Log Analytics

9. **LOG_ANALYTICS_WORKSPACE_KEY**
   - Primary Key di Azure Log Analytics

### Secrets Opzionali

10. **LOG_ANALYTICS_LOG_TYPE**
    - Nome della tabella custom in Log Analytics
    - Default: `Salesforce_CL`

## Come Configurare i Secrets

1. Vai al repository GitHub
2. Clicca su **Settings** → **Secrets and variables** → **Actions**
3. Clicca su **New repository secret**
4. Aggiungi ogni secret con il nome e valore corrispondente
5. Clicca su **Add secret**

## Deployment Manuale

Per eseguire un deployment manuale:

1. Vai a **Actions** nel repository GitHub
2. Seleziona il workflow "Deploy Azure Function - Salesforce Sentinel Polling"
3. Clicca su **Run workflow**
4. Seleziona il branch e l'ambiente
5. Clicca su **Run workflow**

## Monitoraggio Deployment

Dopo ogni deployment:

1. Vai a **Actions** per vedere lo stato del workflow
2. Clicca sul workflow run per vedere i dettagli
3. Verifica i log di ogni step
4. Controlla la Function App su Azure per verificare il deployment

## Troubleshooting

### Errore: "Publish profile not found"

**Causa**: Secret `AZURE_FUNCTIONAPP_PUBLISH_PROFILE` non configurato o non valido.

**Soluzione**: 
- Verifica che il secret sia configurato correttamente
- Scarica nuovamente il publish profile dalla Function App

### Errore: "Function app not found"

**Causa**: Secret `AZURE_FUNCTIONAPP_NAME` non corrisponde al nome della Function App.

**Soluzione**: 
- Verifica che il nome della Function App sia corretto
- Assicurati che la Function App esista su Azure

### Errore: "Build failed"

**Causa**: Errori durante la build delle dipendenze Python.

**Soluzione**: 
- Verifica che `requirements.txt` sia corretto
- Controlla i log del workflow per dettagli sull'errore

### Errore: "Application settings update failed"

**Causa**: Secrets mancanti o non validi.

**Soluzione**: 
- Verifica che tutti i secrets richiesti siano configurati
- Controlla che i valori dei secrets siano corretti

## Sicurezza

⚠️ **Importante**: 
- Non committare mai i secrets nel codice
- Usa sempre GitHub Secrets per valori sensibili
- Considera l'uso di Azure Key Vault per gestire i secrets in produzione
- Abilita branch protection per il branch `main`

## Riferimenti

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Functions Action](https://github.com/Azure/functions-action)
- [Azure App Service Settings Action](https://github.com/Azure/appservice-settings)

