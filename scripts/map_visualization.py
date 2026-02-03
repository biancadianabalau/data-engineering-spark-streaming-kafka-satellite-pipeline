import pandas as pd
import folium


df = pd.read_csv('sample_raw_data.csv', encoding='utf-16')


m = folium.Map(location=[45.9432, 24.9668], zoom_start=5) 

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=row['satname'],
        color='crimson',
        fill=True
    ).add_to(m)

m.save('satellite_map.html')
