from typing import Iterable

import win32serviceutil
import win32service
import win32event
import servicemanager


class ServiceEmail(win32serviceutil.ServiceFramework):
    
    _svc_name_ = "ServicioDeCorreoSMProg"
    _svc_display_name_ = "Servicio de notificación por correo"
    
    def __init__(self, args: Iterable[str]) -> None:
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        
    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Inicio de servicio")
        self.main()
    
    def main(self):
        while True:
            print("Servicio corriendo....")