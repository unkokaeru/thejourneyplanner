"""main.py: Called when the package is run as a script."""

from logging import shutdown as shutdown_logging

from .computation.route_planning import RoutePlanner
from .interface.command_line import command_line_interface
from .logs.setup_logging import setup_logging
from .utilities.file_interaction import duplicate_last_log
from .utilities.polyline_interaction import plot_polyline


def main() -> None:
    """
    Main function for the application.

    Notes
    -----
    This function is the entry point for the application.
    """
    user_arguments = command_line_interface()

    route_planner = RoutePlanner(user_arguments["api_key"])

    route_details = route_planner.plan_route(
        user_arguments["start"],
        user_arguments["end"] if user_arguments["end"] else user_arguments["start"],
        user_arguments["duration"] * 60,  # Convert minutes to seconds
    )

    plot_polyline(
        str(route_details["encoded_polyline"]),
        user_arguments["output"],
        user_arguments["open_map"],
    )

    duplicate_last_log(user_arguments["output"])


if __name__ == "__main__":
    setup_logging()
    main()
    shutdown_logging()
