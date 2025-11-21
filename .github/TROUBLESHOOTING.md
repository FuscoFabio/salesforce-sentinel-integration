# Troubleshooting GitHub Actions Workflow

## Errore: AZURE_CREDENTIALS is not valid JSON

### Problema
Il workflow fallisce con l'errore: `AZURE_CREDENTIALS is not valid JSON`

### Cause comuni
1. **JSON incompleto**: Il JSON è stato copiato parzialmente (manca `{` iniziale o `}` finale)
2. **Caratteri extra**: Sono stati aggiunti spazi, newline o caratteri speciali
3. **Formato errato**: Il JSON non è nel formato corretto per Azure SDK Auth

### Soluzione passo-passo

#### 1. Genera il JSON corretto

Esegui questi comandi in Azure CLI:

```bash
# Accedi ad Azure
az login

# Sostituisci {subscription-id} e {resource-group} con i tuoi valori
az ad sp create-for-rbac \
  --name "github-actions-salesforce-sentinel" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

**Esempio con valori reali:**
```bash
az ad sp create-for-rbac \
  --name "github-actions-salesforce-sentinel" \
  --role contributor \
  --scopes /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-salesforce-sentinel \
  --sdk-auth
```

#### 2. Copia l'intero output

L'output dovrebbe essere simile a:

```json
{
  "clientId": "xxxx-xxxx-xxxx-xxxx",
  "clientSecret": "yyyy-yyyy-yyyy-yyyy",
  "tenantId": "zzzz-zzzz-zzzz-zzzz",
  "subscriptionId": "aaaa-aaaa-aaaa-aaaa"
}
```

**IMPORTANTE:**
- Copia **TUTTO** dall'apertura `{` alla chiusura `}`
- Non aggiungere spazi o caratteri extra
- Non aggiungere virgolette esterne
- Se l'output è su più righe, copia tutte le righe

#### 3. Configura il secret su GitHub

1. Vai su: `https://github.com/{tuo-username}/{tuo-repo}/settings/secrets/actions`
2. Cerca il secret `AZURE_CREDENTIALS`
3. Clicca su **Update** (o **New repository secret** se non esiste)
4. Incolla l'intero JSON nel campo **Value**
5. Clicca su **Update secret**

#### 4. Verifica il formato

Il JSON deve essere valido. Puoi verificarlo con:

```bash
# Salva il JSON in un file
echo '{
  "clientId": "xxxx",
  "clientSecret": "yyyy",
  "tenantId": "zzzz",
  "subscriptionId": "aaaa"
}' > test.json

# Valida il JSON
python3 -m json.tool test.json
```

Se il comando non mostra errori, il JSON è valido.

### Verifica rapida

Dopo aver configurato il secret, il workflow dovrebbe:
1. ✅ Validare il JSON
2. ✅ Verificare che contenga i campi necessari (`clientId`, `clientSecret`, `tenantId`, `subscriptionId`)
3. ✅ Eseguire il login ad Azure

### Problemi comuni

#### Il JSON è valido ma manca un campo
Se vedi un errore tipo `missing 'clientId' field`, verifica che il JSON contenga tutti e 4 i campi:
- `clientId`
- `clientSecret`
- `tenantId`
- `subscriptionId`

#### Il JSON contiene caratteri nascosti
Se hai copiato da un editor che aggiunge caratteri speciali:
1. Genera di nuovo il JSON con `az ad sp create-for-rbac --sdk-auth`
2. Copia direttamente dal terminale (non da un editor)
3. Incolla direttamente nel secret di GitHub

#### Il Service Principal esiste già
Se vedi un errore `Service principal already exists`, puoi:
1. Eliminare il service principal esistente:
   ```bash
   az ad sp delete --id "github-actions-salesforce-sentinel"
   ```
2. Oppure usare un nome diverso:
   ```bash
   az ad sp create-for-rbac --name "github-actions-salesforce-sentinel-2" ...
   ```

### Supporto

Se il problema persiste:
1. Controlla i log del workflow per vedere l'errore JSON specifico
2. Verifica che il JSON sia valido usando `python3 -m json.tool`
3. Rigenera il JSON seguendo i passaggi sopra

