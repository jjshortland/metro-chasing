import json
import requests
import pandas as pd
import os
import time
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
What's needed: 
- Expand latlng_df function to work with import limits, 100 requests every 15 minutes
- keep list of id's that have already been run, to avoid calling old activities unnecessarily: probably easiest to keep
a separate list that is appended within the loop (this could be linked with the first point, to ensure only the needed
requests are made)
- needs to be a check whether the activity contains GPS data. Some types of activity (indoor/treadmill runs, etc) will
not contain GPS data which will break the program. Either do that here or in the Activity_ID get. I think here makes
the most sense. Nesting an IF statement that checks the existence of "latlng" might be useful here.
'''
auth_token_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"

load_dotenv(dotenv_path='.env')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
refresh_token = os.getenv('refresh_token')

auth_token_payload = {
    "client_id": str(client_id),
    "client_secret": str(client_secret),
    "refresh_token": str(refresh_token),
    "grant_type": "refresh_token",
    "f": "json"}

def get_latlng():
    res = requests.post(auth_token_url, data=auth_token_payload, verify=False)
    access_token = res.json()["access_token"]
    header = {"Authorization": "Bearer " + access_token}

    project_root = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(project_root, 'GPS_points_csv')
    os.makedirs(folder_path, exist_ok=True)

    id_checked_list = []
    temporary_id_list = []
    id_list_with_latlng = []

    with open("activity_id_list.json", "r") as f:
        activity_id_list = json.load(f)
    try:
        with open("id_checked_list.json", "r") as f:
            id_checked_list = json.load(f)
            print("Loaded id_checked_list from JSON file")
    except FileNotFoundError:
        print("JSON file not found, creating new JSON file...")

    try:
        with open("id_list_with_latlng.json", "r") as f:
            id_list_with_latlng = json.load(f)
            print("Loaded id_list_with_latlng")
    except FileNotFoundError:
        print("id_list_with_latlng JSON file not found, creating new JSON file")

    for ids in activity_id_list:
        if ids not in id_checked_list:
            temporary_id_list.append(ids)

    def latlng_df(activity_id):
        latlng_lat = []
        latlng_lng = []
        latlng_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
        latlng_test = requests.get(latlng_url, headers=header).json()
        if "latlng" in latlng_test:
            for x in range(len(latlng_test["latlng"]["data"])):
                latlng_lat.append(latlng_test["latlng"]["data"][x][0])
                latlng_lng.append(latlng_test["latlng"]["data"][x][1])
                gps_points_df = pd.DataFrame({"Latitude": latlng_lat, "Longitude": latlng_lng})
                file_path = os.path.join(folder_path, f"gps_points_{activity_id}.csv")
                gps_points_df.to_csv(file_path, index=False)
            id_list_with_latlng.append(activity_id)
        else:
            print(f"There is no latlng data associated with this activity: '{activity_id}'")
        id_checked_list.append(activity_id)

    def pull_coord_with_time(list_of_ids, request_per_interval=90, interval_seconds=900):
        request_count = 0
        start_time = time.time()
        current_time = time.time()
        elapsed_time = current_time - start_time
        for activity_ids in list_of_ids:
            latlng_df(activity_ids)
            request_count += 1
            print(f"Activities added: {activity_ids}")
            if request_count >= request_per_interval:
                print("It's time to stop before Strava bans us")
                time_to_wait = interval_seconds - elapsed_time % interval_seconds
                time.sleep(time_to_wait)
                start_time = time.time()
                request_count = 0
            if elapsed_time >= interval_seconds:
                print("You've gained more time!")
                start_time = time.time()
                request_count = 0

    pull_coord_with_time(temporary_id_list)
    with open("id_checked_list.json", "w") as f:
        json.dump(id_checked_list, f)

    with open("id_list_with_latlng.json", "w") as f:
        json.dump(id_list_with_latlng, f)
