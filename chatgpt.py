import pandas as pd
import requests

from bs4 import BeautifulSoup
from icecream import ic

df = pd.read_csv("mm_links.csv")

results_df = pd.DataFrame()


def parse_soup(soup):
    title = soup.title.string.strip()
    shortlink = soup.find("link", rel="shortlink")["href"].strip()

    header = soup.find("h1", class_="page-header")
    header_text = header.text.strip() if header else None
    header_img = header.img["src"].strip() if header and header.img else None

    subheader_div = soup.find("div", class_="outer-title-route-info")
    subheader_text = subheader_div.text.strip() if subheader_div else None

    description_div = soup.find("div", class_="pane-node-field-leadin")
    description_text = description_div.text.strip() if description_div else None

    facts_div = soup.find("div", class_="view-mode-facts")
    if facts_div:
        group_divs = list(facts_div.find_all("div", class_="field-group-html-element"))
        facts_dict = {}

        for div in group_divs:
            field_item = div.find("div", class_="field-item")

            if field_item:
                key = [c for c in div.get("class") if c.startswith("group-")]
                key = key[0].replace("group-", "")

                value = field_item.text.strip()
                facts_dict[key] = value
    else:
        facts_dict = None

    return {
        "title": title,
        "short": shortlink,
        "header": header_text,
        "header_image": header_img,
        "subheader": subheader_text,
        "description": description_text,
        **facts_dict,
    }


for link in df["link"][:10]:
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        result = {
            "link": link,
            **parse_soup(soup),
        }

        results_df = pd.concat([results_df, pd.DataFrame([result])])

    else:
        print(f"Error: Failed to retrieve data from {link}")

results_df.to_csv("mm_details.csv", index=False)
