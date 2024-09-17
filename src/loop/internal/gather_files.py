from typing      import List, Tuple, Dict
from os          import listdir
from secrets     import choice
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


def _pick_file(path_list: List[str], scan_for = None, do_not_choose = None) -> str:
    files = _scan_files(path_list)
    if scan_for is not None and do_not_choose is not None:
        filename = scan_for.rsplit('/', 1)[-1]
        if do_not_choose:
            files = [file for file in files if file.rsplit('/', 1)[-1] != filename]

        for file in files:
            if file.rsplit('/', 1)[-1] == filename:
                return file
     
    return _randomly_select_file(files)


def _make_selections(specs: ConfigSpecs, group_path_dict: Dict) -> List[Tuple[str, str]]:
    id = specs.get_selection_type()
    tuple_list = []
    if id == 0:
        #get group with the largest number of wallpapers to choose from
        index = max(group_path_dict, key=lambda i: len(_scan_files(group_path_dict[i])))
        print(index)
        file = _pick_file(group_path_dict[index])
        tuple_list.append( (index, file) )
        for group_name, path_list in group_path_dict.items():
            if group_name == index:
                continue
            tuple_list.append( (group_name, _pick_file(path_list, file, False)) ) 
        return tuple_list

    elif id == 1:
        #get group with smallest number of wallpapers to choose from
        index = min( 
            (k for k in group_path_dict if len(_scan_files(group_path_dict[k])) > 0),
            key=lambda i: len(_scan_files(group_path_dict[i]))
        )

        file = _pick_file(group_path_dict[index])
        tuple_list.append( (index, file) )
        for group_name, path_list in group_path_dict.items():
            if group_name == index:
                continue
            tuple_list.append( (group_name, _pick_file(path_list, file, True)) )
        return tuple_list
    
    #if neither 0 nor 1 we just make all selections independently
    for group_name, path_list in group_path_dict.items():
        tuple_list.append( (group_name, _pick_file(path_list)) )
    return tuple_list

def randomly_select_wallpapers(specs: ConfigSpecs, paths: List[str]) -> List[Tuple[str, str]]:
    groups = specs.get_group_names()
    base_path = specs.get_path()
    groups_dict = dict()
    if groups is not None:
        for g in groups:
            groups_dict[g] = [base_path + "/" + g]
            for p in paths:
                if p.startswith(base_path + "/" + g):
                    groups_dict[g].append(p)
 
        return _make_selections(specs, groups_dict)

    else:
        groups_dict[""] = paths
        return _make_selections(specs, groups_dict)

        



