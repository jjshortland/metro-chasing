from Station_Locations_pd import station_location_df
from Request_specific_activities import request_specific_activities
from DD import *
import pandas as pd
import os
project_root = os.path.dirname(os.path.abspath(__file__))
folder_path_2 = os.path.join(project_root, 'Stations_per_activity_csv')
os.makedirs(folder_path_2, exist_ok=True)


def statistics():
    stations_visited_df_csv = "stations_visited_df.csv"
    stations_visited_df = pd.read_csv(stations_visited_df_csv, index_col=0)

    network_names = ["London Underground", "London Overground", "DLR", "Tramlink", "TfL Rail"]
    line_names = ["District", "Central", "Victoria", "Hammersmith & City", "Bakerloo", "Piccadilly",
                  "Northern", "Jubilee", "Waterloo & City", "Metropolitan", "Circle", "London Overground", "DLR"]

    while True:
        stats_request = str(input("Would you like to know about your networks, lines or zones? Or type activities to "
                                  "search by activity number. Press the return key to exit.\n")).upper()
        if stats_request == "ZONES":
            for x in range(1, 10):
                zone_count = (station_location_df["Zone"] == x).sum()
                zone_visited = (stations_visited_df["Zone"] == x).sum()
                zone_percentage = round((zone_visited/zone_count*100), 2)
                print(f"You have visited {zone_visited}/{zone_count} ({zone_percentage}%) of Zone {x} stations.")
            deeper_dive = str(input("Would you like to take a deeper dive into your zones? y/n\n")).upper()
            if deeper_dive == "Y":
                    zones_dd()
            else:
                continue
        elif stats_request == "LINES":
            for line in line_names:
                line_count = (station_location_df["Line"].str.contains(line).sum())
                line_visited = (stations_visited_df["Line"].str.contains(line).sum())
                line_percentage = round((line_visited/line_count*100), 2)
                print(f"You have visited {line_visited}/{line_count} ({line_percentage}%) of the {line} Line")
            deeper_dive = str(input("Would you like to take a deeper dive into your lines? y/n\n")).upper()
            if deeper_dive == "Y":
                lines_dd()
            else:
                continue
        elif stats_request == "NETWORKS":
            for network in network_names:
                network_count = (station_location_df["Network"].str.contains(network).sum())
                network_visited = (stations_visited_df["Network"].str.contains(network).sum())
                network_percentage = round((network_visited / network_count * 100), 2)
                print(f"You have visited {network_visited}/{network_count} ({network_percentage}%) of the {network}")
            deeper_dive = str(input("Would you like to take a deeper dive into your networks? y/n\n")).upper()
            if deeper_dive == "Y":
                network_dd()
            else:
                continue
        elif stats_request == "ACTIVITIES":
            request_specific_activities()
        elif stats_request == "":
            print("Thanks for your interest!")
            break
        else:
            print("Sorry, I don't understand, please try again!")
