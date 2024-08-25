"""setup_logging.py: Set up the logging configuration."""

import logging
import os
from datetime import datetime
from typing import Literal

from rich.logging import RichHandler

from config.constants import Constants


def setup_logging(
    console_logging_level: Literal[
        "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
    ] = Constants.LOGGING_LEVEL_CONSOLE_DEFAULT,
    file_logging_level: Literal[
        "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"
    ] = Constants.LOGGING_LEVEL_LOGFILE_DEFAULT,
) -> None:
    """
    Setup logging configuration.

    Parameters
    ----------
    console_logging_level : Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], optional
        The logging level for the console handler, by default Constants.LOGGING_LEVEL_CONSOLE_DEFAULT
    file_logging_level : Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], optional
        The logging level for the file handler, by default Constants.LOGGING_LEVEL_LOGFILE_DEFAULT

    Raises
    ------
    ValueError
        If the logging level is invalid.

    Examples
    --------
    >>> setup_logging()

    >>> setup_logging(console_logging_level="WARNING", file_logging_level="DEBUG")

    Notes
    -----
    ...
    """
    valid_levels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }

    for logging_level in [console_logging_level, file_logging_level]:
        if logging_level not in valid_levels:
            raise ValueError(
                "Invalid logging level: "
                + logging_level
                + ". \nValid levels are: "
                + ", ".join(valid_levels.keys())
            )

    # Create logs directory if it does not exist
    os.makedirs(Constants.ARCHIVED_LOGS_DIRECTORY, exist_ok=True)

    # Create a log file with a timestamp
    timestamp = datetime.now().strftime(Constants.LOGGING_TIMESTAMP_FORMAT)
    logging_file = os.path.join(Constants.ARCHIVED_LOGS_DIRECTORY, f"{timestamp}.log")

    # Set up file handler
    file_handler = logging.FileHandler(logging_file)
    file_handler.setLevel(valid_levels[file_logging_level])
    file_handler.setFormatter(
        logging.Formatter(
            fmt=Constants.LOGGING_LOGFILE_FORMAT,
            datefmt=Constants.LOGGING_DATE_FORMAT,
        )
    )

    # Set up console handler
    console_handler = RichHandler(rich_tracebacks=Constants.LOGGING_TRACEBACKS)
    console_handler.setLevel(valid_levels[console_logging_level])
    console_handler.setFormatter(
        logging.Formatter(
            fmt=Constants.LOGGING_CONSOLE_FORMAT,
            datefmt=Constants.LOGGING_DATE_FORMAT,
        )
    )

    # Set up logging configuration
    logging.basicConfig(
        level=valid_levels["DEBUG"],
        handlers=[console_handler, file_handler],
    )
