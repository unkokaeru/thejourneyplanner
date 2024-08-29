"""route_planning.py: Functions for route planning."""

import logging

from ..config.constants import Constants
from ..integrations.google_maps import compute_route, search_nearby_places
from ..integrations.nominatim import find_longitude_and_latitude
from ..utilities.unit_conversion import convert_distance, convert_duration

logger = logging.getLogger(__name__)


class RoutePlanner:  # TODO: Re-work logic to create a more circular route
    """Finds a route between two locations with intermediate stops."""

    def __init__(self, api_key: str):
        """
        Initialise the RoutePlanner with API key.

        Parameters
        ----------
        api_key : str
            The API key for the Google Maps API.
        """
        self.api_key = api_key
        self.start_latlong: tuple[float, float] = (0, 0)
        self.end_latlong: tuple[float, float] = (0, 0)
        self.remaining_duration: float = 0
        self.intermediate_latlongs: list[tuple[float, float]] = []
        self.selected_latlongs: set[tuple[float, float]] = set()

    def _initialise_journey(self, start: str, end: str, duration: float) -> None:
        """
        Initialise journey details and calculate start and end latitude/longitude.

        Parameters
        ----------
        start : str
            The starting location for the journey.
        end : str
            The ending location for the journey.
        duration : float
            The total duration of the journey, in seconds.

        Raises
        ------
        ValueError
            If the ending location is not reachable within the specified duration.
        """
        self.remaining_duration = duration

        self.start_latlong = find_longitude_and_latitude(start)
        self.end_latlong = find_longitude_and_latitude(end)

        logger.debug(
            f"Initial journey details: "
            f"{self.remaining_duration}, {self.start_latlong}, {self.end_latlong}"
        )

        if not self._check_route_possibility(self.start_latlong, self.end_latlong):
            logger.fatal("Ending location not reachable within the specified duration.")
            raise ValueError("Ending location not reachable within the specified duration.")

    def _check_route_possibility(
        self, start_latlong: tuple[float, float], end_latlong: tuple[float, float]
    ) -> bool:
        """
        Check if the route is possible without any intermediate stops.

        Parameters
        ----------
        start_latlong : tuple[float, float]
            The starting latitude/longitude for the journey.
        end_latlong : tuple[float, float]
            The ending latitude/longitude for the journey.

        Returns
        -------
        bool
            True if the route is possible, False otherwise.
        """
        if (
            compute_route(self.api_key, start_latlong, end_latlong)["duration_seconds"]
            <= self.remaining_duration
        ):
            return True
        else:
            return False

    def _find_nearby_places(self) -> list[dict]:
        """
        Search for nearby places within the remaining duration.

        Returns
        -------
        list[dict]
            A list of nearby places, each represented as a dictionary containing place details.

        Notes
        -----
        The search is conducted based on the current starting latitude/longitude and the
        remaining duration converted to meters.
        """
        nearby_places = search_nearby_places(
            self.api_key,
            self.start_latlong,
            self.remaining_duration * Constants.CONVERSION_FACTOR_SECONDS_TO_METERS,
        )

        logger.debug(f"Nearby places (raw): {nearby_places}")

        return [
            place
            for place in reversed(nearby_places)
            if place["latlong"] not in self.selected_latlongs
            and place["latlong"] != self.end_latlong
        ]

    def _check_nearby_places(self, nearby_places: list[dict]) -> bool:
        """
        Check each nearby place for reachability and update the route if reachable.

        Parameters
        ----------
        nearby_places : list[dict]
            A list of nearby places to check, each represented as a dictionary.

        Returns
        -------
        bool
            True if at least one place was reachable, False otherwise.

        Notes
        -----
        This method updates the remaining duration and the starting latitude/longitude
        if a nearby place is reachable.
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

    def _finalise_route(self, start: str, end: str) -> dict[str, str | float]:
        """
        Calculate total route information including the end destination.

        Parameters
        ----------
        start : str
            The starting location for the journey.
        end : str
            The ending location for the journey.

        Returns
        -------
        dict[str, str | float]
            A dictionary containing the total route information, including duration and distance.

        Raises
        ------
        ValueError
            If no nearby places were found within the specified duration.

        Notes
        -----
        This method computes the total route information using the starting and ending
        latitude/longitude along with any intermediate stops.
        """
        if not self.intermediate_latlongs:
            logger.fatal("No nearby places found within the specified duration.")
            raise ValueError("No nearby places found within the specified duration.")

        total_route_information = compute_route(
            self.api_key,
            self.start_latlong,
            self.end_latlong,
            self.intermediate_latlongs,
        )

        logger.debug(f"Total route information: {total_route_information}")
        logger.info(
            f"The route between {start} and {end} "
            f"has been planned successfully with "
            f"{len(self.intermediate_latlongs)} intermediate stops.\n"
            f"It should take "
            f"{convert_duration(total_route_information['duration_seconds'], 'seconds')} "
            f"to travel the "
            f"{convert_distance(total_route_information['distance_meters'], 'meters')} "
            f"of the journey."
        )

        return total_route_information

    def plan_route(self, start: str, end: str, duration: float) -> dict[str, str | float]:
        """
        Plan the route by finding nearby points of interest.

        Parameters
        ----------
        start : str
            The starting location for the journey.
        end : str
            The ending location for the journey.
        duration : float
            The total duration of the journey, in seconds.

        Returns
        -------
        dict[str, str | float]
            A dictionary containing the route information, including duration and distance.

        Notes
        -----
        This method initializes the journey and iteratively finds nearby places until
        the remaining duration is exhausted or no more reachable places are found.
        """
        self._initialise_journey(start, end, duration)

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

        return self._finalise_route(start, end)
