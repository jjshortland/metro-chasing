import numpy as np
import pandas as pd
import os
from Station_Locations_pd import station_location_df


def stations_visited():
    stations_visited_df_csv = "stations_visited_df.csv"
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GPS_points_csv")

    if os.path.exists(stations_visited_df_csv):
        stations_visited_df = pd.read_csv(stations_visited_df_csv, index_col=0)
        print("Loading stations_visited_df...")
    else:
        stations_visited_df = pd.DataFrame()
        print("stations_visited_df does not exist, creating now...")
    for file_name in os.listdir(folder_path):
        new_stations_df = pd.DataFrame()
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            gps_points_df = pd.read_csv(file_path)

        def compare_rows(row_to_check, tolerance=0.002):  #0.002=200m
            latitude_difference = np.abs(gps_points_df["latitude"] - row_to_check["latitude"])
            longitude_difference = np.abs(gps_points_df["longitude"] - row_to_check["longitude"])
            exists_within_tolerance = (latitude_difference <= tolerance) & (longitude_difference <= tolerance)
            if exists_within_tolerance.any():
                return row_to_check
        for x in range(len(station_location_df)):
            matched_row = compare_rows(station_location_df.iloc[x])
            if matched_row is not None:
                new_stations_df = pd.concat([new_stations_df, matched_row.to_frame().T], ignore_index=False)
        filtered_stations = new_stations_df[~new_stations_df.index.isin(stations_visited_df.index)]
        if not filtered_stations.empty:
            print("Adding the new stations now!")
            stations_visited_df = pd.concat([stations_visited_df, filtered_stations], ignore_index=False)
        stations_visited_df.to_csv(stations_visited_df_csv)
