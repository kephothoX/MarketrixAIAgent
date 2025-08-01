import requests, os, json, base64, io
from io import BytesIO

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


from dotenv import load_dotenv

load_dotenv()

print(f"{os.environ.get('QLOO_ENDPOINT_URL')}")


def getEntitiesID(name: str) -> str:
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query={name}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        entities = str
        EntityIDs = list()

        for entity in data["results"]:
            EntityIDs.append(entity["entity_id"])

        entities = str(EntityIDs).replace("[", "").replace("]", "").replace("'", "")

        return entities

    else:
        return ""


def play():
    # print(f"Entity IDs:   {getEntitiesID('safaricom')['entity_ids']}")
    # url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query=kasuku"
    # url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/compare?a.signal.interests.entities=Google Cloud&b.signal.interests.entities=AWS&page=1&take=20"
    # url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/audiences?filter.parents.types=urn:audience:global_issues,urn:audience:communities,urn:audience:investing_interests,urn:audience:leisure,urn:audience:spending_habits,urn:audience:professional_area,urn:audience:political_preferences,urn:audience:life_preferences_beliefs,urn:audience:life_stage,urn:audience:hobbies_and_interests"

    # /v2/audiences?filter.parents.types=urn%3Aaudience%3Aleisure

    # url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights?filter.type=urn:tag&signal.location.query=nairobi"
    # &filter.parents.types=urn:audience:investing_interests"
    # &filter.parents.types=urn:entity:book"

    # url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:brand&signal.location.query=nairobi"

    # filter.type.types=urn:tag:keyword:brand&

    # url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/tags/types"

    # /v2/insights?filter.type=urn:tag&filter.tag.types=urn:tag:keyword:brand"

    # &filter.parents.types=urn:audience:investing_interests"

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query=NYC&signal.interests.entities={ getEntitiesID('safaricom') }"

    # print(f"URL: {url}")
    # signal.interests.tags=urn:tag:genre:media:comedy"
    # urn:tag:genre:media:fiction,urn:tag:genre:media:comedy,urn:tag:genre:media:drama,urn:tag:genre:media:sports,urn:tag:genre:media:documentary&signal.interests.entities=Google Cloud,Amazon Web Services&signal.interests.types=urn:entity:type:brand"

    # url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query=AWS"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{ os.environ.get('QLOO_API_KEY') }",
    }

    response = requests.get(url, headers=headers)

    print(response)
    print(response.json())

    location = response.json()["results"]["heatmap"][0]
    query = response.json()["results"]["heatmap"][1]
    dataset = pd.json_normalize(response.json()["results"]["heatmap"])
    dataset = dataset.rename(
        columns={
            "location.latitude": "latitude",
            "location.longitude": "longitude",
            "query.affinity": "affinity_score",
            "query.affinity_rank": "affinity_rank",
            "query.popularity": "popularity_score",
        }
    )
    df = pd.DataFrame(dataset)
    a = df.pivot_table(
        index="latitude", columns="longitude", values="popularity_score", aggfunc="mean"
    )
    # dat = json.dumps(response.json()["results"]["heatmap"], indent=4)

    # for location, query in dat:
    #    print(f"Location: {location}, Query: {query}")

    # dict_data = json.loads(dat)
    # print(f"Dict data: {dict_data}")
    # df = pd.json_normalize(dict_data["location"], dict_data["query"])

    # df = pd.json_normalize(dat["location"], dict_data["query"])

    # print("Dataset: ", dataset)
    print(f"Dataset: {dataset}")
    print(f"Dataframe: {df}")
    print(f"A:     {a}")
    # print(f"DataFrame: {df['location']}")
    # print(f"DataFrame: {df['location']["latitude"]}")
    # print(f"DataFrame: {df['query']}")
    # dataset = {
    #    "latitude": response.json()["results"][0]["location"]["latitude"],
    #    "longitude": response.json()["results"][0]["location"]["longitude"],
    #    "affinity_rank": response.json()["results"][0]["query"]["affinity_rank"],

    # print(response.json())

    heat_map = sns.kdeplot(
        df,
        x="longitude",
        y="latitude",
        fill=True,
        cmap="coolwarm",
        alpha=0.3,
        gridsize=200,
        levels=20,
        # ax=ax
    )

    """[
            df["latitude"],
            df["longitude"],
            df["affinity_rank"],
            df["affinity_score"],
            df["popularity_score"],
        ],
    """
    """heat_map = sns.heatmap(        
        a,
        annot=True,
        fmt=".1f",
        cmap="viridis",
        vmin=-1,
        vmax=1,
        center=0,
    )
    """

    heat_map.set_title("Heatmap of Safaricom in NYC")
    # heat_map.set_xlabel("Longitude")
    # heat_map.set_ylabel("Latitude")
    heat_map.figure.savefig("heatmap_safaricom_nyc.png")
    heat_map.figure.show()

    buf = BytesIO()
    heat_map.figure.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    # Draw the canvas and save as PNG into the buffer
    canvas = FigureCanvas(heat_map.figure)
    canvas.print_png(buf)

    print(f"Canvas:  { canvas}")

    print(f"Encoded Image: { encoded_image}")
    return encoded_image


play()
