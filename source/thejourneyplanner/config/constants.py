"""constants.py: Constants for the application."""

from typing import Literal


class Constants:
    """
    Constants for the application.

    Notes
    -----
    This class contains constants used throughout the application.
    By storing constants in a single location, it is easier to
    manage and update them. Constants should be defined as class
    attributes and should be named in uppercase with underscores
    separating words.
    """

    # Logging constants
    POSSIBLE_LOGGING_LEVELS = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    LOGGING_LEVEL_LOGFILE_DEFAULT: POSSIBLE_LOGGING_LEVELS = "DEBUG"
    LOGGING_LEVEL_CONSOLE_DEFAULT: POSSIBLE_LOGGING_LEVELS = "INFO"
    LOGGING_LOGFILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_CONSOLE_FORMAT = "%(message)s"
    LOGGING_TIMESTAMP_FORMAT: str = "%Y-%m-%d_%H-%M-%S"
    LOGGING_DATE_FORMAT = "[%X]"
    LOGGING_TRACEBACKS = True
    ARCHIVED_LOGS_DIRECTORY: str = "logs/archived_logs"

    # API response constants
    SUCCESS_CODE = 200
    SUCCESS_TEXT = "OK"
    FORBIDDEN_CODE = 403

    # API constants
    MAX_NEARBY_PLACES = 20
    API_MAX = 8
    LANGUAGE_CODE = "en-GB"

    DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
    NEARBY_SEARCH_URL = "https://places.googleapis.com/v1/places:searchNearby"
    NEARBY_SEARCH_FIELD_MASK = (
        "places.displayName,"
        "places.location,"
        "places.formattedAddress,"
        "places.rating,"
        "places.userRatingCount"
    )
    NEARBY_SEARCH_RANK_BY = "DISTANCE"
    NEARBY_SEARCH_TYPES = ["tourist_attraction"]
    COMPUTE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
    COMPUTE_ROUTES_FIELD_MASK = (
        "routes.duration," "routes.distanceMeters," "routes.polyline.encodedPolyline"
    )

    # Computation constants
    CONVERSION_FACTOR_MINUTES_TO_METERS: int = 750  # meters per minute (just under 30mph)
    CONVERSION_FACTOR_SECONDS_TO_METERS: float = CONVERSION_FACTOR_MINUTES_TO_METERS / 60

    # Default save values
    DEFAULT_SAVE_DIRECTORY: str = "output/"
    LOG_FILE_NAME: str = "log.txt"
