# Configurazione Salesforce

La configurazione Salesforce è **identica per tutte le soluzioni**.

## Prerequisiti

- Licenza Salesforce Enterprise, Unlimited o Performance Edition
- Event Monitoring abilitato
- Permessi di amministratore per creare Connected App
- Accesso a Setup → Event Monitoring

## Passo 1: Abilitare Event Monitoring

1. Accedi a **Setup** in Salesforce
2. Cerca "Event Monitoring" nella barra di ricerca
3. Vai a **Event Monitoring Settings**
4. Abilita **Event Monitoring** se non già attivo
5. Verifica che **Event Log Files** sia abilitato

## Passo 2: Creare Connected App

1. Vai a **Setup** → **App Manager**
2. Clicca su **New Connected App**
3. Compila i campi obbligatori:
   - **Connected App Name**: Nome descrittivo (es. "Azure Sentinel Integration")
   - **API Name**: Nome API (generato automaticamente)
   - **Contact Email**: La tua email
4. Abilita **Enable OAuth Settings**
5. Configura **Callback URL**: 
   - Per CCF: URL fornito da Azure Sentinel
   - Per Function/Logic App: URL della tua funzione/app
6. Seleziona **OAuth Scopes**:
   - `Manage user data via APIs (api)`
   - `Perform requests on your behalf at any time (refresh_token, offline_access)`
   - `Access the identity URL service (id, profile, email, address, phone)`
7. Abilita **Require Secret for Web Server Flow**
8. Salva e attendi alcuni minuti per la propagazione

## Passo 3: Ottenere Credenziali

Dopo la creazione della Connected App:

1. Vai alla **Connected App** appena creata
2. Clicca su **Manage** → **Edit Policies**
3. Configura le policy di sicurezza:
   - **Permitted Users**: "All users may self-authorize" o "Admin approved users are pre-authorized"
   - **IP Relaxation**: "Relax IP restrictions" (se necessario)
4. Vai a **API (Enable OAuth Settings)** → **View**
5. Copia:
   - **Consumer Key** (Client ID)
   - **Consumer Secret** (Client Secret)

## Passo 4: Configurare Permessi API

1. Vai a **Setup** → **Users** → **Permission Sets**
2. Crea o modifica un Permission Set
3. Aggiungi i permessi necessari:
   - **API Enabled**
   - **View Event Log Files**
4. Assegna il Permission Set agli utenti che eseguiranno l'integrazione

## Passo 5: Verificare Event Monitoring

1. Vai a **Setup** → **Event Monitoring** → **Event Log Files**
2. Verifica che ci siano eventi recenti
3. Controlla che gli eventi includano:
   - LoginEvent
   - LogoutEvent
   - ApiEvent (se necessario)

## Note Importanti

- Le credenziali OAuth sono sensibili: conservale in modo sicuro
- Il Consumer Secret viene mostrato solo una volta: salvalo immediatamente
- Event Monitoring può avere un delay di 24-48 ore per l'attivazione
- Alcuni eventi potrebbero non essere disponibili immediatamente

## Troubleshooting

- **Event Monitoring non disponibile**: Verifica la licenza Salesforce
- **Nessun evento visibile**: Attendi 24-48 ore dopo l'abilitazione
- **Errori OAuth**: Verifica Callback URL e OAuth Scopes
- **Permessi insufficienti**: Verifica Permission Sets e profili utente

## Fonti

- [Salesforce Event Monitoring Overview](https://developer.salesforce.com/docs/atlas.en-us.event_monitoring.meta/event_monitoring/)
- [Salesforce Event Log Files REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_event_log_file.htm)
- [Salesforce Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm&type=5)
- [Salesforce OAuth Scopes](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_scopes.htm&type=5)

