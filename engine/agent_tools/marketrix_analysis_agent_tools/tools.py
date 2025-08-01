import os
import requests


def marketAnalysis(entity_ids: list) -> dict:
    """
    Retrieves  and analyses data based on entities ids.

    Args:
        entity_ids (list): List of entities to analyze.

    Returns:
        dict: A dictionary containing results of analysis.

    """

    #  \
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/analysis?entity_ids={ entity_ids }&page=1&take=20"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
