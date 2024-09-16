import subprocess
from time import sleep

def start_hyprpaper():
    subprocess.Popen(["hyprpaper"], start_new_session=True)
    sleep(1) #short delay to make sure hyprpaper initializes

def unload_wallpapers_hyprpaper():
    subprocess.run(["hyprctl", "hyprpaper", "unload", "all"])

def preload_wallpaper_hyprpaper(path: str):
    subprocess.run(["hyprctl", "hyprpaper", "preload", path])

def load_wallpaper_hyprpaper(path: str, display_name: str):
    subprocess.run(["hyprctl", "hyprpaper", "wallpaper", f"{display_name},{path}"])
