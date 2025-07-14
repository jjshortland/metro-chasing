import gpxpy
import gpxpy.gpx
import pandas as pd

lat_coords = []
long_coords = []
def find_path_coordinates(gpxfile):
    file = open(gpxfile, "r")
    gpx = gpxpy.parse(file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat_coords.append(point.latitude)
                long_coords.append(point.longitude)
    gps_points_df = pd.DataFrame({"Latitude": lat_coords, "Longitude": long_coords})
    return gps_points_df


