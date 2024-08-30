"""geocoding.py: Integration with the Geocoder API."""

import logging
from typing import Any

import geocoder
import questionary
import requests

from .google_maps import place_autocomplete

logger = logging.getLogger(__name__)


def extract_address_place_id(data: dict[str, Any]) -> list[tuple[str, str]]:
    """
    Extracts a list of tuples containing addresses and place IDs from the API response.

    Parameters
    ----------
    data : dict[str, Any]
        The response data from the Place Autocomplete API.

    Returns
    -------
    List[Tuple[str, str]]
        A list of tuples where each tuple contains the address and the corresponding place ID.
    """
    address_place_id_list: list[tuple[str, str]] = []

    if "suggestions" in data:
        for suggestion in data["suggestions"]:
            place_prediction = suggestion.get("placePrediction", {})
            place_id = place_prediction.get("placeId")
            text = place_prediction.get("text", {}).get("text")

            if place_id and text:
                address_place_id_list.append((text, place_id))

    return address_place_id_list


def get_latitude_longitude(api_key: str, location: str) -> tuple[float, float]:
    """
    Get the latitude and longitude of a location using the Place Autocomplete API.

    Parameters
    ----------
    api_key : str
        The API key for the Google Maps API.
    location : str
        The location to get the latitude and longitude for.

    Returns
    -------
    tuple[float, float]
        A tuple containing the latitude and longitude of the location.

    Notes
    -----
    Uses the Place Autocomplete API to get the latitude and longitude of a location.
    It asks the user to select the correct location if multiple results are found.
    """
    # Get predictions from the Place Autocomplete API
    result_dictionary = place_autocomplete(api_key, location)

    # Extract address and place ID from the predictions
    predictions_list = extract_address_place_id(result_dictionary)

    if not predictions_list:
        raise ValueError(f"No results found for {location}.")

    # Handle multiple results
    if len(predictions_list) > 1:
        addresses = [address for address, _ in predictions_list]
        selected_location = questionary.select(
            "Multiple results found. Please select the correct location:", choices=addresses
        ).ask()

        if selected_location is None:
            raise ValueError("No selection made.")

        # Find the corresponding place_id based on the selected address
        selected_location = predictions_list[addresses.index(selected_location)]
    else:
        selected_location = predictions_list[0]

    # Get latitude and longitude using the Place Details (New) API
    place_id = selected_location[1]  # Extract place ID
    details_url = (
        f"https://places.googleapis.com/v1/places/{place_id}?fields=location&key={api_key}"
    )

    response = requests.get(details_url)

    if response.status_code != 200:
        raise ValueError(f"Error fetching place details: {response.status_code}")

    details_data = response.json()
    if "location" not in details_data:
        raise ValueError(f"Error fetching place details: {details_data.get('status')}")

    # Extract latitude and longitude from the details response
    latitude = details_data["location"]["latitude"]
    longitude = details_data["location"]["longitude"]

    return latitude, longitude


def get_current_location() -> tuple[float, float]:  # TODO: Improve this function's accuracy
    """
    Get the current geographical location of the user based on their IP address.

    Returns
    -------
    tuple[float, float]
        A tuple containing the latitude and longitude of the current location.
        If the location cannot be determined, returns (None, None).

    Raises
    ------
    ValueError
        If the location cannot be determined.

    Examples
    --------
    >>> lat, lon = get_current_location()
    >>> print(lat, lon)
    (37.7749, -122.4194)
    """
    g = geocoder.ip("me")
    if g.ok:
        return tuple(g.latlng)
    else:
        raise ValueError("Unable to determine current location.")
