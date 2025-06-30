import pandas as pd
import folium

# Step 1: Load the CSV file
csv_file = 'image_metadata_full.csv'  # Change this to your actual CSV filename
df = pd.read_csv(csv_file)

# Step 2: Center map on average coordinates
avg_lat = df['GPSLatitude'].mean()
avg_lon = df['GPSLongitude'].mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)

# Step 3: Add points to the map
for idx, row in df.iterrows():

    print(row['GPSLatitude'], row['GPSLongitude']) 
    # if gps_lat != 'N/A' and gps_lon != 'N/A':
    print(f"lat,long {row['GPSLatitude']}, {row['GPSLongitude']} ")
    popup_text = f"""
    <b>File:</b> {row['FileName']}<br>
    <b>Datetime:</b> {row['DateTimeOriginal']}<br>
    <b>Location:</b> {row['Location']}
    """
    folium.Marker(
        location=[row['GPSLatitude'], row['GPSLongitude']],
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='camera', prefix='fa')
    ).add_to(m)

# Step 4: Save the map to an HTML file
m.save("photo_map.html")
print("Map saved as 'photo_map.html'")
