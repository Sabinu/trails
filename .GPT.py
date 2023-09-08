import json

import drawsvg as draw

m = lambda i: int(i // 100)
cx = lambda x: m(x - 120000)
cy = lambda y: m(y - 200000)

trans = lambda c: (cx(c[0]), cy(c[1]))


def coordinates_to_svg_path(coordinates):
    x, y = trans(coordinates[0])
    path = f"M {x} {y} "

    for coord in coordinates[1:]:
        x, y = trans(coord)
        path += f"L {x} {y} "

    return path


with open("./data/unitati_relief.geojson") as f:
    geojson = json.load(f)

d = draw.Drawing(8000, 5000, origin="center")

for feat in geojson["features"]:
    coord = feat["geometry"]["coordinates"][0]

    d.append(
        draw.Path(
            coordinates_to_svg_path(coord[0]),
            close=True,
            fill="lightblue",
            stroke="black",
        )
    )

d.save_svg("./data/unitati_relief.svg")
