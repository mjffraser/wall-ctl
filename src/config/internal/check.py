from os      import getenv, makedirs
from os.path import isdir

from configSpecs import ConfigSpecs
             
import yaml

def create_directory(path: str):
    makedirs(path)

def validate_directory(path: str) -> bool:
    if not isdir(path):
        create_directory(path)

    if not isdir(path):
        return False
    return True

def validate_config(home_dir: str) -> bool:
    path = home_dir + "/.config/wall-ctl/"
    return validate_directory(path)

def validate_cache(home_dir: str) -> bool:
    path = home_dir + "/.cache/wall-ctl/"
    return validate_directory(path)

def validate_wallpapers(path: str) -> bool:
    return validate_directory(path)

def read_mandatory_field(header: str, name: str, yaml_data):
    try:
        return yaml_data[header][name]
    except:
        raise KeyError(f"Couldn't find mandatory key/value pair {header}:{name} in config file.")

def read_config(home_dir: str) -> ConfigSpecs:
    path = home_dir + "/.config/wall-ctl/config.yaml"
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    
    #config header
    if "config" not in data:
        raise KeyError("Cannot find \"config\" header in config file.")
    manager_name       = read_mandatory_field("config", "manager_name", data) 
    path               = read_mandatory_field("config", "path", data)
    generic_folder     = data["config"].get("generic_folder",  None)
    freq               = data["config"].get("freq",            None)
    preload_buffer     = data["config"].get("preload_buffer",  None)
    refresh_seconds    = data["config"].get("refresh_seconds", None)
    refresh_minutes    = data["config"].get("refresh_minutes", None)
    refresh_hours      = data["config"].get("refresh_hours",   None)

    #displays header
    if "displays" not in data:
        raise KeyError("Cannot find \"displays\" header in config file.")
    display_names      = read_mandatory_field("displays", "display_names", data) 
    group_names        = data["displays"].get("group_names", None)

    #seasons header
    season_names       = None
    season_start_dates = None
    season_end_dates   = None
    if "seasons" in data:
        season_names       = data["seasons"].get("season_names",       None)
        season_start_dates = data["seasons"].get("season_start_dates", None)
        season_end_dates   = data["seasons"].get("season_end_dates",   None)

    #hourly header
    hourly_names       = None
    hourly_start_times = None
    hourly_end_times   = None
    if "hourly" in data:
        hourly_names       = data["hourly"].get("hourly_names",       None)
        hourly_start_times = data["hourly"].get("hourly_start_times", None)
        hourly_end_times   = data["hourly"].get("hourly_end_times",   None)

    return ConfigSpecs(
        manager_name,
        path,
        generic_folder,
        freq,
        preload_buffer,
        refresh_seconds,
        refresh_minutes,
        refresh_hours,
        display_names,
        group_names,
        season_names,
        season_start_dates,
        season_end_dates,
        hourly_names,
        hourly_start_times,
        hourly_end_times
    )
     
def import_config() -> ConfigSpecs: 
    home_dir = getenv("HOME")
    if home_dir is None:
        raise PermissionError("Can't find $HOME dir")
    if not (validate_config(home_dir) and validate_cache(home_dir)):
        raise PermissionError("Can't find .config and .cache directories.") #problem accessing config and cache directories, shouldn't happen if run as user process
    specs = read_config(home_dir)
        
    if not validate_wallpapers(specs.get_path()):
        raise ValueError(f"Can't find main wallpaper dir at: {specs.get_path()}")

    return specs


   





