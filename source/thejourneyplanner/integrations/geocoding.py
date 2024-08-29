"""geocoding.py: Integration with the Geocoder API."""

import geocoder


def forward_geocode(location: str) -> tuple[float, float]:
    """
    Get the geographical coordinates (latitude and longitude) for a given address or location.

    Parameters
    ----------
    location : str
        The address or location to be geocoded.

    Returns
    -------
    tuple[float, float]
        A tuple containing the latitude and longitude of the specified location.
        If the location cannot be determined, returns (None, None).

    Raises
    ------
    ValueError
        If the location cannot be determined.

    Examples
    --------
    >>> lat, lon = forward_geocode("London, UK")
    >>> print(lat, lon)
    (51.5074456, -0.1277653)
    """
    g = geocoder.osm(location)
    if g.ok:
        return tuple(g.latlng)
    else:
        raise ValueError("Unable to geocode the specified location.")


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
