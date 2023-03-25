import os

from dotenv import load_dotenv
import requests

load_dotenv()

BING_MAPS_KEY = os.getenv("BING_MAPS_KEY")
print(BING_MAPS_KEY)
ELEVATION_URL = f"http://dev.virtualearth.net/REST/v1/Elevation/List?points={{lat1}},{{long1}},{{lat2}},{{long2}}&key={BING_MAPS_KEY}"

response = requests.get(ELEVATION_URL)
data = response.json()

print(data)
