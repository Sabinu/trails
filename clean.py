import os
import re
import json

import requests
from icecream import ic

with open("mn_details.geojson", "r", encoding="utf-8") as fh:
    data = json.load(fh)

ic(len(data["features"]))

ic(data["features"][0]["properties"])


def clean(feat):
    del feat["geometry"]

    p = feat["properties"]

    p["title"] = p["title"].replace(" | Muntii Nostri", "")

    p["title"] = re.sub(r"\s+", " ", p["title"])
    p["header"] = re.sub(r"\s+", " ", p["header"])

    p["header"] = p["header"].replace(p["title"], "").replace(": ", "")

    p["trail_group"], p["trail_number"] = p["header"].split("MN")

    del p["header"]

    if "header_image" in p.keys():
        if p["header_image"]:
            p["header_image"] = p["header_image"].split("?")[0]
            p["header_image"] = (
                p["header_image"]
                .split("/")[-1]
                .replace(".png", "")
                .replace("9200_", "")
                .split("track")[0]
                .split("_")[-1]
            )
            p["header_image"] = re.sub(r"(red|blue|yellow)", r"\1_", p["header_image"])

            p["trail_color"], p["trail_type"] = p["header_image"].split("_")

        del p["header_image"]

    p["ascent"] = int(p["ascent"].replace("m", ""))
    p["descent"] = int(p["descent"].replace("m", ""))

    if "peak" in p.keys():
        p["peak"] = int(p["peak"].replace("m", ""))

    p["distance"] = float(p["distance"].replace("km", "").replace(",", "."))

    return feat


cleaned = [clean(feat) for feat in data["features"]]

with open("mn_details_clean.geojson", "w", encoding="utf-8") as fh:
    data["features"] = cleaned
    # json.dump(data, fh, ensure_ascii=False)
    json.dump(data, fh, ensure_ascii=False, indent=2)
