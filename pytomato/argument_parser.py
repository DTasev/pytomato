import argparse


def setupParser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--name",
        required=False,
        type=str,
        help="Name for the entry."
    )

    parser.add_argument(
        "-p",
        "--project",
        required=False,
        type=str,
        help="Project for which this entry is. This will be saved and reused for consecutive entries, "
             "until a new project is specified."
    )

    parser.add_argument(
        "-s",
        "--short",
        required=False,
        action='store_true',
        help="Run a short tomato run, 25 minutes."
    )

    parser.add_argument(
        "-l",
        "--long",
        required=False,
        action='store_true',
        help="Run a short tomato run, 50 minutes."
    )

    parser.add_argument(
        "-d",
        "--duration",
        required=False,
        type=int,
        help="Set a custom duration as the timer. Input expects seconds"
    )

    parser.add_argument(
        "--clean",
        action='store_true',
        help="Clear the tomato past entries. This will delete the ~/.pytomato file."
    )

    parser.add_argument(
        "--cli",
        action='store_true',
        help="Run the timer without importing any of the GUI packages."
    )

    parser.add_argument(
        "-b",
        "--short-break",
        action='store_true',
        help="Do a break run. Default break is 5 minutes."
    )

    parser.add_argument(
        "-lb",
        "--long-break",
        action='store_true',
        help="Do a break run. Default break is 5 minutes."
    )

    parser.add_argument(
        "-i",
        "--list",
        action='store_true',
        help="List the entires and exit."
    )

    parser.add_argument(
        "--delete",
        type=int,
        help="Delete the entry and exit."
    )

    parser.add_argument(
        "-m",
        "--mute",
        action='store_true',
        help="Mute the sound that is played when the tomato timer is finished."
    )

    return parser
