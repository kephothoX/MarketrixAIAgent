import os, requests, base64, io
from io import BytesIO
from google.genai import types

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

MODEL = "gemini-2.0-flash"


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


def getAgeDemographicsHeatmaps(location: str, age_demographics: str) -> dict:
    """
    Retrieves heatmap  age demographics insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        age_demographics (str): Age demographics to filter the insights.

    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&signal.demographics.age={ age_demographics }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def getEntitiesInterestsHeatmaps(location: str, entities_interests: str) -> dict:
    """
    Retrieves heatmap data about entities interests insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        entities_interests (str): Entities interests to filter the insights.


    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&signal.interests.entities={ entities_interests }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def getGenderDemographicsHeatmaps(location: str, gender_demographics: str) -> dict:
    """
    Retrieves heatmap  age demographics insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        gender_demographics (str): Gender demographics to filter the insights.


    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&signal.demographics.gender={ gender_demographics }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def getInterestsTagsHeatmaps(location: str, interest_tags: str) -> dict:
    """
    Retrieves heatmap data about various interest tags insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        interest_tags (str): Interest tags to filter the insights.

    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&signal.interests.tags={ interest_tags }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def getBiasTrendsHeatmaps(location: str, bias_trends: str) -> dict:
    """
    Retrieves heatmap data about various bias trends insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        bias_trends (str): Bias trends to filter the insights.

    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&bias.trends={ bias_trends }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def getBrandsHeatmapsData(location: str, name: str) -> dict:
    """
    Retrieves heatmap data about various brands insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        name (str): Name of the brand to filter the insights.

    Returns:
        dict: A dictionary containing the insight results.
    """

    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:heatmap&filter.location.query={ location}&signal.interests.entities={ getEntitiesID(name)}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"result": response.json()["results"]["heatmap"]}
    else:
        return {"error": "Failed to fetch data"}


def drawHeatMapImage(data: list, name: str) -> dict:
    """
    Draws a heatmap based on the provided parameters.

    Args:
        data (list): The dataset to be used for the heatmap.
        name (str): The name of the heatmap to be drawn.


    Returns:
        dict: A heatmap drawing with latitude, longitude, geohash, affinity, and affinity_score.
    """

    dataset = pd.json_normalize(data)
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

    heatmap = sns.kdeplot(
        df,
        x="longitude",
        y="latitude",
        fill=True,
        cmap="coolwarm",
        alpha=0.3,
        gridsize=200,
        levels=20,
    )

    heatmap.set_title(name)
    heatmap.set_xlabel("Longitude")
    heatmap.set_ylabel("Latitude")
    heatmap.figure.add_axes(heatmap)
    heatmap.figure.savefig(f"{ name }.png")

    buf = BytesIO()
    heatmap.figure.savefig(buf, format="png")
    buf.seek(0)
    buf.close()

    # Draw the canvas and save as PNG into the buffer
    canvas = FigureCanvas(heatmap.figure)

    return {
        "result": types.Content(
            parts=[
                types.Part.from_bytes(
                    data=canvas.print_to_buffer(), mimeType="image/png"
                )
            ]
        ),
        "image": canvas.print_to_buffer(),
    }
