from typing import Iterable
import sys
import os

import sys
import os

# Log de emergencia — captura cualquier crash antes del logger normal
_elog = open(r"E:\Python\ServiceCorreoSMProg\crash.txt", "w")
sys.stderr = _elog
sys.stdout = _elog
print("service.py cargado OK")
_elog.flush()

print(".....")
_elog.flush()

print("imports base OK"); _elog.flush()

import win32serviceutil
print("win32serviceutil OK"); _elog.flush()

import win32service
print("win32service OK"); _elog.flush()

import win32event
print("win32event OK"); _elog.flush()

import servicemanager
print("servicemanager OK"); _elog.flush()

import threading
print("threading OK"); _elog.flush()

from service_correo_smprog.config.config_loader import load_config
print("load_config OK"); _elog.flush()

from service_correo_smprog.database.connection import DataBaseManager
print("DataBaseManager OK"); _elog.flush()

from service_correo_smprog.utils.logger import get_logger
print("get_logger OK"); _elog.flush()

log = get_logger()
print("logger instanciado OK"); _elog.flush()
# Fuerza el path correcto cuando Windows ejecuta el servicio

BASE_DIR = r"E:\Python\ServiceCorreoSMProg"
VENV_SITE = r"E:\Python\ServiceCorreoSMProg\.venv\Lib\site-packages"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if VENV_SITE not in sys.path:
    sys.path.insert(1, VENV_SITE)
os.chdir(BASE_DIR)


class ServiceEmail(win32serviceutil.ServiceFramework):
    
    _svc_name_ = "ServicioDeCorreoSMProg"
    _svc_display_name_ = "Servicio de notificación por correo Frael"
    _svc_description_ = "Gestiona el envío de correos desde múltiples BD"
    
    def __init__(self, args: Iterable[str]) -> None:
        self.log = get_logger()
        self.log.info("__init__ iniciado")
        print("__init__ iniciado"); _elog.flush()
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self._stop_flag = threading.Event() # Para los workers
        self._threads: list[threading.Thread] = []
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self._stop_flag.set()
        win32event.SetEvent(self.stop_event)
        
    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Inicio de servicio")
        self.log.info("Iniciando servicio")
        try:
            
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.main()
        except Exception as e:
            print(f"Error en SvcDoRun: {e}"); _elog.flush()
            self.log.error(f"Error fatal: {e}")
            self.SvcStop()
    
    def main(self):
        """  """
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.connections = DataBaseManager(load_config())
        self.log.info("Servicio en estado RUNNING")
        
        workers = [
            threading.Thread(target=self._worker_revisar_tareas, daemon=True, name="revisar"),
            threading.Thread(target=self._worker_enviar_correos, daemon=True, name="correos"),
            threading.Thread(target=self._worker_actualizar_tareas, daemon=True, name="actualizar")
        ]
        
        for t in workers:
            t.start()
            self._threads.append(t)
            self.log.info(f"Hilo [{t.name}] iniciado.")
            
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            
    
    def _worker_revisar_tareas(self):
        """ Revisar tareas pendientes en BD en un loop """
        self.log.info("Revisando tareas pendientes ...")
        # connections -> Tengo multiples conexiones a BDs
        while not self._stop_flag.is_set():
            
            try:
                # with conn as c:
                    # logica para buscar tareas
                    pass
            except Exception as e:
                self.log.error(f"[tareas] {e}")
            
            self._stop_flag.wait(timeout=30) # pausa 30 s
            
    
    def _worker_enviar_correos(self):
        """ Enviar correos """
        self.log.info("Enviando correos ....")
        
    
    def _worker_actualizar_tareas(self):
        """ Actualizar tareas """
        self.log.info("Actualizando tareas ...")
    
    