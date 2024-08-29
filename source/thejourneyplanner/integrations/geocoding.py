"""geocoding.py: Integration with the Geocoder API."""

import geocoder


def get_current_location() -> tuple[float, float]:
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
