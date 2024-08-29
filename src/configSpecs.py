from typing import List, Tuple, Optional

class ConfigSpecs:
    _initialized        = False

    ################################################################################
    #config section
    #required
    _manager_name       = None
    _path               = None

    #optional
    _generic_folder     = None
    _refresh_seconds    = None
    _refresh_minutes    = None
    _refresh_hours      = None
    #for refresh_* only use one of the three in your config. If you use more than one the priority is seconds > minutes > hours


    ################################################################################
    #displays section
    #required
    _display_names      = None
    
    #optional
    _group_names        = None
    #must have a group name for each group of displays if set

    ################################################################################
    #seasons section
    #optional
    _season_names       = None
    _season_start_dates = None
    _season_end_dates   = None
    #if one is set, all three must be

    ################################################################################
    #hourly section
    #optional
    _hourly_names       = None
    _hourly_start_times = None
    _hourly_end_times   = None
    #if one is set, all three must be
   
    def _check_is_type(self, to_check, correct_type, error_msg):
        if not isinstance(to_check, correct_type):
            raise ValueError(f"{error_msg}\nExpected {correct_type.__name__}, but got {type(to_check).__name__}.")
        return True

    def __init__(self, 
                 manager_name, 
                 path, 
                 generic_folder,
                 refresh_seconds,
                 refresh_minutes,
                 refresh_hours,
                 display_names, 
                 group_names,
                 season_names,
                 season_start_dates, #[mm, dd]
                 season_end_dates,   #[mm, dd]
                 hourly_names,
                 hourly_start_times, #[hr, min, sec]
                 hourly_end_times    #[hr, min, sec]
                 ):

        self._check_is_type(manager_name, str, "Manager name isn't a string!")
        if manager_name == "":
            raise ValueError("Manager name is empty!")

        self._check_is_type(path, str, "Wallpaper path isn't a string!")
        if path == "":
            raise ValueError("Wallpaper path is empty!")

        self._check_is_type(display_names, list, "Display names list is malformed! Please refer to docs.")
        for item in display_names:
            self._check_is_type(item, list, "Nested display group lists are malformed!")
            for entry in item:
                self._check_is_type(entry, str, "An entry in your display names list appears to not be a string?")

        self._manager_name       = manager_name
        self._path               = path
        self._display_names      = display_names

        if len(display_names) > 1:
            self._check_is_type(group_names, list, "No group names list assigned despite display names declaring multiple groups.")
            for item in group_names:
                self._check_is_type(item, str, "An entry in your group names list appears to not be a string?")
            
        
        self._group_names        = group_names

        #optional
        #checks occur in getters
        self._generic_folder     = generic_folder
        self._refresh_seconds    = refresh_seconds
        self._refresh_minutes    = refresh_minutes
        self._refresh_hours      = refresh_hours
        self._season_names       = season_names
        self._season_start_dates = season_start_dates
        self._season_end_dates   = season_end_dates
        self._hourly_names       = hourly_names
        self._hourly_start_times = hourly_start_times
        self._hourly_end_times   = hourly_end_times
        self._initialized        = True

    def _ret_field(self, field):
        if self._initialized is True:
            return field
        else:
            return None
            
    #required, so never None if initialized properly
    def get_name(self) -> str:
        name = self._ret_field(self._manager_name)
        assert type(name) is str
        return name

    def get_path(self) -> str:
        path = self._ret_field(self._path)
        assert type(path) is str
        return path.removesuffix("/") #trim trailing slash if needed

    def get_display_names(self) -> List[List[str]]:
        display_names = self._ret_field(self._display_names)
        assert type(display_names) is list
        return display_names

    #optional getters
    #these return defaults if nothing was set
    #DEFAULT = False
    def get_generic_folder(self) -> bool:
        if self._generic_folder is True:
            return True
        else:
            return False

    #returns refresh in seconds
    #DEFAULT = 10 minutes
    def get_refresh(self) -> int:
        if self._refresh_seconds is not None:
            return self._refresh_seconds
        elif self._refresh_minutes is not None:
            return self._refresh_minutes * 60
        elif self._refresh_hours is not None:
            return self._refresh_hours * 60 * 60
        else:
            return 600 

    #DEFAULT = None
    def get_group_names(self) -> Optional[List[str]]:
        if self._group_names is not None:
            #don't need to type check this since it happened in constructor
            return self._group_names

    #returns names, start dates, end dates, in that order
    #DEFAULT = None
    def get_seasons(self) -> Optional[Tuple[ List[str], List[List[int]], List[List[int]] ]]:        
        if (self._season_names       is not None and
            self._season_start_dates is not None and
            self._season_end_dates   is not None):
            if len(self._season_names) == len(self._season_start_dates) and len(self._season_names) == len(self._season_end_dates):
                return self._season_names, self._season_start_dates, self._season_end_dates

    def get_hourly(self) -> Optional[Tuple[ List[str], List[List[int]], List[List[int]] ]]:       
        if (self._hourly_names       is not None and
            self._hourly_start_times is not None and
            self._hourly_end_times   is not None):
            if len(self._hourly_names) == len(self._hourly_start_times) and len(self._hourly_names) == len(self._hourly_end_times):
                return self._hourly_names, self._hourly_start_times, self._hourly_end_times
