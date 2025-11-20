# Guida al Deployment

Guida passo-passo per il deployment dell'Azure Function su Azure.

## Prerequisiti

- Azure CLI installato e configurato
- Azure Functions Core Tools v4
- Python 3.9 o superiore
- Accesso ad Azure Subscription con permessi per creare risorse

## Opzione 1: Deployment tramite Azure Portal

### 1. Creare Function App

1. Accedi al [Portale Azure](https://portal.azure.com)
2. Cerca "Function App" e clicca su **Create**
3. Compila i campi:
   - **Subscription**: Seleziona la sottoscrizione
   - **Resource Group**: Crea o seleziona un resource group
   - **Function App name**: Nome univoco (es. `salesforce-sentinel-001`)
   - **Publish**: Code
   - **Runtime stack**: Python
   - **Version**: 3.9, 3.10 o 3.11
   - **Region**: Seleziona una regione
   - **Plan Type**: Consumption (serverless) o Premium
4. Clicca su **Review + Create** → **Create**

### 2. Configurare Application Settings

1. Vai alla Function App creata
2. Vai a **Configuration** → **Application settings**
3. Aggiungi le seguenti variabili:

```
Salesforce__ConsumerKey=<your-consumer-key>
Salesforce__ConsumerSecret=<your-consumer-secret>
Salesforce__Username=<salesforce-username>
Salesforce__Password=<salesforce-password>
Salesforce__SecurityToken=<security-token>
Salesforce__AuthMode=password
Salesforce__LoginUrl=https://login.salesforce.com
Salesforce__JwtPrivateKey=<base64-o-PEM>
Salesforce__JwtPrivateKeyPath=/path/to/key.pem
Salesforce__JwtAudience=https://login.salesforce.com
Salesforce__JwtSubject=<integration-user@company.com>
Salesforce__JwtLifetimeSeconds=300
LogAnalytics__WorkspaceId=<workspace-id>
LogAnalytics__WorkspaceKey=<workspace-key>
LogAnalytics__LogType=Salesforce_CL
Environment__Name=dev
Checkpoint__StorageConnectionString=<storage-connection-string>
Checkpoint__TableName=SalesforceCheckpoints
Checkpoint__PartitionKey=Salesforce
Checkpoint__RowKey=EventLogPolling
Checkpoint__OverlapMinutes=5
Checkpoint__FallbackHours=24
```

> Usa nomi diversi per `LogAnalytics__LogType` e/o `Environment__Name` (ad es. `SalesforceTest_CL`, `Environment__Name=prod`) per distinguere i tre ambienti pur condividendo lo stesso workspace Sentinel.

Per abilitare l'autenticazione tramite certificato imposta `Salesforce__AuthMode=jwt`, carica il certificato X.509 nella Connected App e fornisci la chiave privata tramite `Salesforce__JwtPrivateKey` (PEM/base64) oppure `Salesforce__JwtPrivateKeyPath`. La variabile `Salesforce__JwtSubject` indica l'utente Salesforce da impersonare (default `Salesforce__Username`), mentre `Salesforce__JwtAudience` deve combaciare con il dominio di login (es. `https://test.salesforce.com` per sandbox).

4. Clicca su **Save**

### 3. Deploy Codice

1. Vai a **Deployment Center**
2. Seleziona **Local Git** o **GitHub** come source
3. Segui le istruzioni per connettere il repository
4. Il codice verrà deployato automaticamente

## Opzione 2: Deployment tramite Azure Functions Core Tools

### 1. Installare Azure Functions Core Tools

```bash
# Windows (con Chocolatey)
choco install azure-functions-core-tools-4

# macOS (con Homebrew)
brew tap azure/functions
brew install azure-functions-core-tools@4

# Linux
# Vedi: https://github.com/Azure/azure-functions-core-tools
```

### 2. Login ad Azure

```bash
az login
az account set --subscription "<subscription-id>"
```

### 3. Creare Function App (se non esiste)

```bash
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

### 4. Configurare Application Settings

```bash
az functionapp config appsettings set \
  --name salesforce-sentinel-001 \
  --resource-group rg-salesforce-sentinel \
  --settings \
    "Salesforce__ConsumerKey=<your-consumer-key>" \
    "Salesforce__ConsumerSecret=<your-consumer-secret>" \
    "Salesforce__Username=<salesforce-username>" \
    "Salesforce__Password=<salesforce-password>" \
    "Salesforce__SecurityToken=<security-token>" \
    "Salesforce__AuthMode=password" \
    "Salesforce__LoginUrl=https://login.salesforce.com" \
    "Salesforce__JwtPrivateKey=<base64-o-PEM>" \
    "Salesforce__JwtPrivateKeyPath=/path/to/key.pem" \
    "Salesforce__JwtAudience=https://login.salesforce.com" \
    "Salesforce__JwtSubject=<integration-user@company.com>" \
    "Salesforce__JwtLifetimeSeconds=300" \
    "LogAnalytics__WorkspaceId=<workspace-id>" \
    "LogAnalytics__WorkspaceKey=<workspace-key>" \
    "LogAnalytics__LogType=Salesforce_CL" \
    "Environment__Name=dev" \
    "Checkpoint__StorageConnectionString=<storage-connection-string>" \
    "Checkpoint__TableName=SalesforceCheckpoints" \
    "Checkpoint__PartitionKey=Salesforce" \
    "Checkpoint__RowKey=EventLogPolling" \
    "Checkpoint__OverlapMinutes=5" \
    "Checkpoint__FallbackHours=24"
```

### 5. Deploy Function

```bash
# Naviga nella cartella della function
cd azure-function/salesforce-sentinel-polling

# Deploy
func azure functionapp publish salesforce-sentinel-001
```

## Opzione 3: Deployment tramite VS Code

### 1. Installare Estensioni

1. Installa estensione "Azure Functions" per VS Code
2. Installa estensione "Azure Account" per VS Code

### 2. Login ad Azure

1. Apri Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Esegui "Azure: Sign In"
3. Segui le istruzioni per autenticarti

### 3. Deploy

1. Apri la cartella `azure-function/salesforce-sentinel-polling`
2. Apri Command Palette
3. Esegui "Azure Functions: Deploy to Function App"
4. Seleziona subscription, resource group e Function App (o creane una nuova)

## Opzione 4: Deployment tramite Azure DevOps Pipelines (CI/CD) ⭐ CONSIGLIATO

### 1. Pipeline

- Il file `azure-pipelines.yml` contiene la pipeline multi-stage (Build, Deploy Dev, Deploy Collaudo, Deploy Prod).
- Ogni stage usa il task `AzureFunctionApp@1` per pubblicare la cartella `azure-function/salesforce-sentinel-polling`.

### 2. Prerequisiti Azure DevOps

1. Crea un **Service Connection** Azure (tipo `Azure Resource Manager`) con accesso alle tre Function App.
2. (Opzionale) Configura **Variable Group** o Library per salvare valori sensibili (es. nomi Function App).
3. Definisci gli **ambienti** Dev/Test/Prod in Azure DevOps per abilitarne le approvazioni manuali.

### 3. Configurazione pipeline

- Aggiorna le variabili in testa al file:
  - `azureServiceConnection`: nome del service connection creato.
  - `devFunctionApp`, `testFunctionApp`, `prodFunctionApp`: nomi reali delle Function App.
  - `functionProjectPath`: percorso del progetto (default `azure-function/salesforce-sentinel-polling`).
- Se hai bisogno di secrets runtime (Salesforce/Log Analytics), configurali direttamente nelle Function App oppure in Key Vault; la pipeline non li gestisce direttamente.

### 4. Esecuzione

- La pipeline si avvia automaticamente su push al branch `main`.
- Gli stage di Collaudo e Produzione sono deployment jobs legati agli ambienti Azure DevOps, quindi puoi impostare approvazioni o controlli manuali prima del rilascio.
- Per avviare manualmente una run, usa **Pipelines → Run pipeline** e seleziona il branch desiderato.

## Verifica Deployment

### 1. Verificare Function Deployata

```bash
# Lista functions
az functionapp function list \
  --name salesforce-sentinel-001 \
  --resource-group rg-salesforce-sentinel
```

### 2. Verificare Logs

```bash
# Stream logs
az functionapp log tail \
  --name salesforce-sentinel-001 \
  --resource-group rg-salesforce-sentinel
```

### 3. Testare Function

1. Vai al portale Azure → Function App
2. Vai a **Functions** → `salesforce-sentinel-polling`
3. Clicca su **Test/Run** per eseguire manualmente
4. Verifica i logs in **Monitor**

## Configurazione Avanzata

### Application Insights

1. Vai a Function App → **Application Insights**
2. Crea o collega un Application Insights resource
3. I log e metriche verranno automaticamente inviati

### Private Endpoints (Sicurezza)

1. Vai a Function App → **Networking**
2. Configura **Private Endpoints** per isolare la function
3. Vedi [Network e Sicurezza](../../docs/implementation/network-sicurezza.md) per dettagli

### Key Vault Integration (Sicurezza Credenziali)

1. Crea Azure Key Vault
2. Salva le credenziali in Key Vault
3. Configura Managed Identity per Function App
4. Usa Key Vault References nelle Application Settings:

```
Salesforce__ConsumerKey=@Microsoft.KeyVault(SecretUri=https://kv-name.vault.azure.net/secrets/sf-consumer-key/)
```

## Troubleshooting Deployment

### Errore: "Function runtime is unable to start"

**Causa**: Dipendenze mancanti o versione Python non supportata.

**Soluzione**: 
- Verifica che `requirements.txt` sia presente
- Verifica versione Python nella Function App (3.9+)

### Errore: "Module not found"

**Causa**: Dipendenze non installate correttamente.

**Soluzione**:
- Verifica che `requirements.txt` contenga tutte le dipendenze
- Riavvia la Function App dopo il deploy

### Errore: "Timer trigger not firing"

**Causa**: Timer non configurato correttamente o function non abilitata.

**Soluzione**:
- Verifica che la function sia abilitata
- Verifica la cron expression nel codice
- Controlla i logs per errori

## Prossimi Passi

Dopo il deployment:
1. Verifica che la function esegua correttamente
2. Monitora i logs in Application Insights
3. Verifica che gli eventi arrivino in Log Analytics
4. Configura alert in Azure Sentinel
5. Valuta le strategie di scaling-out descritte in `docs/implementation/scaling-out.md` per gestire volumi crescenti
6. Consulta `docs/implementation/low-level-design.md` per i dettagli architetturali e le dipendenze Azure da mantenere allineate tra gli ambienti

## Riferimenti

- [Azure Functions Deployment](https://learn.microsoft.com/azure/azure-functions/functions-deployment-technologies)
- [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)
- [Azure Pipelines - Deploy Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-how-to-azure-devops)

