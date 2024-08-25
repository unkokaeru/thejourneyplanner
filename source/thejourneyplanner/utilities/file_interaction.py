"""file_interaction.py: Functions for interacting with files."""

import os
import shutil
import webbrowser

from ..config.constants import Constants

from . import logger


def duplicate_last_log(
    output_directory: str = Constants.DEFAULT_SAVE_DIRECTORY,
) -> None:  # TODO: Redo this function, it's so janky
    """
    Duplicate the most recently modified log file to the output directory.

    Parameters
    ----------
    output_directory : str, optional
        The path to the output directory, by default Constants.DEFAULT_SAVE_DIRECTORY

    Raises
    ------
    FileNotFoundError
        If no files are found in the source directory.
    """
    if not output_directory:  # If the output directory is empty
        output_directory = Constants.DEFAULT_SAVE_DIRECTORY

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

    # Construct full file paths
    source_file_path = os.path.join(Constants.ARCHIVED_LOGS_DIRECTORY, latest_file)
    destination_file_path = os.path.join(output_directory, Constants.LOG_FILE_NAME)

    # Copy the latest log file to the output directory and rename it
    try:
        shutil.copy2(source_file_path, destination_file_path)
        print(f"Copied '{latest_file}' to '{destination_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return


def open_html_file(file_path: str) -> None:
    """
    Open the specified HTML file in the default web browser.

    Parameters
    ----------
    file_path : str
        The path to the HTML file to open.
    """
    logger.debug(f"Opening HTML file '{file_path}' in the default web browser.")
    absolute_path = os.path.abspath(file_path)
    file_url = f'file:///{absolute_path.replace(os.path.sep, "/")}'

    webbrowser.open(file_url, new=2)
    logger.info(
        f"Opened map with plotted polyline in the default web browser.\n"
        f"If the map does not open, please navigate to '{file_url}' manually."
    )
