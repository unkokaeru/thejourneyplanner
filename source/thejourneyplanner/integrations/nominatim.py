"""nominatim.py: Functions for interacting with the Nominatim API."""

import logging

import requests

from ..config.constants import Constants

logger = logging.getLogger(__name__)


def find_longitude_and_latitude(
    location: str,
) -> tuple[float, float]:  # TODO: Use this function for the initial location finding
    """
    Find the longitude and latitude of a location using the Nominatim API.

    Parameters
    ----------
    location : str
        The location to find the longitude and latitude of.

    Returns
    -------
    tuple[float, float]
        A tuple containing the longitude and latitude of the location.

    Raises
    ------
    ValueError
        If the location is not found or if an HTTP error occurs.

    Examples
    --------
    >>> find_longitude_and_latitude("New York")
    (40.7128, -74.0060)

    >>> find_longitude_and_latitude("Los Angeles")
    (34.0522, -118.2437)

    Notes
    -----
    This function finds the longitude and latitude of a given location.
    It takes in the location as a string and returns a tuple containing
    the longitude and latitude of the location.
    It uses the Nominatim API to find the location. If the location is
    not found, it raises aValueError.
    """
    # Construct the Nominatim API URL
    url = Constants.NOMINATIM_URL
    params: dict[str, str | int] = {
        "q": location,
        "format": "json",
        "limit": 1,
    }  # Limit to one result

    logger.debug(f"Requesting location data for: {location}")

    headers = {"User-Agent": Constants.NOMINATIM_USER_AGENT}  # Set a user agent to avoid 429 errors

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        location_data = response.json()

        logger.debug(f"Location data: {location_data}")

        if location_data:
            latitude = float(location_data[0]["lat"])
            longitude = float(location_data[0]["lon"])

            logger.debug(f"Latitude: {latitude}, Longitude: {longitude}")

            return latitude, longitude
        else:
            logger.fatal(f"Location not found: {location}")
            raise ValueError("Location not found.")
    except requests.exceptions.HTTPError as e:
        logger.fatal(f"HTTP error occurred: {e}")
        raise ValueError(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.fatal(f"An error occurred: {e}")
        raise ValueError(f"An error occurred: {e}")
