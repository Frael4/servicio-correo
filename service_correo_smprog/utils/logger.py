import logging
import os
# Obtener direccion del archivo actual
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# obtener la ruta del proyecto y agregar el archivo log
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'service.log')

# Crea la carpeta Logs si no existe
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def get_logger():
    
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    
    return logging.getLogger()

""" import os
import logging

def get_logger():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(BASE_DIR, "logs")
    log_file = os.path.join(log_dir, "service.log")

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  # evita duplicados

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger """