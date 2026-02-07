# load_stations.py
from model import Base, engine, SessionLocal, StationInfo
from Station_Locations_pd import station_location_df

# This creates all tables (including station_info with the id column)
Base.metadata.create_all(engine)

# Now populate with your DataFrame data
session = SessionLocal()

for _, row in station_location_df.iterrows():
    station = StationInfo(
        name=row['name'],
        latitude=row['latitude'],
        longitude=row['longitude'],
        zone=row['zone'],
        network=row['network'],
        line=row['line']
    )
    session.add(station)

session.commit()
session.close()
print(f'✓ Loaded {len(station_location_df)} stations')

