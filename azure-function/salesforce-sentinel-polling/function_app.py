"""
Azure Function per polling schedulato di eventi Salesforce e invio a Azure Log Analytics (Sentinel).

Questa function esegue polling ogni 5 minuti per estrarre Event Log Files da Salesforce,
trasformarli in formato SIEM e inviarli ad Azure Log Analytics.
"""

import logging
import os
import json
import csv
import io
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
import requests
import hmac
import hashlib
import base64
from pathlib import Path

import jwt
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceNotFoundError

import azure.functions as func

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SalesforceClient:
    """Client per interagire con Salesforce API."""
    
    def __init__(self):
        self.consumer_key = os.environ.get("Salesforce__ConsumerKey")
        self.consumer_secret = os.environ.get("Salesforce__ConsumerSecret")
        self.username = os.environ.get("Salesforce__Username")
        self.password = os.environ.get("Salesforce__Password")
        self.security_token = os.environ.get("Salesforce__SecurityToken")
        self.auth_mode = os.environ.get("Salesforce__AuthMode", "password").lower()
        self.login_url = os.environ.get("Salesforce__LoginUrl", "https://login.salesforce.com")
        self.jwt_private_key = os.environ.get("Salesforce__JwtPrivateKey")
        self.jwt_private_key_path = os.environ.get("Salesforce__JwtPrivateKeyPath")
        self.jwt_audience = os.environ.get("Salesforce__JwtAudience", self.login_url)
        self.jwt_subject = os.environ.get("Salesforce__JwtSubject", self.username)
        
        self.instance_url = None
        self.access_token = None
        self.api_version = "v58.0"
        
        if self.auth_mode not in ("password", "jwt"):
            raise ValueError("Salesforce__AuthMode deve essere 'password' o 'jwt'")
        
        if self.auth_mode == "password":
            if not all([self.consumer_key, self.consumer_secret, self.username, self.password]):
                raise ValueError("Credenziali Salesforce mancanti per il flow Username-Password")
        else:
            if not all([self.consumer_key, self.username]):
                raise ValueError("Salesforce__ConsumerKey e Salesforce__Username sono obbligatori per il flow JWT")
            if not (self.jwt_private_key or self.jwt_private_key_path):
                raise ValueError("Per il flow JWT fornire Salesforce__JwtPrivateKey o Salesforce__JwtPrivateKeyPath")
            if not self.jwt_subject:
                raise ValueError("Salesforce__JwtSubject o Salesforce__Username obbligatorio per il flow JWT")
    
    def _get_token_url(self) -> str:
        return f"{self.login_url.rstrip('/')}/services/oauth2/token"
    
    def authenticate(self) -> str:
        """Autentica con Salesforce usando il flow configurato."""
        if self.auth_mode == "jwt":
            return self._authenticate_with_jwt()
        return self._authenticate_with_password()
    
    def _authenticate_with_password(self) -> str:
        """OAuth 2.0 Username-Password Flow."""
        try:
            token_url = self._get_token_url()
            
            payload = {
                "grant_type": "password",
                "client_id": self.consumer_key,
                "client_secret": self.consumer_secret,
                "username": self.username,
                "password": f"{self.password}{self.security_token}" if self.security_token else self.password
            }
            
            response = requests.post(token_url, data=payload, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.instance_url = token_data["instance_url"]
            
            logger.info("Autenticazione Salesforce riuscita (username/password)")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante autenticazione Salesforce: {str(e)}")
            raise
    
    def _load_private_key(self) -> str:
        if self.jwt_private_key:
            key = self.jwt_private_key.strip()
        elif self.jwt_private_key_path:
            key_path = Path(self.jwt_private_key_path)
            if not key_path.exists():
                raise ValueError(f"File chiave privata non trovato: {self.jwt_private_key_path}")
            key = key_path.read_text(encoding="utf-8").strip()
        else:
            raise ValueError("Chiave privata JWT non configurata")
        
        if "BEGIN" not in key:
            try:
                key = base64.b64decode(key).decode("utf-8")
            except Exception as exc:
                raise ValueError("Chiave privata JWT non valida (base64 decode fallita)") from exc
        
        return key
    
    def _authenticate_with_jwt(self) -> str:
        """OAuth 2.0 JWT Bearer Flow."""
        try:
            private_key = self._load_private_key()
            audience = self.jwt_audience or self.login_url
            token_lifetime = int(os.environ.get("Salesforce__JwtLifetimeSeconds", "300"))
            now = datetime.utcnow()
            exp = now + timedelta(seconds=token_lifetime)
            exp_ts = int(exp.timestamp())
            
            jwt_payload = {
                "iss": self.consumer_key,
                "sub": self.jwt_subject,
                "aud": audience,
                "iat": int(now.timestamp()),
                "exp": exp_ts
            }
            
            assertion = jwt.encode(jwt_payload, private_key, algorithm="RS256")
            
            data = {
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": assertion
            }
            
            response = requests.post(self._get_token_url(), data=data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.instance_url = token_data["instance_url"]
            
            logger.info("Autenticazione Salesforce riuscita (JWT)")
            return self.access_token
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante autenticazione JWT Salesforce: {str(e)}")
            if hasattr(e.response, "text"):
                logger.error(f"Risposta errore Salesforce: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Errore interno durante autenticazione JWT Salesforce: {str(e)}")
            raise
    
    def get_event_log_files(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Recupera la lista di Event Log Files disponibili per il periodo specificato.
        
        Args:
            start_date: Data di inizio (inclusiva)
            end_date: Data di fine (inclusiva)
            
        Returns:
            Lista di Event Log Files
        """
        if not self.access_token:
            self.authenticate()
        
        try:
            # Formatta date per SOQL (YYYY-MM-DD)
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            
            # Query SOQL per recuperare Event Log Files
            # Filtriamo per eventi critici per SIEM
            event_types = [
                "LoginEvent", "LogoutEvent", "ApiEvent", "UriEvent",
                "ReportEvent", "DashboardEvent", "DataExportEvent"
            ]
            event_types_str = "', '".join(event_types)
            
            # Costruisci query SOQL
            query = (
                f"SELECT Id, EventType, LogDate, LogFileLength, LogFileContentType, CreatedDate "
                f"FROM EventLogFile "
                f"WHERE LogDate >= {start_date_str} "
                f"AND LogDate <= {end_date_str} "
                f"AND EventType IN ('{event_types_str}') "
                f"ORDER BY LogDate DESC, CreatedDate DESC"
            )
            
            # Endpoint per Event Log Files (usa sobjects, non query)
            url = f"{self.instance_url}/services/data/{self.api_version}/sobjects/EventLogFile/"
            params = {"q": query}
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.get(url, params=params, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            files = result.get("records", [])
            
            # Gestisci paginazione se presente
            while result.get("nextRecordsUrl"):
                next_url = f"{self.instance_url}{result['nextRecordsUrl']}"
                next_response = requests.get(next_url, headers=headers, timeout=60)
                next_response.raise_for_status()
                result = next_response.json()
                files.extend(result.get("records", []))
            
            logger.info(f"Trovati {len(files)} Event Log Files per il periodo {start_date_str} - {end_date_str}")
            return files
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante recupero Event Log Files: {str(e)}")
            raise
    
    def download_log_file(self, log_file_id: str) -> str:
        """
        Scarica il contenuto di un Event Log File.
        
        Args:
            log_file_id: ID dell'Event Log File
            
        Returns:
            Contenuto del file come stringa CSV
        """
        if not self.access_token:
            self.authenticate()
        
        try:
            url = f"{self.instance_url}/services/data/{self.api_version}/sobjects/EventLogFile/{log_file_id}/LogFile"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.get(url, headers=headers, timeout=120)
            response.raise_for_status()
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante download Event Log File {log_file_id}: {str(e)}")
            raise


class LogAnalyticsClient:
    """Client per inviare dati ad Azure Log Analytics."""
    
    def __init__(self):
        self.workspace_id = os.environ.get("LogAnalytics__WorkspaceId")
        self.workspace_key = os.environ.get("LogAnalytics__WorkspaceKey")
        self.log_type = os.environ.get("LogAnalytics__LogType", "Salesforce_CL")
        self.environment = os.environ.get("Environment__Name")
        
        if not all([self.workspace_id, self.workspace_key]):
            raise ValueError("Credenziali Log Analytics mancanti nelle variabili d'ambiente")
        
        self.api_url = f"https://{self.workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    
    def build_signature(self, date: str, content_length: int, method: str, content_type: str, resource: str) -> str:
        """
        Costruisce la signature HMAC-SHA256 per l'autenticazione con Log Analytics.
        
        Args:
            date: Data in formato RFC 1123
            content_length: Lunghezza del contenuto
            method: Metodo HTTP (POST)
            content_type: Tipo di contenuto (application/json)
            resource: Risorsa API (/api/logs)
            
        Returns:
            Signature codificata in base64
        """
        x_headers = f"x-ms-date:{date}"
        string_to_sign = f"{method}\n{str(content_length)}\n{content_type}\n{x_headers}\n{resource}"
        
        decoded_key = base64.b64decode(self.workspace_key)
        encoded_hash = hmac.new(decoded_key, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        encoded_signature = base64.b64encode(encoded_hash).decode('utf-8')
        
        return f"SharedKey {self.workspace_id}:{encoded_signature}"
    
    def send_logs(self, logs: List[Dict[str, Any]]) -> bool:
        """
        Invia log ad Azure Log Analytics.
        
        Args:
            logs: Lista di log da inviare
            
        Returns:
            True se l'invio è riuscito, False altrimenti
        """
        if not logs:
            logger.warning("Nessun log da inviare")
            return True
        
        try:
            if self.environment:
                for log in logs:
                    log.setdefault("Environment", self.environment)
            
            # Serializza i log in JSON
            json_data = json.dumps(logs)
            content_length = len(json_data.encode('utf-8'))
            content_type = "application/json"
            
            # Data in formato RFC 1123
            date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
            
            # Costruisci signature
            signature = self.build_signature(date, content_length, "POST", content_type, "/api/logs")
            
            # Headers
            headers = {
                "Content-Type": content_type,
                "Authorization": signature,
                "Log-Type": self.log_type,
                "x-ms-date": date,
                "time-generated-field": "TimeGenerated"
            }
            
            # Invia richiesta
            response = requests.post(self.api_url, data=json_data, headers=headers, timeout=60)
            response.raise_for_status()
            
            logger.info(f"Inviati {len(logs)} log a Log Analytics")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Errore durante invio a Log Analytics: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Risposta errore: {e.response.text}")
            return False


class DataTransformer:
    """Trasforma eventi Salesforce in formato SIEM per Azure Sentinel."""
    
    @staticmethod
    def parse_csv_log(csv_content: str, event_type: str) -> List[Dict[str, Any]]:
        """
        Analizza un file CSV di Event Log e lo converte in formato SIEM.
        
        Args:
            csv_content: Contenuto CSV del log
            event_type: Tipo di evento (LoginEvent, ApiEvent, ecc.)
            
        Returns:
            Lista di eventi trasformati
        """
        events = []
        
        try:
            # Leggi CSV
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            for row in csv_reader:
                # Trasforma ogni riga in formato SIEM
                transformed_event = DataTransformer._transform_event(row, event_type)
                if transformed_event:
                    events.append(transformed_event)
            
            logger.info(f"Trasformati {len(events)} eventi di tipo {event_type}")
            return events
            
        except Exception as e:
            logger.error(f"Errore durante parsing CSV per {event_type}: {str(e)}")
            return []
    
    @staticmethod
    def _transform_event(row: Dict[str, str], event_type: str) -> Optional[Dict[str, Any]]:
        """
        Trasforma un singolo evento in formato SIEM.
        
        Args:
            row: Riga CSV dell'evento
            event_type: Tipo di evento
            
        Returns:
            Evento trasformato o None se non valido
        """
        try:
            # Base event structure per SIEM
            event = {
                "TimeGenerated": DataTransformer._parse_timestamp(row.get("TIMESTAMP", row.get("EVENT_DATE", ""))),
                "EventType": event_type,
                "SourceSystem": "Salesforce",
            }
            
            # Aggiungi campi specifici per tipo di evento
            if event_type == "LoginEvent":
                event.update({
                    "UserId": row.get("USER_ID", ""),
                    "Username": row.get("USERNAME", ""),
                    "SourceIp": row.get("SOURCE_IP", ""),
                    "LoginType": row.get("LOGIN_TYPE", ""),
                    "Status": row.get("STATUS", ""),
                    "Browser": row.get("BROWSER", ""),
                    "Platform": row.get("PLATFORM", ""),
                    "LoginGeoId": row.get("LOGIN_GEO_ID", ""),
                    "SessionKey": row.get("SESSION_KEY", ""),
                })
            elif event_type == "LogoutEvent":
                event.update({
                    "UserId": row.get("USER_ID", ""),
                    "Username": row.get("USERNAME", ""),
                    "SourceIp": row.get("SOURCE_IP", ""),
                    "SessionKey": row.get("SESSION_KEY", ""),
                })
            elif event_type == "ApiEvent":
                event.update({
                    "UserId": row.get("USER_ID", ""),
                    "Username": row.get("USERNAME", ""),
                    "ApiType": row.get("API_TYPE", ""),
                    "ApiVersion": row.get("API_VERSION", ""),
                    "Method": row.get("METHOD", ""),
                    "Url": row.get("URL", ""),
                    "Status": row.get("STATUS", ""),
                    "ResponseTime": DataTransformer._parse_int(row.get("RESPONSE_TIME", "")),
                    "SourceIp": row.get("SOURCE_IP", ""),
                    "Client": row.get("CLIENT", ""),
                })
            elif event_type == "UriEvent":
                event.update({
                    "UserId": row.get("USER_ID", ""),
                    "Username": row.get("USERNAME", ""),
                    "Uri": row.get("URI", ""),
                    "PageUrl": row.get("PAGE_URL", ""),
                    "Duration": DataTransformer._parse_int(row.get("DURATION", "")),
                    "SourceIp": row.get("SOURCE_IP", ""),
                })
            else:
                # Per altri tipi di evento, aggiungi tutti i campi disponibili
                for key, value in row.items():
                    if key and value:
                        # Normalizza nomi campi (rimuovi underscore, capitalizza)
                        normalized_key = key.replace("_", "").title()
                        event[normalized_key] = value
            
            return event
            
        except Exception as e:
            logger.warning(f"Errore durante trasformazione evento: {str(e)}")
            return None
    
    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> str:
        """Converte timestamp in formato ISO 8601 UTC."""
        if not timestamp_str:
            return datetime.now(timezone.utc).isoformat()
        
        try:
            # Prova vari formati timestamp Salesforce
            formats = [
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(timestamp_str, fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # Se nessun formato funziona, usa timestamp corrente
            return datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            logger.warning(f"Errore parsing timestamp '{timestamp_str}': {str(e)}")
            return datetime.now(timezone.utc).isoformat()
    
    @staticmethod
    def _parse_int(value: str) -> Optional[int]:
        """Converte stringa in intero, ritorna None se non valido."""
        try:
            return int(value) if value else None
        except (ValueError, TypeError):
            return None


class CheckpointStore:
    """Gestisce la persistenza dell'ultima data processata tramite Azure Table Storage."""
    
    def __init__(self):
        self.connection_string = os.environ.get("Checkpoint__StorageConnectionString")
        self.table_name = os.environ.get("Checkpoint__TableName", "SalesforceCheckpoints")
        self.partition_key = os.environ.get("Checkpoint__PartitionKey", "Salesforce")
        self.row_key = os.environ.get("Checkpoint__RowKey", "EventLogPolling")
        self.table_client = self._create_table_client()
    
    def _create_table_client(self):
        if not self.connection_string:
            return None
        
        try:
            service_client = TableServiceClient.from_connection_string(self.connection_string)
            service_client.create_table_if_not_exists(table_name=self.table_name)
            return service_client.get_table_client(table_name=self.table_name)
        except Exception as exc:
            logger.error(f"Impossibile inizializzare CheckpointStore: {str(exc)}")
            return None
    
    def get_last_processed_date(self) -> Optional[datetime]:
        if not self.table_client:
            return None
        
        try:
            entity = self.table_client.get_entity(self.partition_key, self.row_key)
            last_date = entity.get("LastProcessedDate")
            
            if isinstance(last_date, datetime):
                if last_date.tzinfo is None:
                    last_date = last_date.replace(tzinfo=timezone.utc)
                return last_date
            
            if isinstance(last_date, str) and last_date:
                return datetime.fromisoformat(last_date)
        
        except ResourceNotFoundError:
            logger.info("Checkpoint non trovato in Table Storage, verrà creato al primo salvataggio")
        except Exception as exc:
            logger.error(f"Errore durante lettura checkpoint: {str(exc)}")
        
        return None
    
    def save_last_processed_date(self, date: datetime) -> bool:
        if not self.table_client:
            return False
        
        entity = {
            "PartitionKey": self.partition_key,
            "RowKey": self.row_key,
            "LastProcessedDate": date.isoformat(),
            "UpdatedAt": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            self.table_client.upsert_entity(entity)
            return True
        except Exception as exc:
            logger.error(f"Errore durante salvataggio checkpoint: {str(exc)}")
            return False


def _get_int_env(var_name: str, default: int) -> int:
    """Recupera un intero dalle variabili d'ambiente con fallback sicuro."""
    try:
        return int(os.environ.get(var_name, default))
    except (TypeError, ValueError):
        return default


def get_last_processed_date() -> datetime:
    """
    Recupera l'ultima data processata (checkpoint).
    
    Returns:
        Data dell'ultimo evento processato
    """
    fallback_hours = _get_int_env("Checkpoint__FallbackHours", 24)
    fallback_value = datetime.now(timezone.utc) - timedelta(hours=fallback_hours)
    
    store = CheckpointStore()
    last_date = store.get_last_processed_date()
    
    if last_date:
        return last_date
    
    logger.info("Checkpoint non disponibile: utilizzo fallback di %s ore", fallback_hours)
    return fallback_value


def save_last_processed_date(date: datetime):
    """
    Salva l'ultima data processata (checkpoint).
    
    Args:
        date: Data da salvare
    """
    store = CheckpointStore()
    
    if store.save_last_processed_date(date):
        logger.info("Checkpoint persistito: %s", date.isoformat())
    else:
        logger.warning("Checkpoint non persistito (storage non configurato): %s", date.isoformat())


app = func.FunctionApp()


@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=False)
def salesforce_sentinel_polling(myTimer: func.TimerRequest) -> None:
    """
    Azure Function Timer Trigger che esegue polling ogni 5 minuti.
    
    La function:
    1. Si autentica con Salesforce
    2. Recupera Event Log Files degli ultimi 5 minuti
    3. Scarica e analizza i file
    4. Trasforma gli eventi in formato SIEM
    5. Invia gli eventi ad Azure Log Analytics
    """
    logger.info("Avvio polling Salesforce -> Sentinel")
    
    try:
        # Inizializza client
        sf_client = SalesforceClient()
        la_client = LogAnalyticsClient()
        transformer = DataTransformer()
        
        # Autentica con Salesforce
        sf_client.authenticate()
        
        # Calcola range date per polling utilizzando checkpoint persistente
        end_date = datetime.now(timezone.utc)
        start_date = get_last_processed_date()
        overlap_minutes = max(0, _get_int_env("Checkpoint__OverlapMinutes", 5))
        
        if overlap_minutes:
            start_date -= timedelta(minutes=overlap_minutes)
        
        if start_date >= end_date:
            start_date = end_date - timedelta(minutes=1)
        
        logger.info(f"Polling eventi da {start_date.isoformat()} a {end_date.isoformat()}")
        
        # Recupera lista Event Log Files
        log_files = sf_client.get_event_log_files(start_date, end_date)
        
        if not log_files:
            logger.info("Nessun Event Log File trovato per il periodo specificato")
            return
        
        # Processa ogni file
        all_events = []
        processed_count = 0
        
        for log_file in log_files:
            try:
                log_file_id = log_file["Id"]
                event_type = log_file["EventType"]
                log_date = log_file.get("LogDate", "")
                
                logger.info(f"Processando Event Log File: {log_file_id} (Tipo: {event_type}, Data: {log_date})")
                
                # Scarica contenuto file
                csv_content = sf_client.download_log_file(log_file_id)
                
                if not csv_content:
                    logger.warning(f"File {log_file_id} vuoto, skip")
                    continue
                
                # Trasforma eventi
                events = transformer.parse_csv_log(csv_content, event_type)
                
                if events:
                    all_events.extend(events)
                    processed_count += 1
                
            except Exception as e:
                logger.error(f"Errore durante processamento file {log_file.get('Id', 'unknown')}: {str(e)}")
                continue
        
        # Invia eventi a Log Analytics in batch
        if all_events:
            # Log Analytics accetta max 30MB per richiesta, quindi inviamo in batch da 1000 eventi
            batch_size = 1000
            total_sent = 0
            
            for i in range(0, len(all_events), batch_size):
                batch = all_events[i:i + batch_size]
                if la_client.send_logs(batch):
                    total_sent += len(batch)
                else:
                    logger.error(f"Errore durante invio batch {i // batch_size + 1}")
            
            logger.info(f"Polling completato: {total_sent} eventi inviati a Log Analytics da {processed_count} file")
        else:
            logger.info("Nessun evento da inviare")
        
        # Salva checkpoint
        save_last_processed_date(end_date)
        
    except Exception as e:
        logger.error(f"Errore critico durante polling: {str(e)}", exc_info=True)
        raise

