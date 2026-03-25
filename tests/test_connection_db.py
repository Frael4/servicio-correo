from service_correo_smprog.database.connection import DataBaseManager
from service_correo_smprog.config.config_loader import load_config
from service_correo_smprog.utils.logger import get_logger

logger = get_logger()
config = load_config()
conn = DataBaseManager(config)

def test_connection_db():
    
    smprog_atlas = conn.get_connection('SMPROG_GRUASATLAS')
    
    cursor = smprog_atlas.execute('SELECT 1')
    
    assert cursor.fetchone()[0] == 1 # type: ignore


def test_multi_connection():
    
    atlas = conn.get_connection('SMPROG_GRUASATLAS')
    conauto = conn.get_connection('SMPROG_CONAUTO')
    
    cursor_atlas = atlas.execute('EXEC PSG_CARGA_MENU 1, 2')
    cursor_conauto = conauto.execute('EXEC PSG_CONS_PARAMETRO 1')
    
    logger.info(cursor_atlas.fetchall())
    # logger.info(cursor_atlas.fetchone()[0]) # type: ignore
    logger.info(cursor_conauto.fetchall())
    
    assert 1 == 1
    
def test_existed_connections():
    
    atlas = conn.get_connection('SMPROG_GRUASATLAS')
    conauto = conn.get_connection('SMPROG_CONAUTO')
    
    # conexiones guardadas en el Gestor
    logger.info(conn.connections)
    
    assert len(conn.connections) == 2
    # Recuperamos la conexion existen en el registro
    conauto = conn.connections['SMPROG_CONAUTO']
    # usamos la conexión existente
    c = conauto.execute('SELECT 1')
    
    logger.info(c.fetchone()) # Obtenemos un registro