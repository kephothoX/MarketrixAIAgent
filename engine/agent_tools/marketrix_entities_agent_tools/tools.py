__all__ = [
    "entitiesFilterTypes",
    "getEntitiesByName",
    "getEntitiesByID",
    "getEntitiesID",
]

import os
import requests


def entitiesFilterTypes(entity_type: str) -> dict:

    return {
        "entity_filter_types": [
            "urn:entity:artist",
            "urn:entity:book",
            "urn:entity:brand",
            "urn:entity:destination",
            "urn:entity:movie",
            "urn:entity:person",
            "urn:entity:place",
            "urn:entity:podcast",
            "urn:entity:tv_show",
            "urn:entity:video_game",
        ]
    }


def getEntitiesByName(name: str) -> dict:
    """
    Searches for entities by name.

    Args:
        name (str): The name of the entity to search for.

    Returns:
        dict: A dictionary containing the search results.
    """
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query={name}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def getEntitiesByID(entity_id: str) -> dict:
    """
    Searches for entities by entity id.

    Args:
        entity_id (str): The id of the entity to search for.

    Returns:
        dict: A dictionary containing the search results.
    """
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query={entity_id}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def getEntitiesID(name: str) -> dict:
    """
    Searches for entities for their entity id.

    Args:
        name (str): The name of the entity to search for.

    Returns:
        dict: A dictionary containing the search results.
    """
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/search?query={name}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        EntityIDs = list()

        for entity in data["results"]:
            EntityIDs.append(entity["entity_id"])

        return {"entity_ids": EntityIDs}

    else:
        return {"error": "Failed to fetch data"}
