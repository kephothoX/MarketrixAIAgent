import os
import requests


def getTrendingData(entity_id: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves trending data over a defined period of time of a given entity.

    Args:
        entity_id (str): The entity to research.
        start_date (str): The start date for the trending data in YYYY-MM-DD format.
        end_date (str): The end date for the trending data in YYYY-MM-DD format.
    Returns:
        dict: A dictionary containing the comparison results.

    """

    #  \
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/trends/entity?entity_id={ entity_id }&start_date={ start_date }&end_date={ end_date }&page=1&take=20"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
