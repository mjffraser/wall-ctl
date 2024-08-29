from config.internal.check import import_config 
from configSpecs import ConfigSpecs

def get_config() -> ConfigSpecs:
    try: 
        return import_config() 
    except Exception as e:
        raise ImportError(e)


    


