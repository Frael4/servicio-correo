import sys
import os

# Obtener la ruta de la raíz (E:\Python\ServiceCorreoSMProg)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_path not in sys.path:
    sys.path.insert(0, base_path)
    
# Ruta absoluta al log de errores
LOG_ERR = r'E:\Python\ServiceCorreoSMProg\error_critico.txt'

try:
    f = open(LOG_ERR, 'a')
    sys.stdout = f
    sys.stderr = f
    print("\n--- Intento de arranque ---")
except:
    pass

import win32serviceutil
from service_correo_smprog.service.service import ServiceEmail

import sys

# Esto crea un archivo con el error real si el servicio explota
sys.stderr = open(r'E:\Python\ServiceCorreoSMProg\error_critico.txt', 'w')
sys.stdout = sys.stderr


if __name__ == "__main__":
    
    """ if len(sys.argv) > 1 and sys.argv[1] == 'debug': """
    win32serviceutil.HandleCommandLine(ServiceEmail)
    """ else:
        # MODO DESARROLLO PURO
        print("Iniciando en modo desarrollo directo...")
        serv = ServiceEmail(['ServicioDeCorreoSMProg'])
        serv.SvcDoRun() """