from model import engine
from Station_Locations_pd import station_location_df

print(station_location_df.columns.tolist())
print(station_location_df['name'])

station_location_df.to_sql('station_info', engine, if_exists='replace', index=False)
print(f'Loaded {len(station_location_df)} stations')

