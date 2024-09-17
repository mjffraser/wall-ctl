from typing import List, Tuple, Optional

class ConfigSpecs:
    initialized        = False

    ################################################################################
    #config section
    #required
    _manager_name       = None
    _path               = None

    #optional
    _generic_folder     = None
    _freq               = None
    _preload_buffer     = None
    _refresh_seconds    = None
    _refresh_minutes    = None
    _refresh_hours      = None
    #for refresh_* only use one of the three in your config. If you use more than one the priority is seconds > minutes > hours

    '''
    If dgroup_force_different_choice (dg_diff) is set True, dgroup_force_same_choice (dg_same) is set False irregardless of the config
    These flags are contradictory in their behavior, but three actual behaviors exist:
    - dg_same=True,  dg_diff=False (DEFAULT) -> If possible, all groups will be set to wallpapers with the same name
    - dg_same=False, dg_diff=True            -> If possible, all groups will select wallpapers with different names
    - dg_same=False, dg_diff=False           -> Wallpapers are selected without any checks for matching file names
    '''
    _dgroup_force_same_choice      = None #if one group selects x.png, if x.png also exists in other groups it will be selected for that other group 
    _dgroup_force_different_choice = None #if one group selects x.png, if x.png also exists in other groups it will never be selected for that other group unless it's the only available choice

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
                 freq,
                 preload_buffer,
                 refresh_seconds,
                 refresh_minutes,
                 refresh_hours,
                 dgroup_force_same_choice,
                 dgroup_force_different_choice,
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

        self._manager_name  = manager_name
        self._path          = path
        self._display_names = display_names
        self._group_names   = group_names

        if len(display_names) > 1:
            self._check_is_type(group_names, list, "No group names list assigned despite display names declaring multiple groups.")
            for item in group_names:
                self._check_is_type(item, str, "An entry in your group names list appears to not be a string?")

        #optional
        #checks occur in getters
        self._generic_folder                = generic_folder
        self._freq                          = freq
        self._preload_buffer                = preload_buffer
        self._refresh_seconds               = refresh_seconds
        self._refresh_minutes               = refresh_minutes
        self._refresh_hours                 = refresh_hours
        self._dgroup_force_same_choice      = dgroup_force_same_choice
        self._dgroup_force_different_choice = dgroup_force_different_choice
        self._season_names                  = season_names
        self._season_start_dates            = season_start_dates
        self._season_end_dates              = season_end_dates
        self._hourly_names                  = hourly_names
        self._hourly_start_times            = hourly_start_times
        self._hourly_end_times              = hourly_end_times

    #required, so never None if initialized properly
    def get_name(self) -> str:
        name = self._manager_name
        assert type(name) is str
        return name

    def get_path(self) -> str:
        path = self._path
        assert type(path) is str
        return path.removesuffix("/") #trim trailing slash if needed

    def get_display_names(self) -> List[List[str]]:
        display_names = self._display_names
        assert type(display_names) is list
        return display_names

    '''
    optional getters
    these return defaults if nothing was set
    DEFAULT = False
    '''
    def get_generic_folder(self) -> bool:
        if self._generic_folder is True:
            return True
        else:
            return False

    '''
    returns freq in seconds
    this is how often the loop should check for group changes, and or if a wallpaper refresh should happen
    in other words, this is the amount of time the loop sleeps for
    DEFAULT = 10 minutes
    '''
    def get_check_freq(self) -> int:
        if self._freq is not None:
            return self._freq
        else:
            return 600

    '''
    returns amount of time in seconds that the next group of wallpapers should be preloaded before actually loading in
    DEFAULT = 30 seconds
    '''
    def get_preload_buffer(self) -> int:
        refresh = self.get_refresh()
        if self._preload_buffer is not None:
            if self._preload_buffer < refresh:
                return self._preload_buffer
        
        if refresh > 30:
            return 30
        else:
            return 1

    '''
    returns refresh in seconds
    this is how often wallpapers should swap, not how often checks to swap happen
    DEFAULT = 1 hour
    '''
    def get_refresh(self) -> int:
        if self._refresh_seconds is not None:
            return self._refresh_seconds
        elif self._refresh_minutes is not None:
            return self._refresh_minutes * 60
        elif self._refresh_hours is not None:
            return self._refresh_hours * 60 * 60
        else:
            return 3600 

    '''
    returns id code to determine selection behavior, with the first code indicating behavior between separate groups, and the second for within a group

    first id:
    0 -> TF default behavior defined above
    1 -> FT behavior defined above
    2 -> FF behavior defined above
    '''
    def get_selection_type(self) -> int:
        if self._dgroup_force_same_choice is None and self._dgroup_force_different_choice is not None: #user only set different choice
            if self._dgroup_force_different_choice is True:
                return 1
            else: #is false, so default TF behavior
                return 0
        elif self._dgroup_force_same_choice is not None and self._dgroup_force_different_choice is None:
            if self._dgroup_force_same_choice is True:
                return 0
            else:
                return 1
        elif self._dgroup_force_same_choice is not None and self._dgroup_force_different_choice is not None:
            if self._dgroup_force_same_choice is False:
                if self._dgroup_force_different_choice is True:
                    return 1
                else:
                    return 2

            #if same is set True it means default behavior. Alternatively, if TT is set, the default is also used.
            return 0

        else:
            return 0

    '''
    DEFAULT = None
    '''
    def get_group_names(self) -> Optional[List[str]]:
        if self._group_names is not None:
            #don't need to type check this since it happened in constructor
            return self._group_names

    '''
    returns names, start dates, end dates, in that order
    dates are in the format [month, day]
    DEFAULT = None
    '''
    def get_seasons(self) -> Optional[Tuple[ List[str], List[List[int]], List[List[int]] ]]:        
        if (self._season_names       is not None and
            self._season_start_dates is not None and
            self._season_end_dates   is not None):
            if len(self._season_names) == len(self._season_start_dates) and len(self._season_names) == len(self._season_end_dates):
                return self._season_names, self._season_start_dates, self._season_end_dates

    '''
    returns names, start times, end times, in that order.
    times are in the format [hr, min, sec]
    '''
    def get_hourly(self) -> Optional[Tuple[ List[str], List[List[int]], List[List[int]] ]]:       
        if (self._hourly_names       is not None and
            self._hourly_start_times is not None and
            self._hourly_end_times   is not None):
            if len(self._hourly_names) == len(self._hourly_start_times) and len(self._hourly_names) == len(self._hourly_end_times):
                return self._hourly_names, self._hourly_start_times, self._hourly_end_times
