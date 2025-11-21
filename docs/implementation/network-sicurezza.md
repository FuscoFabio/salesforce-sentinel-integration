# Gestione Network e Sicurezza

Guida per gestire la connettività di rete e la sicurezza quando si configura l'integrazione Salesforce-Azure Sentinel.

## Panoramica

Quando si configura Salesforce per integrare con Azure, è necessario gestire la connettività di rete. Esistono due approcci principali:

1. **Azure Private Endpoints** (⭐ **Consigliato**) - Soluzione più sicura e gestita
2. **Range IP Pubblici Azure** - Soluzione tradizionale che richiede manutenzione

## ⭐ Approccio Consigliato: Azure Private Endpoints

### Perché Usare Private Endpoints

Azure Private Endpoints è l'approccio **consigliato** per le seguenti ragioni:

- ✅ **Sicurezza Superiore**: Comunicazione privata sulla rete Azure, non esposta a Internet
- ✅ **Zero Manutenzione**: Non richiede aggiornamenti periodici dei range IP
- ✅ **Compliance**: Soddisfa requisiti di sicurezza più stringenti
- ✅ **Performance**: Latenza ridotta e throughput ottimizzato
- ✅ **Isolamento**: Traffico isolato dalla rete pubblica
- ✅ **Audit**: Tracciamento completo del traffico di rete

### Come Funzionano i Private Endpoints

I Private Endpoints creano una connessione privata tra:
- La tua risorsa Azure (Function App, Logic App, etc.)
- Salesforce (tramite Azure Private Link)

Il traffico rimane completamente all'interno della rete Azure e non passa attraverso Internet pubblico.

### Quando Usare Private Endpoints

**Usa Private Endpoints se:**
- Hai requisiti di sicurezza elevati
- Vuoi evitare manutenzione periodica
- Hai bisogno di compliance rigorosa
- Il traffico deve rimanere privato
- Hai budget per la configurazione iniziale

**Considera Range IP Pubblici se:**
- Non hai requisiti di sicurezza stringenti
- Hai bisogno di una soluzione rapida e semplice
- Non hai accesso a configurare Private Endpoints
- Il costo è un fattore critico

### Configurazione Private Endpoints per Soluzione

#### Per Azure Function

1. **Crea Virtual Network**:
   ```
   Azure Portal → Virtual Networks → Create
   - Name: vnet-salesforce-integration
   - Address Space: 10.0.0.0/16
   - Subnet: subnet-functions (10.0.1.0/24)
   ```

2. **Configura Function App con VNet Integration**:
   - Function App → Networking → VNet integration
   - Seleziona la VNet e subnet create
   - Abilita "Route All" se necessario

3. **Crea Private Endpoint**:
   - Function App → Networking → Private endpoints
   - Crea nuovo Private Endpoint
   - Connetti alla VNet
   - Configura DNS privato

4. **Configura Salesforce**:
   - In Salesforce, configura la Connected App per accettare connessioni dal Private Endpoint
   - Usa l'IP privato del Private Endpoint invece di range IP pubblici

#### Per Azure Logic App

1. **Crea Integration Service Environment (ISE)**:
   ```
   Azure Portal → Logic Apps → Integration Service Environments → Create
   - Name: ise-salesforce-integration
   - Location: Seleziona regione
   - Network: Crea nuova VNet o usa esistente
   ```

2. **Crea Logic App Standard con ISE**:
   - Quando crei la Logic App, seleziona l'ISE come ambiente
   - La Logic App avrà automaticamente connettività privata

3. **Configura Connettori**:
   - I connettori nell'ISE hanno automaticamente IP privati
   - Configura Salesforce per accettare connessioni dall'ISE

#### Per CCF (CodeLess Connector Framework)

⚠️ **Nota**: Il CCF è un servizio gestito da Microsoft. La configurazione di Private Endpoints dipende dall'infrastruttura Azure Sentinel.

1. **Verifica Supporto Private Endpoints**:
   - Controlla la documentazione Microsoft per il supporto Private Endpoints nel CCF
   - Alcuni connector potrebbero non supportare Private Endpoints direttamente

2. **Alternativa - Azure Private Link per Log Analytics**:
   - Configura Private Link per Log Analytics Workspace
   - Il CCF invierà dati tramite Private Link invece di Internet pubblico

### Costi Private Endpoints

- **Private Endpoint**: ~$0.01/ora (~$7.30/mese)
- **Private DNS Zone**: ~$0.50/mese
- **Data Processing**: Costi standard per il traffico

**Totale stimato**: ~$8-10/mese per Private Endpoint

### Dettagli Tecnici Private Endpoints

#### Architettura Private Endpoint

```
Salesforce API
    ↓
Internet (HTTPS)
    ↓
Azure Private Endpoint (IP Privato nella VNet)
    ↓
Azure Function/Logic App (nella stessa VNet)
    ↓
Log Analytics (tramite Private Link)
```

#### Componenti Necessari

1. **Virtual Network (VNet)**
   - Spazio indirizzi privato (es. 10.0.0.0/16)
   - Subnet dedicata per le risorse
   - Network Security Groups (NSG) per controllo traffico

2. **Private Endpoint**
   - IP privato nella VNet (es. 10.0.1.5)
   - Connessione privata al servizio Azure
   - Non esposto a Internet pubblico

3. **Private DNS Zone**
   - Risoluzione DNS privata
   - Mapping nome servizio → IP privato
   - Integrazione automatica con VNet

4. **Network Security Group (NSG)**
   - Regole di sicurezza per il traffico
   - Filtraggio basato su IP, porta, protocollo
   - Logging e audit

#### Configurazione Dettagliata Private Endpoint

**Passo 1: Creare VNet e Subnet**

```bash
# Azure CLI
az network vnet create \
  --resource-group rg-salesforce-integration \
  --name vnet-salesforce-integration \
  --address-prefix 10.0.0.0/16 \
  --subnet-name subnet-functions \
  --subnet-prefix 10.0.1.0/24
```

**Passo 2: Creare Private DNS Zone**

```bash
# Azure CLI
az network private-dns zone create \
  --resource-group rg-salesforce-integration \
  --name privatelink.azurewebsites.net
```

**Passo 3: Collegare DNS Zone alla VNet**

```bash
# Azure CLI
az network private-dns link vnet create \
  --resource-group rg-salesforce-integration \
  --zone-name privatelink.azurewebsites.net \
  --name link-to-vnet \
  --virtual-network vnet-salesforce-integration \
  --registration-enabled false
```

**Passo 4: Creare Private Endpoint**

```bash
# Azure CLI
az network private-endpoint create \
  --resource-group rg-salesforce-integration \
  --name pe-function-app \
  --vnet-name vnet-salesforce-integration \
  --subnet subnet-functions \
  --private-connection-resource-id /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{function-app-name} \
  --group-id sites \
  --connection-name connection-to-function
```

#### Monitoraggio Private Endpoints

**Query KQL per Monitorare Connettività:**

```kql
// Verifica connessioni Private Endpoint
AzureDiagnostics
| where Category == "PrivateEndpointConnection"
| summarize count() by bin(TimeGenerated, 1h), ConnectionState
| render timechart
```

**Metriche da Monitorare:**
- Stato connessione Private Endpoint
- Latenza delle richieste
- Volume traffico
- Errori di connessione

#### Troubleshooting Private Endpoints

**Problema: Connessione Fallita**
1. Verifica che il Private Endpoint sia in stato "Approved"
2. Controlla le regole NSG
3. Verifica la risoluzione DNS privata
4. Controlla i log di Azure Monitor

**Problema: DNS Non Risolve**
1. Verifica che la Private DNS Zone sia collegata alla VNet
2. Controlla le impostazioni DNS della VNet
3. Verifica che il record DNS sia presente

**Problema: Timeout Connessioni**
1. Verifica che il NSG permetta il traffico necessario
2. Controlla che la subnet abbia spazio IP sufficiente
3. Verifica la latenza di rete

### Best Practices Private Endpoints

1. **DNS Privato**: Usa sempre Azure Private DNS Zones per risoluzione automatica
2. **Network Security Groups**: Configura NSG per limitare il traffico solo a quello necessario
3. **Monitoring**: Monitora la connettività con Azure Monitor e metriche
4. **Backup**: Configura endpoint secondari per alta disponibilità
5. **Documentazione**: Mantieni traccia di tutte le configurazioni (VNet, subnet, NSG)
6. **Tagging**: Usa tag Azure per organizzare le risorse di rete
7. **Naming Convention**: Usa nomi chiari e consistenti (es. `pe-{service}-{env}`)
8. **Access Control**: Limita l'accesso alle risorse di rete con RBAC
9. **Cost Optimization**: Monitora i costi dei Private Endpoints
10. **Testing**: Testa sempre la connettività dopo la configurazione

## Approccio Alternativo: Range IP Pubblici Azure

### Quando Usare Range IP Pubblici

Usa range IP pubblici se:
- Non puoi configurare Private Endpoints
- Hai bisogno di una soluzione rapida
- I requisiti di sicurezza permettono traffico pubblico
- Il budget è limitato

### Perché Gestire i Range IP

- **Sicurezza**: Restringere l'accesso solo da IP Azure autorizzati
- **Compliance**: Soddisfare requisiti di sicurezza aziendali
- **Controllo Accesso**: Prevenire accessi non autorizzati

## Range IP Azure

Azure pubblica i range IP per:
- Azure Functions
- Azure Logic Apps
- Azure Service Bus
- Altri servizi Azure

### Ottenere i Range IP

1. **Download JSON ufficiale**:
   - URL: `https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13F5F5FE99/ServiceTags_Public_20240115.json`
   - Aggiornato settimanalmente

2. **Tramite Azure Portal**:
   - Vai a **Network** → **Service Tags**
   - Cerca "AzureCloud" o servizi specifici

3. **Tramite API**:
   ```bash
   curl https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13F5F5FE99/ServiceTags_Public_20240115.json
   ```

## Configurazione in Salesforce

### Trusted IP Ranges

1. Vai a **Setup** → **Network Access**
2. Clicca su **New** per aggiungere range IP
3. Aggiungi i range IP di Azure per la tua regione
4. Salva le modifiche

### Esempio Range IP per Regioni Comuni

**West Europe**:
- 20.50.0.0/16
- 20.51.0.0/16
- (verifica sempre i range aggiornati)

**East US**:
- 20.42.0.0/16
- 20.43.0.0/16
- (verifica sempre i range aggiornati)

**Nota**: I range IP cambiano regolarmente. Usa sempre i range più recenti.

## Automatizzazione

### Script PowerShell per Aggiornare Range IP

```powershell
# Scarica i Service Tags
$serviceTags = Invoke-RestMethod -Uri "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13F5F5FE99/ServiceTags_Public_20240115.json"

# Filtra per regione (es. WestEurope)
$westEuropeIPs = $serviceTags.values | 
    Where-Object { $_.name -like "*WestEurope*" } | 
    Select-Object -ExpandProperty properties | 
    Select-Object -ExpandProperty addressPrefixes

# Output per configurazione Salesforce
$westEuropeIPs | ForEach-Object { Write-Host $_ }
```

### Script Python

```python
import requests
import json

# Scarica Service Tags
response = requests.get("https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13F5F5FE99/ServiceTags_Public_20240115.json")
data = response.json()

# Filtra per regione
region = "WestEurope"
ip_ranges = []
for value in data['values']:
    if region in value['name']:
        ip_ranges.extend(value['properties']['addressPrefixes'])

# Output
for ip in ip_ranges:
    print(ip)
```

## Best Practices

1. **Aggiornamento Regolare**: I range IP cambiano settimanalmente
2. **Monitoraggio**: Configura alert per cambiamenti nei range IP
3. **Documentazione**: Mantieni traccia dei range IP configurati
4. **Test**: Verifica sempre che la configurazione funzioni dopo aggiornamenti

## Differenze per Soluzione

### CCF (CodeLess Connector Framework)

**Caratteristiche**:
- Connector gestito da Microsoft
- IP dinamici dell'infrastruttura Azure Sentinel
- Range IP molto ampi (tutta l'infrastruttura Azure)

**Configurazione**:
- Se usi range IP: Configura range IP di Azure Cloud per la regione
- Se usi Private Endpoints: Configura Private Link per Log Analytics (se supportato)

**Raccomandazione**: 
- Per sicurezza: Usa Private Link per Log Analytics se disponibile
- Alternativa: Configura range IP Azure Cloud per la regione specifica

### Azure Function

**Caratteristiche**:
- IP dinamici della Function App
- Range IP specifici per regione Azure
- Possibilità di IP statico con App Service Plan Premium

**Configurazione**:
- Se usi range IP: Configura range IP Azure Functions per la regione
- Se usi Private Endpoints: ⭐ **Consigliato** - Configura VNet Integration + Private Endpoint

**Raccomandazione**: 
- ⭐ **Usa Private Endpoints** per massima sicurezza
- Alternativa: Configura range IP Azure Functions per la regione

### Azure Logic App

**Caratteristiche**:
- IP dinamici del servizio Logic Apps
- Range IP specifici per regione
- Con ISE: IP privati dedicati

**Configurazione**:
- Se usi range IP: Configura range IP Azure Logic Apps per la regione
- Se usi Private Endpoints: ⭐ **Consigliato** - Usa Integration Service Environment (ISE)

**Raccomandazione**: 
- ⭐ **Usa ISE** per connettività privata nativa
- Alternativa: Configura range IP Azure Logic Apps per la regione

## Troubleshooting

### Problema: Connessioni Bloccate

1. Verifica che i range IP siano aggiornati
2. Controlla i log di Salesforce per IP bloccati
3. Verifica la regione Azure corretta

### Problema: Range IP Troppo Ampi

- Usa range IP specifici per regione invece di tutti i range Azure
- Considera l'uso di Private Endpoints

## Link Utili

- [Azure IP Ranges and Service Tags](https://www.microsoft.com/download/details.aspx?id=56519)
- [Service Tags Documentation](https://learn.microsoft.com/azure/virtual-network/service-tags-overview)
- [Salesforce Network Access](https://help.salesforce.com/s/articleView?id=sf.security_network_access.htm)

## Fonti

- [Azure Private Link Overview](https://learn.microsoft.com/azure/private-link/private-link-overview)
- [Azure Functions Networking Options](https://learn.microsoft.com/azure/azure-functions/functions-networking-options)
- [Salesforce Network Access](https://help.salesforce.com/s/articleView?id=sf.security_network_access.htm)
- [Azure Monitor Logs Data Collector API](https://learn.microsoft.com/azure/azure-monitor/logs/data-collector-api)

