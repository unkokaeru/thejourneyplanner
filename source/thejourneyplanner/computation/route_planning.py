"""route_planning.py: Functions for route planning."""

import logging

from ..config.constants import Constants
from ..integrations.google_maps import (
    compute_route,
    get_distance_matrix,
    search_nearby_places,
)
from ..integrations.nominatim import find_longitude_and_latitude
from ..utilities.unit_conversion import convert_distance, convert_duration

logger = logging.getLogger(__name__)


class RoutePlanner:  # TODO: Re-work logic to create a more circular route
    """Finds a route between two locations with intermediate stops."""

    def __init__(self, api_key: str, start: str, end: str, duration: int):
        """
        Initialise the RoutePlanner with API key, start and end locations, and duration.

        Parameters
        ----------
        api_key : str
            The API key for the Google Maps API.
        start : str
            The starting location for the journey.
        end : str
            The ending location for the journey.
        duration : int
            The total duration of the journey, in seconds.
        """
        self.api_key = api_key
        self.start: tuple[str, tuple[float, float]] = (start, (0, 0))
        self.end: tuple[str, tuple[float, float]] = (end, (0, 0))
        self.duration = duration
        self.start_latlong: tuple[float, float] = (0, 0)
        self.end_latlong: tuple[float, float] = (0, 0)
        self.remaining_duration = duration
        self.intermediate_latlongs: list[tuple[float, float]] = []
        self.selected_latlongs: set[tuple[float, float]] = set()

        self._initialise_journey()
        self._check_route_possibility()

    def _initialise_journey(self) -> None:
        """Initialise journey details and calculate start and end latitude/longitude."""
        start_to_end_distance_matrix = get_distance_matrix(self.api_key, self.start[0], self.end[0])

        self.start_latlong = find_longitude_and_latitude(
            start_to_end_distance_matrix["start_location"]
        )
        self.end_latlong = find_longitude_and_latitude(start_to_end_distance_matrix["end_location"])

        self.start = (self.start[0], self.start_latlong)
        self.end = (self.end[0], self.end_latlong)

        logger.debug(
            f"Initial journey details: "
            f"{self.remaining_duration}, {self.start_latlong}, {self.end_latlong}"
        )

    def _check_route_possibility(self) -> None:
        """Check if the route is possible without any intermediate stops."""
        if (
            get_distance_matrix(self.api_key, self.start[0], self.end[0])["duration_value"]
            > self.duration
        ):
            logger.fatal("Ending location not reachable within the specified duration.")
            raise ValueError("Ending location not reachable within the specified duration.")

    def _find_nearby_places(self) -> list[dict]:
        """
        Search for nearby places within the remaining duration.

        Returns
        -------
        list[dict]
            A list of nearby places.
        """
        nearby_places = search_nearby_places(
            self.api_key,
            self.start_latlong,
            self.remaining_duration * Constants.CONVERSION_FACTOR_SECONDS_TO_METERS,
        )

        logger.debug(f"Nearby places (raw): {nearby_places}")

        return [
            place
            for place in nearby_places
            if place["latlong"] not in self.selected_latlongs
            and place["latlong"] != self.end_latlong
        ]

    def _check_nearby_places(self, nearby_places: list[dict]) -> bool:
        """
        Check each nearby place for reachability and update the route if reachable.

        Parameters
        ----------
        nearby_places : list[dict]
            A list of nearby places to check.

        Returns
        -------
        bool
            True if at least one place was reachable, False otherwise.
        """
        for place in nearby_places:
            selected_latlong = place["latlong"]
            route_to_selection = compute_route(self.api_key, self.start_latlong, selected_latlong)

            logger.debug(f"Route to selection: {route_to_selection}")

            if route_to_selection["duration_seconds"] <= self.remaining_duration:
                self.remaining_duration -= route_to_selection["duration_seconds"]
                self.intermediate_latlongs.append(selected_latlong)
                self.selected_latlongs.add(selected_latlong)
                self.start_latlong = selected_latlong

                logger.info(
                    f"Added {selected_latlong} to route. "
                    f"Remaining duration: {self.remaining_duration}"
                )
                return True  # A place was reachable
        return False  # No places were reachable

    def _finalise_route(self) -> dict[str, str | int]:
        """
        Calculate total route information including the end destination.

        Returns
        -------
        dict[str, str | int]
            A dictionary containing the total route information.
        """
        if not self.intermediate_latlongs:
            logger.fatal("No nearby places found within the specified duration.")
            raise ValueError("No nearby places found within the specified duration.")

        total_route_information = compute_route(
            self.api_key,
            self.start[1],
            self.end[1],
            self.intermediate_latlongs,
        )

        logger.debug(f"Total route information: {total_route_information}")
        logger.info(
            f"The route between {self.start[0]} and {self.end[0]} "
            f"has been planned successfully with "
            f"{len(self.intermediate_latlongs)} intermediate stops.\n"
            f"It should take "
            f"{convert_duration(total_route_information['duration_seconds'], 'seconds')} "
            f"to travel the "
            f"{convert_distance(total_route_information['distance_meters'], 'meters')} "
            f"of the journey."
        )

        return total_route_information

    def plan_route(self) -> dict[str, str | int]:
        """
        Plan the route by finding nearby points of interest.

        Returns
        -------
        dict[str, str | int]
            A dictionary containing the route information.
        """
        while self.remaining_duration > 0:
            if len(self.intermediate_latlongs) >= Constants.API_MAX:
                logger.warning("Maximum number of intermediate stops reached.")
                break

            nearby_places = self._find_nearby_places()
            if not nearby_places:
                logger.warning("No more unique nearby places available to select.")
                break

            if not self._check_nearby_places(nearby_places):
                logger.warning("No nearby places are reachable within the remaining duration.")
                break

        return self._finalise_route()
