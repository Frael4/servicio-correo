from service_correo_smprog.config.config_loader import load_config

def test_get_data_config():
    
    config = load_config()
    
    assert config["SMPROG_GRUASATLAS"]["SESION_DAC"] == 'N'