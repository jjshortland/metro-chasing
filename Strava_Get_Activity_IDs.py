import requests
import urllib3
import json
import os
from dotenv import load_dotenv


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_activity_ids():
    activity_id_list = []
    all_activities = []

    try:
        with open("activity_id_list.json", "r") as f:
            activity_id_list = json.load(f)
            print("Loaded activity_id_list from JSON file")
    except FileNotFoundError:
        print("JSON file not found, fetching data from API")

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

    res = requests.post(auth_token_url, data=auth_token_payload, verify=False)

    access_token = res.json()["access_token"]
    header = {"Authorization": "Bearer " + access_token}

    import_page_number = 1
    new_activities_found = False

    while True:
        param = {"page": import_page_number, "per_page": 200}
        my_dataset = requests.get(activities_url, headers=header, params=param).json()
        if len(my_dataset) == 0:
            break
        for activity in my_dataset:
            if activity["id"] not in activity_id_list:
                activity_id_list.append(activity["id"])
                all_activities.append(activity)
                new_activities_found = True
        import_page_number += 1

    if new_activities_found:
        with open("activity_id_list.json", "w") as f:
            print("New activities found, updating JSON")
            json.dump(activity_id_list, f)
    else:
        print("No new activities found. JSON file remains the same.")
