from subprocess import run, DEVNULL
from configSpecs import ConfigSpecs

def check_manager(specs: ConfigSpecs) -> bool:
    result = run(["which", f"{specs.get_name()}"], stdout=DEVNULL, stderr=DEVNULL)
    if result.returncode == 0:
        return True 
    return False
