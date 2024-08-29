from config.read_config         import ConfigSpecs
from loop.internal.get_groups   import get_group_paths
from loop.internal.gather_files import randomly_select_wallpapers

def main_loop(specs: ConfigSpecs):
    groups = get_group_paths(specs)

    select = randomly_select_wallpapers(specs, groups)
    print(select)
    
