from configSpecs import ConfigSpecs
from typing import List, Tuple
import subprocess

#supported manager imports
from loop.internal.managers.hyprpaper import start_hyprpaper, unload_wallpapers_hyprpaper, preload_wallpaper_hyprpaper, load_wallpaper_hyprpaper

def _start_manager(specs: ConfigSpecs):
    if specs.get_name() == "hyprpaper":
        start_hyprpaper()

def _check_manager(specs: ConfigSpecs):
    try:
        subprocess.check_output( ["pgrep", specs.get_name()] )
    except subprocess.CalledProcessError:
        _start_manager(specs)

def _unload_wallpapers(specs: ConfigSpecs):
    if specs.get_name() == "hyprpaper":
        unload_wallpapers_hyprpaper() 

def _preload_wallpaper(specs: ConfigSpecs, path: str):
    if specs.get_name() == "hyprpaper":
        preload_wallpaper_hyprpaper(path) 

def _load_wallpaper(specs: ConfigSpecs, path: str, display_name: str):
    if specs.get_name() == "hyprpaper":
        load_wallpaper_hyprpaper(path, display_name) 
    

def preload_wallpapers(specs: ConfigSpecs, selections: List [ Tuple[str, str] ]):
    if specs.initialized is False:
        _check_manager(specs)
        specs.initialized = True

    _unload_wallpapers(specs)

    for entry in selections:
        wallpaper = entry[1]
        if wallpaper != "":
            _preload_wallpaper(specs, entry[1])
    

def load_wallpapers(specs: ConfigSpecs, selections: List[ Tuple[str, str] ]):
    if specs.initialized is False:
        _check_manager(specs) 
        specs.initialized = True 

    #actual load
    groups = specs.get_group_names()
    display_list = specs.get_display_names()
    for entry in selections:
        if groups is not None:
            index = groups.index(entry[0])
        else:
            index = 0
        
        displays = display_list[index]
        for d in displays:
            if entry[1] != "":
                _load_wallpaper(specs, entry[1], d)


