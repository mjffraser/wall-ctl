from configSpecs import ConfigSpecs
from os          import mkdir
from typing      import List, Tuple

def _check_path(path: str) -> bool:
    try:
        mkdir(path)
    except FileExistsError:
        return True
    except Exception:
        return False
    return True


def _check_all_paths(paths: List[str]):
    for path in paths:
        if _check_path(path) is False:
            raise NameError(f"Can't create/find path: {path}")


def _check_nested_paths(names_list: List[str], base_paths: List[str]) -> Tuple[ List[str], bool ]:
    updated_list = []
    okay = True
    for path in base_paths:
        for name in names_list:
            updated_list.append(f"{path}/{name}")

    try:
        _check_all_paths(updated_list)
    except NameError:
        okay = False
    return updated_list, okay


def check_or_setup_paths(specs: ConfigSpecs) -> bool:
    ret = True
    base_paths = [f"{specs.get_path()}"]
   
    #groups
    group_names = specs.get_group_names()
    if group_names is not None:
        base_paths, result = _check_nested_paths(group_names, base_paths)
        ret &= result

    #seasons
    seasons = specs.get_seasons()
    if seasons is not None:
        season_names, *_ = seasons
        base_paths, result = _check_nested_paths(season_names, base_paths)
        ret &= result 

    #hourly
    hourly = specs.get_hourly()
    if hourly is not None:
        hourly_names, *_ = hourly
        base_paths, result = _check_nested_paths(hourly_names, base_paths)
        ret &= result

    return ret

    
