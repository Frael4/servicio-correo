import configparser
from pathlib import Path

def load_config(path="config.ini"):
    
    config = configparser.ConfigParser()
    # Construir ruta relativa al archivo de configuración
    base_path = Path(__file__).resolve().parent
    config_path = base_path / "config.ini"
    
    config.read(config_path)
    
    return config