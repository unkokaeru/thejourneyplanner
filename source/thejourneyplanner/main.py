"""main.py: Called when the package is run as a script."""

from logging import shutdown as shutdown_logging
from pathlib import Path

from .computation.route_planning import RoutePlanner
from .interface.command_line import command_line_interface
from .logs.setup_logging import setup_logging
from .utilities.polyline_interaction import plot_polyline


def main() -> None:
    """
    Main function for the application.

    Notes
    -----
    This function is the entry point for the application.
    """
    # Get the arguments from the command line
    user_arguments = command_line_interface()

    # Extract the arguments
    start: str = user_arguments["start"]
    end: str = user_arguments["end"] if user_arguments["end"] else start
    duration: float = user_arguments["duration"] * 60  # Convert minutes to seconds
    map_output_location: Path = Path(user_arguments["map_output"])
    log_output_location: Path = user_arguments["log_output"]
    open_map = user_arguments["open_map"]
    verbose = user_arguments["verbose"]

    # Setup logging
    if verbose:
        setup_logging(log_output_location, console_logging_level="DEBUG")
    else:
        setup_logging(log_output_location)

    # Plan the route
    route_planner = RoutePlanner(user_arguments["api_key"])
    route_details = route_planner.plan_route(
        start,
        end,
        duration,
    )

    # Plot the route on the map
    plot_polyline(
        str(route_details["encoded_polyline"]),
        map_output_location,
        open_map,
    )

    shutdown_logging()


if __name__ == "__main__":
    main()
