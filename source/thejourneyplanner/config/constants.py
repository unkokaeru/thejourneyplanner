"""constants.py: Constants for the application."""

from pathlib import Path
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
    LOGGING_LOGFILE_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_CONSOLE_FORMAT: str = "%(message)s"
    LOGGING_TIMESTAMP_FORMAT: str = "%Y-%m-%d_%H-%M-%S"
    LOGGING_DATE_FORMAT: str = "[%X]"
    LOGGING_TRACEBACKS: bool = True
    ARCHIVED_LOGS_DIRECTORY: Path = Path("logs/archived_logs")

    # API response constants
    SUCCESS_CODE: int = 200
    SUCCESS_TEXT: str = "OK"
    FORBIDDEN_CODE: int = 403

    # API constants
    MAX_NEARBY_PLACES: int = 20
    API_MAX: int = 8
    LANGUAGE_CODE: str = "en-GB"

    DISTANCE_MATRIX_URL: str = "https://maps.googleapis.com/maps/api/distancematrix/json"
    NEARBY_SEARCH_URL: str = "https://places.googleapis.com/v1/places:searchNearby"
    NEARBY_SEARCH_FIELD_MASK = (
        "places.displayName,"
        "places.location,"
        "places.formattedAddress,"
        "places.rating,"
        "places.userRatingCount"
    )
    NEARBY_SEARCH_RANK_BY: str = "DISTANCE"
    NEARBY_SEARCH_TYPES: list[str] = ["tourist_attraction"]
    COMPUTE_ROUTES_URL: str = "https://routes.googleapis.com/directions/v2:computeRoutes"
    COMPUTE_ROUTES_FIELD_MASK = (
        "routes.duration," "routes.distanceMeters," "routes.polyline.encodedPolyline"
    )
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"
    NOMINATIM_USER_AGENT: str = "Mozilla/5.0"

    # Computation constants
    CONVERSION_FACTOR_MINUTES_TO_METERS: int = 750  # meters per minute (just under 30mph)
    CONVERSION_FACTOR_SECONDS_TO_METERS: float = CONVERSION_FACTOR_MINUTES_TO_METERS / 60

    # Default values
    DEFAULT_LOG_SAVE_PATH: Path = Path("thejourneyplanner-log.txt")
    DEFAULT_MAP_SAVE_PATH: Path = Path("thejourneyplanner-map.html")
    DEFAULT_OPEN_MAP: bool = False
