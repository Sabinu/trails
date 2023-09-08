from bs4 import BeautifulSoup
import pandas as pd


def tcx_to_csv(trail_id):
    tcx_file = f"./activities/{trail_id}.tcx"
    csv_file = f"./activities/{trail_id}.csv"

    with open(tcx_file, "r") as f:
        soup = BeautifulSoup(f, "xml")
    data = []
    for trackpoint in soup.find_all("Trackpoint"):
        time = trackpoint.find("Time").text
        latitude = trackpoint.find("LatitudeDegrees").text
        longitude = trackpoint.find("LongitudeDegrees").text
        altitude = trackpoint.find("AltitudeMeters").text
        distance = trackpoint.find("DistanceMeters").text
        heart_rate = trackpoint.find("HeartRateBpm").Value.text
        data.append(
            [
                trail_id,
                time,
                latitude,
                longitude,
                altitude,
                distance,
                heart_rate,
            ]
        )
    df = pd.DataFrame(
        data,
        columns=[
            "TrailId",
            "Time",
            "Latitude",
            "Longitude",
            "Altitude",
            "Distance",
            "HeartRate",
        ],
    )
    df.to_csv(csv_file, index=False)


tcx_to_csv(8836580877)
tcx_to_csv(8848902623)
tcx_to_csv(8866824156)
tcx_to_csv(8878277312)
tcx_to_csv(8884576484)

# cd strava
# poetry run python ./tcx_to_csv.py
