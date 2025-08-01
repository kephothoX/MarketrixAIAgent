import os
import requests


def compareAndAnalyseBrands(entity_a: str, entity_b: str) -> dict:
    """
    Compares two entities and analyses their differences.

    Args:
        entity_a (str): The first entity to compare.
        entity_b (str): The second entity to compare.

    Returns:
        dict: A dictionary containing the comparison results.

    """

    #  \
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/compare?a.signal.interests.entities={ entity_a}&b.signal.interests.entities={ entity_b}&page=1&take=20"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
