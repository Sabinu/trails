import json

import geojson
import pandas as pd
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from icecream import ic


async def fetch_data(session, link):
    async with session.get(link) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), "html.parser")
            trail_id = link.split("/")[-1]

            return {"link": link, "id": trail_id, **parse_soup(soup)}
        else:
            print(f"Error: Failed to retrieve data from {link}")
            return None


async def fetch_trail(session, link):
    async with session.get(link) as response:
        if response.status == 200:
            trail = json.loads(await response.text())[0]
            trail = [[x, y] for (y, x) in trail]
            return {"trail": trail}
        else:
            print(f"Error: Failed to retrieve data from {link}")
            return None


async def scrape_batch(batch_links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, link[0]) for link in batch_links]
        props = await asyncio.gather(*tasks)

        tasks = [fetch_trail(session, link[1]) for link in batch_links]
        trails = await asyncio.gather(*tasks)

        results = zip(props, trails)

        return [{**r[0], **r[1]} for r in results if r is not None]


def parse_soup(soup):
    title = soup.title.string.strip()

    header = soup.find("h1", class_="page-header")
    header_text = header.text.strip() if header else None
    header_img = header.img["src"].strip() if header and header.img else None

    subheader_div = soup.find("div", class_="outer-title-route-info")
    subheader_text = subheader_div.text.strip() if subheader_div else None

    description_div = soup.find("div", class_="pane-node-field-leadin")
    description_text = description_div.text.strip() if description_div else None

    facts_div = soup.find("div", class_="view-mode-facts")
    facts_dict = {}

    if facts_div:
        group_divs = list(facts_div.find_all("div", class_="field-group-html-element"))

        for div in group_divs:
            field_item = div.find("div", class_="field-item")

            if field_item:
                key = [c for c in div.get("class") if c.startswith("group-")]
                key = key[0].replace("group-", "")

                value = field_item.text.strip()
                facts_dict[key] = value

    return {
        "title": title,
        "header": header_text,
        "header_image": header_img,
        "subheader": subheader_text,
        "description": description_text,
        **facts_dict,
    }


def list_to_geojson(lst):
    features = []
    for item in lst:
        geometry = geojson.LineString(item["trail"])

        properties = item
        del properties["trail"]

        feature = geojson.Feature(geometry=geometry, properties=properties)
        features.append(feature)

    return geojson.FeatureCollection(features)


async def main(batch_size):
    df = pd.read_csv("mn_links_02.csv")

    # links = list(enumerate(zip(df["link"][:10].tolist(), df["trail"])))
    links = list(enumerate(zip(df["link"].tolist(), df["trail"].tolist())))
    results = []

    while links:
        ic(links[:batch_size])
        batch = [l[1] for l in links[:batch_size]]
        links = links[batch_size:]
        batch_results = await scrape_batch(batch)
        results.extend(batch_results)

    results_df = pd.DataFrame(results)
    results_df = results_df.drop("trail", axis=1)
    results_df.to_csv("mn_details.csv", index=False)

    with open("mn_details.geojson", "w", encoding="utf-8") as fh:
        results = list_to_geojson(results)

        geojson.dump(results, fh, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main(batch_size=5))
