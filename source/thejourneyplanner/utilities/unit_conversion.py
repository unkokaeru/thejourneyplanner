"""unit_conversion.py: Functions for unit conversion."""

import logging

logger = logging.getLogger(__name__)


def convert_distance(distance: float, units: str) -> str:
    """
    Convert distance to the most appropriate units for readability.

    Parameters
    ----------
    distance : float
        The distance to be converted.
    units : str
        The units of the given distance.

    Returns
    -------
    str
        The distance in the most appropriate units.
    """
    if units == "meters":
        if distance < 1000:
            return f"{distance:.0f} meters"
        else:
            return f"{distance / 1000:.1f} kilometers"
    elif units == "kilometers":
        return f"{distance:.1f} kilometers"
    else:
        logger.error(f"Invalid units: {units}")
        return "Invalid units"  # TODO: Implement more distance unit options, such as miles


def convert_duration(duration: int, units: str) -> str:
    """
    Convert duration to the most appropriate units for readability.

    Parameters
    ----------
    duration : int
        The duration to be converted.
    units : str
        The units of the given duration.

    Returns
    -------
    str
        The duration in the most appropriate units.
    """
    if units == "seconds":
        if duration < 60:
            return f"{duration:.0f} seconds"
        elif duration < 3600:
            return f"{duration // 60:.0f} minutes and {duration % 60:.0f} seconds"
        else:
            return f"{duration // 3600:.0f} hours and {duration % 3600 // 60:.0f} minutes"
    elif units == "minutes":
        if duration < 60:
            return f"{duration:.0f} minutes"
        else:
            return f"{duration // 60:.0f} hours and {duration % 60:.0f} minutes"
    else:
        logger.error(f"Invalid units: {units}")
        return "Invalid units"  # TODO: Implement more duration unit options, such as hours
