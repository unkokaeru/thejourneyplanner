"""google_maps.py: Integration with the Google Maps API."""

import json
from typing import Any, List, Literal, Tuple

import requests

from ..config.constants import Constants
from . import logger


def get_distance_matrix(
    api_key: str,
    start_location: str,
    end_location: str,
    units: Literal["metric", "imperial"] = "metric",
) -> dict[str, Any]:
    """
    Retrieve the distance/duration between two locations using the Google Maps Distance Matrix API.

    Parameters
    ----------
    api_key : str
        The API key for authenticating requests to the Google Maps API.
    start_location : str
        The starting location for the distance matrix request.
    end_location : str
        The ending location for the distance matrix request.
    units : Literal['metric', 'imperial'], optional
        The units to use for the distance and duration values, by default 'metric'.

    Returns
    -------
    dict of str to str or int
        A dictionary containing the distance and duration between the two locations.

    Raises
    ------
    ValueError
        If the API request fails or if the locations are not found.

    Example
    -------
    >>> api_key = 'your_api_key_here'
    >>> start_location = 'London'
    >>> end_location = 'Bury St Edmunds'
    >>> get_distance_matrix(api_key, start_location, end_location)
    {
        'start_location': 'London, UK',
        'end_location': 'Bury St Edmunds, Bury Saint Edmunds, UK',
        'distance_text': '133 km',
        'distance_value': 133313,
        'duration_text': '1 hour 47 mins',
        'duration_value': 6398
    }
    """
    url: str = (
        f"{Constants.DISTANCE_MATRIX_URL}?"
        f"destinations={end_location}&origins={start_location}&units={units}&key={api_key}"
    )

    logger.debug(f"Requesting distance matrix with URL: {url}")

    response = requests.get(url)
    if response.status_code != Constants.SUCCESS_CODE:
        logger.fatal(f"API request failed with status code {response.status_code}")
        raise ValueError(f"API request failed with status code {response.status_code}")

    data = response.json()

    logger.debug(f"Distance matrix response: {data}")

    if data["status"] != Constants.SUCCESS_TEXT:
        logger.fatal(
            f"API response status is not OK: {data['status']} ({data.get('error_message')})"
        )
        raise ValueError(
            f"API response status is not OK: {data['status']} ({data.get('error_message')})"
        )

    origin_addresses = data["origin_addresses"]
    destination_addresses = data["destination_addresses"]
    elements = data["rows"][0]["elements"][0]

    if elements["status"] != Constants.SUCCESS_TEXT:
        logger.fatal(f"Element status is not OK: {elements['status']}")
        raise ValueError(f"Element status is not OK: {elements['status']}")

    result = {
        "start_location": origin_addresses[0],
        "end_location": destination_addresses[0],
        "distance_text": elements["distance"]["text"],
        "distance_value": elements["distance"]["value"],
        "duration_text": elements["duration"]["text"],
        "duration_value": elements["duration"]["value"],
    }

    logger.debug(f"Distance matrix result: {result}")

    return result


def search_nearby_places(
    api_key: str,
    latlong: Tuple[float, float],
    radius: float,
    types_list: List[str] = Constants.NEARBY_SEARCH_TYPES,
) -> List[dict[str, Any]]:
    """
    Search for nearby places using the Google Places API.

    Parameters
    ----------
    api_key : str
        The API key for authenticating requests to the Google Maps API.
    latlong : tuple of float
        The latitude and longitude of the search location.
    radius : float
        The radius of the search area in meters.
    types_list : list of str, optional
        A list of place types to include in the search. Default is Constants.NEARBY_SEARCH_TYPES.

    Returns
    -------
    list of dict of str to Any
        A list of dictionaries containing information about the nearby places.

    Raises
    ------
    ValueError
        If the API request fails or if the response contains an error.

    Example
    -------
    >>> api_key = 'your_api_key_here'
    >>> latitude = 52.2635809
    >>> longitude = 0.6916481
    >>> radius = 10000
    >>> search_nearby_places(api_key, (latitude, longitude), radius)
    [
        {
            'formatted_address': 'West Midland Safari and Leisure Park, Bewdley DY12 1LF, UK',
            'rating': 4.5,
            'user_rating_count': 2,
            'display_name': 'Twilight Cave'
        },
        ...
    ]
    """
    url = Constants.NEARBY_SEARCH_URL
    field_mask = Constants.NEARBY_SEARCH_FIELD_MASK
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": field_mask,
    }
    payload = {
        "locationRestriction": {
            "circle": {
                "center": {"latitude": latlong[0], "longitude": latlong[1]},
                "radius": radius,
            }
        },
        "rankPreference": Constants.NEARBY_SEARCH_RANK_BY,
        "includedTypes": types_list,
        "maxResultCount": Constants.MAX_NEARBY_PLACES,
    }

    logger.debug(
        f"Searching nearby places with...\n"
        f"url: {url},\n"
        f"headers: {headers},\n"
        f"payload: {json.dumps(payload)}"
    )

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    logger.debug(f"Nearby places raw response: {response.text}")
    if response.status_code != Constants.SUCCESS_CODE:
        logger.fatal(f"API request failed with status code {response.status_code}")
        raise ValueError(f"API request failed with status code {response.status_code}")

    data = response.json()

    if "places" not in data:
        logger.fatal(f"API response error: {data}")
        raise ValueError(f"API response error: {data}")

    logger.debug(f"Nearby places response: {data}")

    places = []
    for place in data["places"]:
        place_info = {
            "formatted_address": place.get("formattedAddress"),
            "latlong": (place["location"]["latitude"], place["location"]["longitude"]),
            "rating": place.get("rating"),
            "user_rating_count": place.get("userRatingCount"),
            "display_name": (place["displayName"]["text"] if "displayName" in place else None),
        }
        places.append(place_info)

    logger.debug(f"Nearby places: {places}")

    return places


def compute_route(
    api_key: str,
    origin_latlong: Tuple[float, float],
    destination_latlong: Tuple[float, float],
    intermediate_latlongs: List[Tuple[float, float]] = [],
    travel_mode: str = "DRIVE",  # TODO: Add support for other travel modes
    routing_preference: str = "TRAFFIC_AWARE",  # TODO: Add support for other routing preferences
    compute_alternative_routes: bool = False,
    avoid_tolls: bool = False,
    avoid_highways: bool = False,  # TODO: Add support for other route modifiers
    avoid_ferries: bool = False,
    units: Literal["IMPERIAL", "METRIC"] = "METRIC",  # TODO: Add support for other units
) -> dict[str, Any]:
    """
    Compute a route between two locations using the Google Routes API.

    Parameters
    ----------
    api_key : str
        The API key for authenticating requests to the Google Maps API.
    origin_latlong : tuple of float
        The latitude and longitude of the origin location.
    destination_latlong : tuple of float
        The latitude and longitude of the destination location.
    intermediate_latlongs : list of tuple of float, optional
        A list of intermediate locations to visit along the route. Default is [].
    travel_mode : str, optional
        Mode of travel (e.g., 'DRIVE', 'WALK'). Default is 'DRIVE'.
    routing_preference : str, optional
        Routing preference (e.g., 'TRAFFIC_AWARE'). Default is 'TRAFFIC_AWARE'.
    compute_alternative_routes : bool, optional
        Whether to compute alternative routes. Default is False.
    avoid_tolls : bool, optional
        Whether to avoid tolls. Default is False.
    avoid_highways : bool, optional
        Whether to avoid highways. Default is False.
    avoid_ferries : bool, optional
        Whether to avoid ferries. Default is False.
    units : Literal['IMPERIAL', 'METRIC'], optional
        Units for the response. Default is 'METRIC'.

    Returns
    -------
    dict of str to int or str
        A dictionary containing the route distance, duration, and encoded polyline.

    Raises
    ------
    ValueError
        If the API request fails or if the response contains an error.

    Example
    -------
    >>> api_key = 'your_api_key_here'
    >>> origin_lat = 37.419734
    >>> origin_lng = -122.0827784
    >>> destination_lat = 37.417670
    >>> destination_lng = -122.079595
    >>> compute_route(api_key, (origin_lat, origin_lng), (destination_lat, destination_lng))
    {
        'distance_meters': 772,
        'duration_seconds': 165,
        'encoded_polyline': 'ipkcFfichVnP@j@BLoFVwM{E?'
    }
    """
    url = f"{Constants.COMPUTE_ROUTES_URL}?key={api_key}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": Constants.COMPUTE_ROUTES_FIELD_MASK,
    }
    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_latlong[0],
                    "longitude": origin_latlong[1],
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_latlong[0],
                    "longitude": destination_latlong[1],
                }
            }
        },
        "intermediates": (
            [
                {"location": {"latLng": {"latitude": latlong[0], "longitude": latlong[1]}}}
                for latlong in intermediate_latlongs
            ]
            if intermediate_latlongs != []
            else []
        ),
        "travelMode": travel_mode,
        "routingPreference": routing_preference,
        "computeAlternativeRoutes": compute_alternative_routes,
        "routeModifiers": {
            "avoidTolls": avoid_tolls,
            "avoidHighways": avoid_highways,
            "avoidFerries": avoid_ferries,
        },
        "languageCode": Constants.LANGUAGE_CODE,  # TODO: Add support for other languages
        "units": units,
    }

    logger.debug(f"Computing route with payload: {payload}")

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != Constants.SUCCESS_CODE:
        if response.status_code == Constants.FORBIDDEN_CODE:
            logger.fatal(
                f"API request failed with status code {Constants.FORBIDDEN_CODE}: Forbidden. "
                f"This could be due to an invalid API key, lack of permissions, "
                f"or exceeding the quota."
            )
            raise ValueError(
                f"API request failed with status code {Constants.FORBIDDEN_CODE}: Forbidden. "
                f"This could be due to an invalid API key, lack of permissions, "
                f"or exceeding the quota."
            )
        else:
            logger.fatal(
                f"API request failed with status code {response.status_code}: {response.text}"
            )
            raise ValueError(
                f"API request failed with status code {response.status_code}: {response.text}"
            )

    data = response.json()

    if "routes" not in data or not data["routes"]:
        logger.fatal(f"API response error: {data}")
        raise ValueError(f"API response error: {data}")

    logger.debug(f"Route response: {data}")

    route: dict = data["routes"][0]
    route_info = {
        "distance_meters": route.get("distanceMeters"),
        "duration_seconds": int(route.get("duration", "0").replace("s", "")),
        "encoded_polyline": route.get("polyline", {}).get("encodedPolyline"),
    }

    logger.debug(f"Route info: {route_info}")

    return route_info
