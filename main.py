from model import SessionLocal, ProcessedActivity, StationInfo, StationVisit
from dotenv import load_dotenv
import os
import requests
import time
import numpy as np
from datetime import datetime


# new single function that processes activities with GPS data on load in
def process_new_activities():
    # activate session for SQl database
    session = SessionLocal()

    # Strava API calls, user information currently saved in .env files.

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

    # check ProcessedActivity SQL table for activities that have already been processed

    processed_ids = {id[0] for id in session.query(ProcessedActivity.strava_id).all()}
    print(f'Already processed: {len(processed_ids)} activities.')

    # fetch activities from Strava

    all_activities = []
    page = 1

    while True:
        param = {"page": page, "per_page": 200}
        activities = requests.get(activities_url, headers=header, params=param).json()
        # if there's no activities, break
        if len(activities) == 0:
            break

        # check if the new activities are in the SQL DB, if not they're new activities and are kept.
        new_activities = [a for a in activities if a["id"] not in processed_ids]
        all_activities.extend(new_activities)
        page += 1

    print(f"Found {len(all_activities)} new activities to process")

    if len(all_activities) == 0:
        print("Nothing to do!")
        session.close()
        return

    # load all station information from the StationInfo SQL table
    all_stations = session.query(StationInfo).all()
    print(f'Loaded all {len(all_stations)} stations!')

    # process all activities

    # tolerance set at ~200m
    tolerance = 0.002
    request_count = 0
    start_time = time.time()

    for activity in all_activities:
        activity_id = activity['id']
        activity_date = datetime.fromisoformat(activity["start_date"].replace('Z', '+00:00'))
        activity_name = activity['name']
        activity_type = activity['sport_type']

        # fetch GPS data
        latlng_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=latlng&key_by_type=true"
        latlng_test = requests.get(latlng_url, headers=header).json()
        request_count += 1

        # prepare activity record for given activity
        activity_record = ProcessedActivity(
            strava_id=activity_id,
            date=activity_date,
            processed_at=datetime.now(),
            activity_name=activity_name,
            activity_type=activity_type
        )

        session.add(activity_record)

        # if there's no associated latlng data, save information to DB and move to next activity
        if 'latlng' not in latlng_test:
            print(f'Activity {activity_id}: no GPS data found.')
            session.commit()
            continue

        # extract gps points for comparison with station information
        gps_points = latlng_test['latlng']['data']
        gps_lats = np.array([point[0] for point in gps_points])
        gps_long = np.array([point[1] for point in gps_points])

        # check each station against the latitude/longitude pairs, checking against the tolerance
        stations_found = 0
        for station in all_stations:
            lat_diff = np.abs(gps_lats - station.latitude)
            long_diff = np.abs(gps_long - station.longitude)
            within_tolerance = (lat_diff <= tolerance) & (long_diff <= tolerance)

            if within_tolerance.any():
                # record station visit
                visit = StationVisit(
                    strava_id=activity_id,
                    station_id=station.id
                )

                session.add(visit)
                stations_found += 1

        print(f"Activity {activity_id}: {len(gps_points)} GPS points → {stations_found} stations")
        session.commit()

        if request_count >= 90:
            elapsed = time.time() - start_time
            if elapsed < 900:  # 15 minutes
                wait_time = 900 - elapsed
                print(f"Rate limit: waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time)
            start_time = time.time()
            request_count = 0

    total_visits = session.query(StationVisit).count()
    unique_stations = session.query(StationVisit.station_id).distinct().count()

    print("\n" + "=" * 50)
    print("✓ PROCESSING COMPLETE")
    print("=" * 50)
    print(f"Total station visits: {total_visits}")
    print(f"Unique stations: {unique_stations}")

    session.close()
