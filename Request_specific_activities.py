import pandas as pd
import os
project_root = os.path.dirname(os.path.abspath(__file__))
folder_path_2 = os.path.join(project_root, 'Stations_per_activity_csv')
os.makedirs(folder_path_2, exist_ok=True)


def request_specific_activities():
    while True:
        activity_id = input("What activity would you like to know more about? Or press the return key to return "
                            "to stats.\n")
        if activity_id == "":
            break
        file_path = os.path.join(folder_path_2, f"new_stations_df_{activity_id}.csv")
        if os.path.exists(file_path):
            gps_points_df = pd.read_csv(file_path, index_col=0)
            stations_visited = gps_points_df.index.tolist()
            stations_list = ", ".join(stations_visited)
            print(f"During the activity #{activity_id}, you visited {stations_list}.")
        else:
            print("This activity either doesn't exist, doesn't have any GPS data, or didn't go near any stations."
                  " Why don't you try again?")
