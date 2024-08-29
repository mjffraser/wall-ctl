from checks.internal.check_manager import check_manager
from checks.internal.check_path    import check_or_setup_paths
from configSpecs                   import ConfigSpecs

def check_error(res: bool, msg):
    if res is False:
        raise Exception(msg)

def run_checks(specs: ConfigSpecs):
    check_error(check_manager(specs),        f"Can't find {specs.get_name()}. Is it installed?")
    check_error(check_or_setup_paths(specs), f"A problem occured locating {specs.get_path()}")
