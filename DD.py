import pandas as pd
from Station_Locations_pd import station_location_df
import os
def zones_dd():
    while True:
        which_zone = input("Which zone would you like to know more about? 1-9. Press return to exit\n")
        if which_zone == "":
            return
        stations_visited_df_csv = "stations_visited_df.csv"
        stations_visited_df = pd.read_csv(stations_visited_df_csv, index_col=0)
        if int(which_zone) <1 or int(which_zone) >9:
            print("Sorry, please pick a zone between 1 and 9.")
            continue
        stations_in_zone = stations_visited_df[stations_visited_df["Zone"] == int(which_zone)]
        stations_visited = set(stations_in_zone.index.tolist())
        stations_df = station_location_df[station_location_df["Zone"] == int(which_zone)]
        all_zone_stations = set(stations_df.index.tolist())
        stations_missing = all_zone_stations - stations_visited
        if stations_visited:
            print(f"YOU'VE VISITED THESE STATION IN ZONE {which_zone}:")
            for stations in stations_visited:
                print(stations)
        else:
            print(f"No stations visited in Zone {which_zone}.")
        if stations_missing:
            print(f"YOU'RE MISSING THESE STATIONS IN ZONE {which_zone}:")
            for stations in stations_missing:
                print(stations)
        else:
            print(f"You've visited all the stations in Zone {which_zone}! Congratulations!")


def lines_dd():
    while True:
        which_line = str(input("Which line would you like to know more about? Press return to exit\n")).title()
        if which_line == "":
            return
        stations_visited_df_csv = "stations_visited_df.csv"
        stations_visited_df = pd.read_csv(stations_visited_df_csv, index_col=0)
        if not stations_visited_df["Line"].str.contains(which_line, case=False, na=False).any():
            print("Sorry, I don't recognize that line.")
            continue
        stations_on_line = stations_visited_df[stations_visited_df["Line"].str.contains(which_line)]
        stations_visited = set(stations_on_line.index.tolist())
        stations_df = station_location_df[station_location_df["Line"].str.contains(which_line)]
        all_zone_stations = set(stations_df.index.tolist())
        stations_missing = all_zone_stations - stations_visited
        which_line_upper = which_line.upper()
        if stations_visited:
            print(f"STATIONS VISITED ON THE {which_line_upper} LINE:")
            for stations in stations_visited:
                print(stations)
        else:
            print(f"No stations visited in on the {which_line} line.")
        if stations_missing:
            print(f"YOU'RE MISSING THESE STATIONS ON THE {which_line_upper} LINE:")
            for stations in stations_missing:
                print(stations)
        else:
            print(f"You've visited all the stations on the {which_line} line! Congratulations!")


def network_dd():
    while True:
        which_network = str(input("Which network would you like to know more about? Press return to exit\n")).title()
        if which_network == "":
            return
        stations_visited_df_csv = "stations_visited_df.csv"
        stations_visited_df = pd.read_csv(stations_visited_df_csv, index_col=0)
        if not stations_visited_df["Network"].str.contains(which_network, case=False, na=False).any():
            print("Sorry, I don't recognize that network.")
            continue
        stations_in_network = stations_visited_df[stations_visited_df["Network"].str.contains(which_network)]
        stations_visited = set(stations_in_network.index.tolist())
        stations_df = station_location_df[station_location_df["Network"].str.contains(which_network)]
        all_zone_stations = set(stations_df.index.tolist())
        stations_missing = all_zone_stations - stations_visited
        which_network_upper = which_network.upper()
        if stations_visited:
            print(f"STATIONS VISITED ON THE {which_network_upper} NETWORK:")
            for stations in stations_visited:
                print(stations)
        else:
            print(f"No stations visited on the {which_network}.")
        if stations_missing:
            print(f"YOU'RE MISSING THESE STATIONS ON THE {which_network_upper} NETWORK:")
            for stations in stations_missing:
                print(stations)
        else:
            print(f"You've visited all the stations on the {which_network} network! Congratulations!")
