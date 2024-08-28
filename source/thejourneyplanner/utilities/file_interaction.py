"""file_interaction.py: Functions for interacting with files."""

import logging
import os
import shutil
import webbrowser
from pathlib import Path

from ..config.constants import Constants

logger = logging.getLogger(__name__)


def duplicate_last_log(
    save_path: Path = Constants.DEFAULT_LOG_SAVE_PATH,
) -> None:  # TODO: Redo this function, it's so janky
    """
    Duplicate the most recently modified log file to the output directory.

    Parameters
    ----------
    output_path : Path, optional
        The path to the output directory, by default Constants.DEFAULT_LOG_SAVE_PATH

    Raises
    ------
    FileNotFoundError
        If no files are found in the source directory.
    """
    # Get a list of files in the source directory
    try:
        files = os.listdir(Constants.ARCHIVED_LOGS_DIRECTORY)
    except FileNotFoundError:
        print(f"Source directory '{Constants.ARCHIVED_LOGS_DIRECTORY}' not found.")
        return

    # Filter out files to ensure we only consider files (not directories)
    files = [f for f in files if os.path.isfile(os.path.join(Constants.ARCHIVED_LOGS_DIRECTORY, f))]

    if not files:
        raise FileNotFoundError(
            f"No files found in source directory '{Constants.ARCHIVED_LOGS_DIRECTORY}'."
        )

    # Get the most recently modified file
    latest_file = max(
        files,
        key=lambda f: os.path.getmtime(os.path.join(Constants.ARCHIVED_LOGS_DIRECTORY, f)),
    )

    # Construct full file path
    source_file_path = Constants.ARCHIVED_LOGS_DIRECTORY / latest_file

    # Copy the latest log file to the output directory and rename it
    try:
        shutil.copy2(source_file_path, save_path)
        print(f"Copied '{latest_file}' to '{save_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return


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
