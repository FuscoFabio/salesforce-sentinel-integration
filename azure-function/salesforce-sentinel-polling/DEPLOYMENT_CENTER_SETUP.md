# Configurazione Azure Deployment Center

## Problema: requirements.txt non trovato

Se il Deployment Center cerca `requirements.txt` nella root del repository invece che in `azure-function/salesforce-sentinel-polling/`, devi configurare il Deployment Center per usare la directory corretta.

## Soluzione: Configurare il Deployment Center

### Opzione 1: Tramite Azure Portal (Consigliato)

1. Vai al **Portale Azure** → Function App
2. Vai a **Deployment Center**
3. Nella sezione **Settings**, cerca **Application Settings** o **Build Settings**
4. Imposta **Working Directory** o **Project Path** a: `azure-function/salesforce-sentinel-polling`
5. Salva le modifiche

### Opzione 2: Tramite Azure CLI

```bash
az functionapp config appsettings set \
  --name <function-app-name> \
  --resource-group <resource-group> \
  --settings \
    SCM_REPOSITORY_PATH="azure-function/salesforce-sentinel-polling"
```

### Opzione 3: Tramite Application Settings

Aggiungi questa Application Setting nella Function App:

- **Nome**: `SCM_REPOSITORY_PATH`
- **Valore**: `azure-function/salesforce-sentinel-polling`

## Verifica

Dopo aver configurato, il Deployment Center dovrebbe:
1. Trovare `requirements.txt` in `azure-function/salesforce-sentinel-polling/`
2. Eseguire correttamente il build con Oryx
3. Deployare la function app senza errori

## Note

- Il file `.deployment` nella root del repository potrebbe non essere sufficiente per Azure Functions
- Azure Functions usa Oryx per il build, che cerca i file nella directory specificata
- Se il problema persiste, verifica che la directory `azure-function/salesforce-sentinel-polling/` contenga:
  - `function_app.py`
  - `requirements.txt`
  - `host.json`

