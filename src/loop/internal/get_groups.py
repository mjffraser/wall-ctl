from typing             import List
from config.read_config import ConfigSpecs
from datetime           import datetime, timedelta

def _between_hours(now: datetime, hour_start: List[int], hour_end: List[int]) -> bool:
    if len(hour_start) < 3 or len(hour_end) < 3:
        return False

    hour_start_corrected = now.replace(hour=hour_start[0], minute=hour_start[1], second=hour_start[2])
    hour_end_corrected = now.replace(hour=hour_end[0], minute=hour_end[1], second=hour_end[2])

    #account for a period that crossed midnight, ex. start=22, end=4
    if hour_start_corrected.hour > hour_end_corrected.hour:
        if (now.hour >= hour_start_corrected.hour):
            #this means same day  
            hour_end_corrected += timedelta(days=1)  
        else:
            #this means we're the morning of, and that's where our now snapshot was taken, so we instead decrement the start date
            hour_start_corrected -= timedelta(days=1)

    if now >= hour_start_corrected and now <= hour_end_corrected:
        return True

    return False


def _between_dates(now: datetime, date_start: List[int], date_end: List[int]) -> bool:
    if len(date_start) < 2 or len(date_end) < 2:
        return False

    date_start_corrected = now.replace(month=date_start[0], day=date_start[1])
    date_end_corrected = now.replace(month=date_end[0], day=date_end[1])

    #account for a period that crosses over the new year
    if date_start_corrected > date_end_corrected:
        date_end_corrected = date_end_corrected.replace(year=date_end_corrected.year+1)
        
    if now >= date_start_corrected and now <= date_end_corrected:
        return True

    return False

def _get_hourly(specs: ConfigSpecs, now: datetime) -> List[str]:
    names = []
    hourly = specs.get_hourly()
    if hourly is not None:
        hourly_names, start_dates, end_dates = hourly
        for i, name in enumerate(hourly_names):
            if _between_hours(now, start_dates[i], end_dates[i]) is True:
                names.append(name)

    return names
             

def _get_seasons(specs: ConfigSpecs, now: datetime) -> List[str]:
    names = []
    seasons = specs.get_seasons()
    if seasons is not None:
        season_names, start_dates, end_dates = seasons
        for i, name in enumerate(season_names):
            if _between_dates(now, start_dates[i], end_dates[i]) is True:
                names.append(name)

    return names
    

def _get_groups(specs: ConfigSpecs) -> List[str]:
    names = []
    group_names = specs.get_group_names()
    if group_names is not None:
        for g in group_names:
            names.append(g)
    return names

    
def get_group_paths(specs: ConfigSpecs) -> List[str]:
    now = datetime.now()
    all_selections = []
    groups  = _get_groups (specs)
    seasons = _get_seasons(specs, now)
    hourly  = _get_hourly (specs, now)

    group_lists = []
    if len(groups) > 0: 
        for g in groups:
            group_lists.append(g)
    else:
        group_lists.append("")

    season_lists = []
    if len(seasons) > 0:
        for g in group_lists:
            for s in seasons:
                to_add = g
                if len(g) != 0: #has a group, so needs a divider
                    to_add += "/"
                to_add += s
                season_lists.append(to_add)

    hourly_lists = []
    if len(hourly) > 0:
        if len(season_lists) > 0:
            for s in season_lists:
                for h in hourly:
                    hourly_lists.append(s + "/" + h)

        else: #no seasons, but groups is always populated, even if with the empty string
            for g in group_lists:
                for h in hourly:
                    to_add = g
                    if len(g) != 0:
                        to_add += "/"
                    to_add += h
                    hourly_lists.append(to_add)

    all_selections += group_lists
    all_selections += season_lists
    all_selections += hourly_lists

    abs_path_selections = []
    base_path = specs.get_path()
    for path in all_selections:
        if len(path) != 0:
            abs_path_selections.append(base_path + "/" + path)
        else:
            abs_path_selections.append(base_path)

    return abs_path_selections 

    
