# Configurazione Azure Deployment Center

## Problema: requirements.txt non trovato

Se il Deployment Center cerca `requirements.txt` nella root del repository invece che in `azure-function/salesforce-sentinel-polling/`, devi configurare il Deployment Center per usare la directory corretta.

## Soluzione: Configurare il Deployment Center

### Opzione 1: Tramite Azure Portal (Consigliato)

**Metodo A: Configurazione nel Deployment Center**

1. Vai al **Portale Azure** → Function App
2. Vai a **Deployment Center**
3. Se hai già configurato GitHub come source:
   - Clicca su **Settings** (icona ingranaggio) o **Edit**
   - Cerca il campo **Working Directory**, **Project Path**, o **Root Directory**
   - Imposta il valore a: `azure-function/salesforce-sentinel-polling`
   - Salva le modifiche
4. Se non trovi questa opzione, vai al **Metodo B**

**Metodo B: Configurazione tramite Application Settings**

1. Vai al **Portale Azure** → Function App
2. Vai a **Configuration** → **Application settings**
3. Clicca su **+ New application setting**
4. Aggiungi:
   - **Name**: `SCM_REPOSITORY_PATH`
   - **Value**: `azure-function/salesforce-sentinel-polling`
5. Clicca su **OK** e poi su **Save**
6. Riavvia la Function App se necessario

**Nota**: Il workflow GitHub Actions configura automaticamente questa setting, ma puoi verificarla o configurarla manualmente se necessario.

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

