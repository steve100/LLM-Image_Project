
import os
import csv
import time
import exiftool
import requests

# === Configuration ===
image_folder = "./images"
output_csv = "image_metadata_full.csv"
image_extensions = (".jpg", ".jpeg", ".heic", ".png")

# Fields to extract (ExifTool tag names)
fields = [
    "File:FileName",
    "EXIF:DateTimeOriginal",
    "EXIF:Make",
    "EXIF:Model",
    "EXIF:LensModel",
    "EXIF:ISO",
    "EXIF:ShutterSpeedValue",
    "EXIF:ApertureValue",
    "EXIF:FocalLength",
    "EXIF:ImageWidth",
    "EXIF:ImageHeight",
    "EXIF:GPSLongitudeRef",
    "EXIF:GPSLatitudeRef",
    "EXIF:GPSLatitude",
    "EXIF:GPSLongitude",
]

# Reverse geocoding function
def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {'lat': lat, 'lon': lon, 'format': 'json', 'zoom': 10}

    # you may need a real email in the future
    headers = {'User-Agent': 'ExifLocationApp/1.0 (your_email@example.com)'}

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', 'N/A')
    except Exception as e:
        print(f"Reverse geocode error: {e}")
    return 'N/A'

# Safe float conversion
def safe_float(val):
    try:
        if isinstance(val, list):
            val = val[0]
        return float(val)
    except:
        return None

# Extract metadata and write CSV
def extract_and_write():
    files = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(image_extensions)
    ]

    with exiftool.ExifTool() as et, open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f.split(":")[-1] for f in fields] + ['Location'])

        metadata_list = et.get_metadata_batch(files)

        for data in metadata_list:
            row = []
            lat_ref = lon_ref = None
            gps_lat = gps_lon = None

            for key in fields:
                value = data.get(key, 'N/A')
                short_key = key.split(":")[-1]

                if short_key == "GPSLatitudeRef":
                    lat_ref = value
                elif short_key == "GPSLongitudeRef":
                    lon_ref = value
                elif short_key == "GPSLatitude":
                    val = safe_float(value)
                    if val is not None:
                        gps_lat = -val if lat_ref == "S" else val
                    value = gps_lat if gps_lat is not None else 'N/A'
                elif short_key == "GPSLongitude":
                    val = safe_float(value)
                    if val is not None:
                        gps_lon = -val if lon_ref == "W" else val
                    value = gps_lon if gps_lon is not None else 'N/A'

                row.append(value)

            if gps_lat is not None and gps_lon is not None:
                location = reverse_geocode(gps_lat, gps_lon)
            else:
                location = 'No GPS data'

            row.append(location)
            writer.writerow(row)
            print(f"Processed: {row[0]}")

            #because we are using the rate-limited free version
            time.sleep(1)

if __name__ == "__main__":
    extract_and_write()
    print(f"\n✅ Done. Metadata saved to: {output_csv}")
