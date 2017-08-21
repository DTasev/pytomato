import argparse

from defaults import (DEFAULT_BREAK_NAME, DEFAULT_BREAK_TYPE,
                      DEFAULT_LONG_BREAK_DURATION,
                      DEFAULT_LONG_TOMATO_DURATION,
                      DEFAULT_SHORT_BREAK_DURATION,
                      DEFAULT_SHORT_TOMATO_DURATION, DEFAULT_TOMATO_NAME,
                      DEFAULT_TOMATO_TYPE, DefaultRun)


def setupParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--name",
        required=False,
        type=str,
        help="Help of the timer run."
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
        "-t",
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
        help="Clear the tomato past entries. This will delete the ~/.pytomato file."
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
        "-d",
        "--delete",
        type=int,
        help="Delete the entry and exit."
    )

    return parser


def setUpRunParameters(parameters, args):
    # can't do both at the same time, we prefer long
    if args.short and args.long:
        args.short = False

    # run without any parameters it will be a short run
    if not args.duration and not args.short and not args.long:
        args.short = True

    if args.short_break or args.long_break:
        if args.short_break:
            parameters.duration = DEFAULT_SHORT_BREAK_DURATION

        if args.long_break:
            parameters.duration = DEFAULT_LONG_BREAK_DURATION

        if args.duration:
            parameters.duration = args.duration

        parameters.name = DEFAULT_BREAK_NAME
        parameters.runType = DEFAULT_BREAK_TYPE

    else:
        if args.short:
            parameters.duration = DEFAULT_SHORT_TOMATO_DURATION

        if args.long:
            parameters.duration = DEFAULT_LONG_TOMATO_DURATION

        if args.duration:
            parameters.duration = args.duration

        parameters.name = DEFAULT_TOMATO_NAME
        parameters.runType = DEFAULT_TOMATO_TYPE

    parameters.clean = args.clean
    parameters.listAndExit = args.list
    parameters.delete = args.delete

    return parameters


def main(parameters, args):

    if args.cli:
        import timer
        timer = timer.Timer()
    else:
        import guitimer
        timer = guitimer.GUITimer()

    timer.run(parameters)


if __name__ == '__main__':

    parser = setupParser()
    args = parser.parse_args()

    parameters = DefaultRun()
    parameters = setUpRunParameters(parameters, args)

    main(parameters, args)
