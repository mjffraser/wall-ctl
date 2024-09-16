from config.read_config            import ConfigSpecs
from loop.internal.get_groups      import get_group_paths
from loop.internal.gather_files    import randomly_select_wallpapers
from loop.internal.load_and_unload import load_wallpapers, preload_wallpapers
from time                          import sleep

def main_loop(specs: ConfigSpecs):
    current_groups = get_group_paths(specs)
    time = 0
    refresh_time = specs.get_refresh()
    preload_time = refresh_time - specs.get_preload_buffer()
    
    #this doesn't really make sense to do and can cause some weird timing 
    if preload_time > specs.get_check_freq():
        preload_time = refresh_time - specs.get_check_freq() 

    selected = None

    while True:
        groups = get_group_paths(specs)
        if current_groups != groups: #if wallpaper groups has changed, swap wallpapers as soon as it's noticed
            current_groups = groups
            selected = randomly_select_wallpapers(specs, current_groups)
            preload_wallpapers(specs, selected)
            sleep(specs.get_preload_buffer())
            load_wallpapers(specs, selected)
            time = 0

        elif time == preload_time:
            selected = randomly_select_wallpapers(specs, current_groups) 
            preload_wallpapers(specs, selected)

        elif time == refresh_time:
            assert selected is not None
            load_wallpapers(specs, selected)
            time = 0     

        del groups

        if time < preload_time and time + specs.get_check_freq() > preload_time: #if it's matches exactly the else clause handles it
            sleep_time = preload_time - time
        elif time == preload_time: 
            sleep_time = refresh_time - time 
        else:
            sleep_time = specs.get_check_freq()

        time += sleep_time 
        sleep(sleep_time)



 
    
