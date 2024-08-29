from typing  import List, Tuple
from os      import listdir
from secrets import choice
from configSpecs import ConfigSpecs

allowed_paths = ["png", "jpg", "jpeg"]

def _scan_files(group: List[str]) -> List[str]:
    files = []
    for path in group:
        for file in listdir(path):
            if file.endswith(tuple(allowed_paths)):
                files.append(path + "/" + file)
    return files
        
    
def _randomly_select_file(files: List[str]) -> str:
    if len(files) > 0:
        return choice(files)
    return ""


def _pick_file(path_list: List[str]) -> str:
    files = _scan_files(path_list)
    return _randomly_select_file(files)

def randomly_select_wallpapers(specs: ConfigSpecs, paths: List[str]) -> List[Tuple[str, str]]:
    groups = specs.get_group_names()
    base_path = specs.get_path()
    if groups is not None:
        groups_dict = dict()
        for g in groups:
            groups_dict[g] = [base_path + "/" + g]
            for p in paths:
                if p.startswith(base_path + "/" + g):
                    groups_dict[g].append(p)

        tuple_list = []
        for group_name, path_list in groups_dict.items():
            tuple_list.append( (group_name, _pick_file(path_list)) )
        return tuple_list

    else:
        return [ ( "", _pick_file(paths) ) ] 

        



