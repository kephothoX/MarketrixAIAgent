import os, requests


def brandInsights(location: str) -> dict:
    """
    Retrieves brand insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve brand insights.
        signal_interest_tags (str): Tags related to the signal interests.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:brand&filter.location.query={ location }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def destinationInsights(location: str) -> dict:
    """
    Retrieves destination insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve destination insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:destination&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def placeInsights(location: str) -> dict:
    """
    Retrieves place insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve place insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:place&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def movieInsights(location: str) -> dict:
    """
    Retrieves movie insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve movie insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:movie&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def bookInsights(location: str) -> dict:
    """
    Retrieves book insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve book insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:book&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def personInsights(location: str) -> dict:
    """
    Retrieves person insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve person insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:person&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def tvShowsInsights(location: str) -> dict:
    """
    Retrieves TV show insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve TV Shows insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:tv_show&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def artistInsights(location: str) -> dict:
    """
    Retrieves Artists insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve Artists insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:artist&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def podcastInsights(location: str) -> dict:
    """
    Retrieves Podcasts insights from Qloo API for a given location.

    Args:
        location (str): Location for which to retrieve Podcasts insights.

    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights/?filter.type=urn:entity:podcast&signal.location.query={ location}"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}


def demographicInsights(entity_id: str) -> dict:
    """
    Retrieves demographic insights for a given entity from Qloo API.

    Args:
        entity_id (str): The ID of the entity for which to retrieve demographic insights.
    Returns:
        dict: A dictionary containing the insight results.
    """
    url = f"{ os.environ.get('QLOO_ENDPOINT_URL')}/v2/insights?filter.type=urn:demographics&signal.interests.entities={ entity_id }"

    headers = {
        "accept": "application/json",
        "X-Api-Key": f"{os.environ.get('QLOO_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
