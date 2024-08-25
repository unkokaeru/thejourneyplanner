"""command_line.py: Command line interface for the application."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import Any, Dict

from . import logger


def command_line_interface() -> Dict[str, Any]:
    """
    Takes arguments from the command line and returns them as a dictionary.

    Returns
    -------
    dict[str, Any]
        A dictionary containing the arguments passed to the application.
    """
    argparser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )  # Automatically generates help messages

    argparser.add_argument(
        "--api_key",
        "-k",
        action="store",
        type=str,
        required=True,
        help="API key for the Google Maps API.",
    )  # API key

    argparser.add_argument(
        "--output",
        "-o",
        action="store",
        type=str,
        required=False,
        help="Path to save the output.",
    )  # Path to save the output

    argparser.add_argument(
        "--start",
        "-s",
        action="store",
        type=str,
        required=True,
        help="Starting location for the journey.",
    )  # Starting location

    argparser.add_argument(
        "--end",
        "-e",
        action="store",
        type=str,
        required=False,
        help=(
            "Ending location for the journey, "
            "if not provided, the journey will be a return journey."
        ),
    )  # Ending location

    argparser.add_argument(
        "--duration",
        "-d",
        action="store",
        type=int,
        required=True,
        help="Duration of the journey in minutes.",
    )  # Duration of the journey

    parsed_args = argparser.parse_args()

    # Create a dictionary to return the parsed arguments
    arguments: Dict[str, Any] = {
        "api_key": parsed_args.api_key,
        "output": parsed_args.output,
        "start": parsed_args.start,
        "end": parsed_args.end,
        "duration": parsed_args.duration,
    }  # TODO: Add more arguments as needed, e.g. logging level and output file

    logger.debug(f"Arguments: {arguments}")

    return arguments
