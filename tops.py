import requests
import geojson

# Define the bounding box of Romania
bbox = "22.3642,43.6311,29.7334,48.2654"

# Define the query to search for mountain peaks
query = "[natural=peak][mountain=yes]"

# Define the API endpoint to use
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox}&{query}"

# Make the request to the API and get the response
response = requests.get(url)

# Parse the XML response into a GeoJSON FeatureCollection
features = []
for node in response.content:
    if node.tag == "node":
        lat = node.get("lat")
        lon = node.get("lon")
        name = node.findtext("tag[@k='name']")
        features.append(
            geojson.Feature(
                geometry=geojson.Point((float(lon), float(lat))),
                properties={"name": name},
            )
        )
feature_collection = geojson.FeatureCollection(features)

# Write the GeoJSON to a file
with open("romania_mountain_peaks.geojson", "w") as f:
    json.dump(feature_collection, f)
