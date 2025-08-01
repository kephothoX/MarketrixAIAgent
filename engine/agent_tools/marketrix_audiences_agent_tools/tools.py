import os
import requests


def findAudiences(query: str) -> dict:
    """
    Retrieves  and analyses data based on entities ids.

    Args:
        query (str): The query to search for audiences.

    Returns:
        dict: A dictionary containing results of analysis.

    """

    #  \
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}//v2/audiences?filter.parents.types=urn:audience:global_issues,urn:audience:communities,urn:audience:investing_interests,urn:audience:leisure,urn:audience:spending_habits,urn:audience:professional_area,urn:audience:political_preferences,urn:audience:life_preferences_beliefs,urn:audience:life_stage,urn:audience:hobbies_and_interests"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
