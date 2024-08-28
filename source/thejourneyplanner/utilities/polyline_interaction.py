"""polyline_interaction.py: Contains functions for interacting with polylines."""

import logging
import os
from pathlib import Path

import folium
import polyline

from ..config.constants import Constants
from .file_interaction import open_html_file

logger = logging.getLogger(__name__)


def plot_polyline(
    encoded_polyline: str,
    save_path: Path = Constants.DEFAULT_MAP_SAVE_PATH,
    open_map: bool = Constants.DEFAULT_OPEN_MAP,
) -> Path:
    """
    Plot the given encoded polyline on a map.

    Parameters
    ----------
    encoded_polyline : str
        The encoded polyline to be plotted.
    save_path : Path, optional
        The path to save the map, by default Constants.DEFAULT_MAP_SAVE_PATH
    open_map : bool, optional
        Whether to open the map in the default web browser, by default False

    Raises
    ------
    PermissionError
        If the save path is invalid.

    Returns
    -------
    Path
        The path to the saved map.
    """
    logger.info("Plotting the polyline on a map")

    decoded_polyline = polyline.decode(encoded_polyline)

    map_center = (decoded_polyline[0][0], decoded_polyline[0][1])
    folium_map = folium.Map(location=map_center, zoom_start=15)

    folium.PolyLine(decoded_polyline).add_to(folium_map)

    try:
        map_location = save_path
        os.makedirs(map_location.parent, exist_ok=True)
        folium_map.save(map_location)

        if open_map:
            open_html_file(map_location)

        return map_location
    except PermissionError:
        logger.fatal("Permission denied. Please provide a valid path.")
        raise PermissionError("Permission denied. Please provide a valid path.")
