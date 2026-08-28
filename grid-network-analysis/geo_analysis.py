import pandas as pd
from geopy.distance import geodesic

substations = pd.read_csv('data_sets/substations.csv')

# Build the lookup dictionary
substation_coords = {}
for index, row in substations.iterrows():
    substation_coords[row['Substation ID']] = (row['Latitude'], row['Longitude'])

#print(substation_coords)

lines = pd.read_csv('data_sets/lines.csv')

results = []

for index, row in lines.iterrows():
    source_id = row['Source Substation ID']
    dest_id = row['Destination Substation ID']
    
    source_coords = substation_coords[source_id]
    dest_coords = substation_coords[dest_id]
    
    computed_km = geodesic(source_coords, dest_coords).km
    stated_km = row['Length (km)']
    difference = abs(computed_km - stated_km)
    
    results.append({
        'line_id': row['Line ID'],
        'computed_km': computed_km,
        'stated_km': stated_km,
        'difference': difference
    })

results_df = pd.DataFrame(results)
print(results_df.head())
print(results_df.describe())