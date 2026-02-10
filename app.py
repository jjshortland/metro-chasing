# app.py
from flask import Flask, render_template, jsonify
from model import SessionLocal, StationVisit, StationInfo, ProcessedActivity

app = Flask(__name__)


def get_all_stations_geojson():
    """Get all stations with visited status"""
    session = SessionLocal()

    try:
        # Get all stations
        all_stations = session.query(StationInfo).all()

        # Get set of visited station IDs
        visited_station_ids = set(
            visit.station_id for visit in session.query(StationVisit).all()
        )

        features = []
        for station in all_stations:
            feature = {
                'type': 'Feature',
                'properties': {
                    'name': station.name,
                    'line': station.line,
                    'visited': station.id in visited_station_ids,  # ✅ Track visited status
                    'zone': station.zone if hasattr(station, 'zone') else None
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [station.longitude, station.latitude]
                }
            }
            features.append(feature)

        return {
            'type': 'FeatureCollection',
            'features': features
        }

    finally:
        session.close()

@app.route('/api/all-stations')
def get_all_stations():
    """Get all stations with visited status"""
    geojson = get_all_stations_geojson()
    return jsonify(geojson)

@app.route('/')
def home():
    """Homepage - show your stats"""
    session = SessionLocal()

    unique_stations = session.query(StationVisit.station_id).distinct().count()
    total_activities = session.query(ProcessedActivity).count()

    session.close()

    return render_template('index.html',
                           total_visits=unique_stations,
                           unique_stations=(f'{round((unique_stations/498*100),2)}%'),
                           total_activities=total_activities)


@app.route('/stations')
def stations():
    """List all stations you've visited"""
    session = SessionLocal()

    # Get all your visits with station info
    visits = session.query(StationVisit).all()

    # Group by station
    station_counts = {}
    for visit in visits:
        station_name = visit.station.name
        if station_name not in station_counts:
            station_counts[station_name] = {
                'name': station_name,
                'zone': visit.station.zone,
                'lines': visit.station.line,
                'count': 0
            }
        station_counts[station_name]['count'] += 1

    stations_list = sorted(station_counts.values(), key=lambda x: x['count'], reverse=True)

    session.close()

    return render_template('stations.html', stations=stations_list)


@app.route('/lines')
def lines():
    session = SessionLocal()

    visits = session.query(StationVisit).all()
    all_stations = session.query(StationInfo).all()

    # Track visited stations per line
    visited_stations_by_line = {}
    for visit in visits:
        lines = visit.station.line.split(',')
        for line in lines:
            line = line.strip()
            if line not in visited_stations_by_line:
                visited_stations_by_line[line] = set()
            visited_stations_by_line[line].add(visit.station.name)

    # Track ALL stations per line
    total_stations_by_line = {}
    for station in all_stations:
        lines = station.line.split(',')

        for line in lines:
            line = line.strip()

            if line not in total_stations_by_line:
                total_stations_by_line[line] = set()

            total_stations_by_line[line].add(station.name)

    # Build the final list with percentages and missing stations
    line_list = []
    for line in total_stations_by_line.keys():
        total = len(total_stations_by_line[line])
        visited_set = visited_stations_by_line.get(line, set())  # Returns empty set if line not visited
        visited = len(visited_set)

        # Calculate percentage
        percentage = (visited / total * 100) if total > 0 else 0

        # Find missing stations (set difference)
        missing_stations = total_stations_by_line[line] - visited_set

        line_list.append({
            'line': line,
            'visited': visited,
            'total': total,
            'percentage': round(percentage, 1),
            'visited_stations': sorted(visited_set),  # Sorted list for display
            'missing_stations': sorted(missing_stations)  # Sorted list of what's left
        })

    # Sort by percentage (highest first)
    line_list = sorted(line_list, key=lambda x: x['percentage'], reverse=True)

    session.close()

    return render_template('lines.html', lines=line_list)


@app.route('/zones')
def zones():
    session = SessionLocal()

    visits = session.query(StationVisit).all()
    all_stations = session.query(StationInfo).all()

    # Track visited stations per zone
    visited_stations_by_zone = {}
    for visit in visits:
        zone = visit.station.zone  # Just get the zone directly

        if zone not in visited_stations_by_zone:
            visited_stations_by_zone[zone] = set()

        visited_stations_by_zone[zone].add(visit.station.name)

    # Track ALL stations per zone
    total_stations_by_zone = {}
    for station in all_stations:
        zone = station.zone  # Just get the zone directly

        if zone not in total_stations_by_zone:
            total_stations_by_zone[zone] = set()

        total_stations_by_zone[zone].add(station.name)

    # Build the final list with percentages and missing stations
    zone_list = []
    for zone in total_stations_by_zone.keys():
        total = len(total_stations_by_zone[zone])
        visited_set = visited_stations_by_zone.get(zone, set())
        visited = len(visited_set)

        # Calculate percentage
        percentage = (visited / total * 100) if total > 0 else 0

        # Find missing stations (set difference)
        missing_stations = total_stations_by_zone[zone] - visited_set

        zone_list.append({
            'zone': zone,
            'visited': visited,
            'total': total,
            'percentage': round(percentage, 1),
            'visited_stations': sorted(visited_set),
            'missing_stations': sorted(missing_stations)
        })

    # Sort by zone number (Zone 1, Zone 2, etc.)
    zone_list = sorted(zone_list, key=lambda x: x['zone'])

    session.close()

    return render_template('zones.html', zones=zone_list)  # Changed 'lines' to 'zones'!

if __name__ == '__main__':
    app.run(debug=True, port=5001)