import json

import drawsvg as draw

width = 8000
height = 6000

d = draw.Drawing(width, height, origin="center")

m = lambda i: int(i // 100)
cx = lambda x: m(x - 120000) - width / 2
cy = lambda y: -m(y - 200000) + height / 2

trans = lambda c: (cx(c[0]), cy(c[1]))


def remove_consecutive_duplicates(coordinates):
    if not coordinates:
        return []
    result = [coordinates[0]]
    for coord in coordinates[1:]:
        if coord != result[-1]:
            result.append(coord)
    return result


def coordinates_to_svg_path(coordinates):
    coordinates = remove_consecutive_duplicates([trans(c) for c in coordinates])

    x, y = coordinates[0]
    path = f"M {x} {y} "

    for coord in coordinates[1:]:
        x, y = coord
        path += f"L {x} {y} "

    return path


def get_center(coordinates):
    x_coords = [trans(coord)[0] for coord in coordinates]
    y_coords = [trans(coord)[1] for coord in coordinates]
    _len = len(coordinates)
    centroid_x = int(sum(x_coords) / _len)
    centroid_y = int(sum(y_coords) / _len)
    return (centroid_x, centroid_y)


with open("./data/unitati_relief.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)


for feat in geojson["features"]:
    i = feat["properties"]["ID"]
    name = feat["properties"]["DENUMIRE"]

    coord = feat["geometry"]["coordinates"][0]

    grp = draw.Group()

    grp.append(
        draw.Path(
            coordinates_to_svg_path(coord[0]),
            close=True,
            fill="lightblue",
            stroke="black",
        )
    )

    center_x, center_y = get_center(coord[0])
    grp.append(
        draw.Text(
            # f"{center_x}:{center_y}",
            f"{i}:{name}",
            20,
            center_x,
            center_y,
            center=True,
        )
    )

    d.append(grp)

d.save_svg("./data/unitati_relief.svg")
