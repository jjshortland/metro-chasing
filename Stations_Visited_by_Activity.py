import json
import pandas as pd
import os
import numpy as np
from Station_Locations_pd import station_location_df

def stations_visited_per_activity():
    individual_activity_id_checked_list = []
    temporary_id_list = []
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GPS_points_csv")

    project_root = os.path.dirname(os.path.abspath(__file__))
    folder_path_2 = os.path.join(project_root, 'Stations_per_activity_csv')
    os.makedirs(folder_path_2, exist_ok=True)

    with open("id_list_with_latlng.json", "r") as f:
        activity_id_list = json.load(f)
    try:
        with open("individual_activity_id_checked_list.json", "r") as f:
            individual_activity_id_checked_list = json.load(f)
            print("Loaded individual_activity_id_checked_list from JSON file")
    except FileNotFoundError:
        print("JSON file not found, creating new JSON file...")
    for ids in activity_id_list:
        if ids not in individual_activity_id_checked_list:
            temporary_id_list.append(ids)

    for ids in temporary_id_list:
        new_stations_df_csv = os.path.join(folder_path_2, f"new_stations_df_{ids}.csv")
        new_stations_df = pd.DataFrame()
        file_path = os.path.join(folder_path, f"gps_points_{ids}.csv")
        gps_points_df = pd.read_csv(file_path)
        def compare_rows(row_to_check, tolerance=0.002):  #0.002=200m
            latitude_difference = np.abs(gps_points_df["Latitude"] - row_to_check["Latitude"])
            longitude_difference = np.abs(gps_points_df["Longitude"] - row_to_check["Longitude"])
            exists_within_tolerance = (latitude_difference <= tolerance) & (longitude_difference <= tolerance)
            if exists_within_tolerance.any():
                return row_to_check
        for x in range(len(station_location_df)):
            matched_row = compare_rows(station_location_df.iloc[x])
            if matched_row is not None:
                new_stations_df = pd.concat([new_stations_df, matched_row.to_frame().T], ignore_index=False)
        if not new_stations_df.empty:
            new_stations_df.to_csv(new_stations_df_csv, index=True)
        individual_activity_id_checked_list.append(ids)
    with open("individual_activity_id_checked_list.json", "w") as f:
        json.dump(individual_activity_id_checked_list, f)
