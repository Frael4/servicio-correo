import pyodbc
from service_correo_smprog.utils.logger import get_logger
import threading # Uso de hilos

log = get_logger()

class DataBaseManager:
    
    def __init__(self, config) -> None:
        self.config = config
        self.connections = {}
        self.lock = threading.Lock() # Candado para evitar colisiones
        
    def get_connection(self, name_connection):
        with self.lock: # Se agrega bloqueo de uso para hilos
            
            if name_connection in self.connections: # Si conexion ya existe, devolvemos la conexión
                log.info("Conexión encontrada en diccionario, retornando conexión")
                con = self.connections[name_connection]
                
                try:
                    con.cursor().execute('SELEC 1')
                    return con
                except (pyodbc.Error, Exception):
                    log.warning(f"Conexión {name_connection} estaba caida")
                    self.connections.pop(name_connection, None) # quitamos la conexión del diccionario
            
            db = self.config[name_connection]
            
            log.info("Iniciando conexión la base de datos... ")
            log.info("Datos de conexión:")
            log.info(f"{db['SERVIDOR/HOST']} DB:{db['BD/SERVICIO']} USER:{db['USUARIO']} PWD:{db['CONTRASENA']}")
            
            conn = ''
            try:
                # Importante poner los punto y coma en los parametros
                conn = pyodbc.connect(
                    "DRIVER={ODBC Driver 17 for SQL Server};"
                    f"SERVER={db['SERVIDOR/HOST']};"
                    f"DATABASE={db['BD/SERVICIO']};"
                    f"UID={db['USUARIO']};"
                    f"PWD={db['CONTRASENA']};"
                )
                
                log.info("Conexión establecida, retornando conexión")
                self.connections[name_connection] = conn
            
            except pyodbc.Error as e:
                log.debug(f"{e}")
                raise e
            
        return conn