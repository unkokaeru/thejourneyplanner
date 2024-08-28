"""file_interaction.py: Functions for interacting with files."""

import logging
import webbrowser
from pathlib import Path

logger = logging.getLogger(__name__)


def open_html_file(file_path: Path) -> None:
    """
    Open the specified HTML file in the default web browser.

    Parameters
    ----------
    file_path : Path
        The path to the HTML file to open.
    """
    logger.debug(f"Opening HTML file '{file_path}' in the default web browser.")
    absolute_path = file_path.resolve()
    file_url = f"file:///{absolute_path.as_posix()}"

    webbrowser.open(file_url, new=2)
    logger.info(
        f"Opened map with plotted polyline in the default web browser.\n"
        f"If the map does not open, please navigate to '{file_url}' manually."
    )
