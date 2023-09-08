import json
import pandas as pd

# Load the GeoJSON file
with open("./data/unitati_relief.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract the data
data = [feature["properties"] for feature in data["features"]]

# Create a DataFrame
df = pd.DataFrame(data)

# Write the data to a CSV file
df.to_csv("./data/unitati_relief.csv", index=False, encoding="utf-8")
