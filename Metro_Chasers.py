#!/usr/bin/env python3
from Strava_Get_Activity_IDs import get_activity_ids
from Strava_Get_LatLng import get_latlng
from Stations_Visited_pd import stations_visited
from Statistics import statistics
from Stations_Visited_by_Activity import stations_visited_per_activity

get_activity_ids()
get_latlng()
stations_visited()
stations_visited_per_activity()
stats = str(input("Your database has been updated, would you like to look at your stats? Y/N\n")).upper()
if stats == "Y":
    statistics()
elif stats == "N":
    print("Have a lovely day.")