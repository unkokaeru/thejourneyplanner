"""polyline_interaction.py: Contains functions for interacting with polylines."""

import os

import folium
import polyline

from ..config.constants import Constants
from . import logger


def plot_polyline(encoded_polyline: str, save_path: str = Constants.DEFAULT_SAVE_DIRECTORY) -> str:
    """
    Plot the given encoded polyline on a map.

    Parameters
    ----------
    encoded_polyline : str
        The encoded polyline to be plotted.
    save_path : str, optional
        The path to save the map, by default Constants.DEFAULT_MAP_SAVE_PATH

    Raises
    ------
    PermissionError
        If the save path is invalid.

    Returns
    -------
    str
        The path to the saved map.
    """
    logger.info("Plotting the polyline on a map")

    if not save_path:  # If the save path is empty
        save_path = Constants.DEFAULT_SAVE_DIRECTORY

    # Create the save path if it does not exist
    if os.path.exists(save_path):
        logger.debug(f"Save path '{save_path}' exists.")
    else:
        logger.debug(f"Save path '{save_path}' does not exist.")
        os.makedirs(save_path)
        logger.debug(f"Save path '{save_path}' created.")

    decoded_polyline = polyline.decode(encoded_polyline)

    map_center = (decoded_polyline[0][0], decoded_polyline[0][1])
    folium_map = folium.Map(location=map_center, zoom_start=15)

    folium.PolyLine(decoded_polyline).add_to(folium_map)

    try:
        map_location = save_path + "map.html"
        folium_map.save(map_location)
        return map_location
    except PermissionError:
        logger.fatal("Permission denied. Please provide a valid path.")
        raise PermissionError("Permission denied. Please provide a valid path.")
