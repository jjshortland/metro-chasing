import os
import pandas as pd
from Station_names import station_names
def station_stats():
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Stations_per_activity_csv")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            stations_visited = pd.read_csv(file_path)
            print(stations_visited)
            for stations in station_names:
                if stations in stations_visited:
                    print(stations)

station_stats()