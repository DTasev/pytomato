from defaults import (BREAK_NAME, BREAK_TYPE, LONG_BREAK_DURATION,
                      LONG_TOMATO_DURATION, SHORT_BREAK_DURATION,
                      SHORT_TOMATO_DURATION, TOMATO_NAME, TOMATO_TYPE)
from run_parameters import RunParameters
from argument_parser import setupParser


def _set_up_break_or_tomato(args, short_duration, long_duration, default_name, run_type):
    """
    :param args: The argument parser
    :param short_dur: Short duration for the run type
    :param long_dur: Long duration for the run type
    :param custom_dur: Custom duration provided by the user
    :param custom_name: Custom name provided by the user
    :param run_type: The run type
    """
    if args.short_break:
        parameters.duration = short_duration

    if args.long_break:
        parameters.duration = long_duration

    if args.duration:
        parameters.duration = args.duration

    if args.name:
        parameters.name = args.name
    else:
        parameters.name = default_name

    parameters.runType = run_type


def setUpRunParameters(parameters, args):
    # can't do both at the same time, we prefer long
    if args.short and args.long:
        args.short = False

    # run without any parameters it will be a short run
    if not args.duration and not args.short and not args.long:
        args.short = True

    if args.short_break or args.long_break:
        _set_up_break_or_tomato(args, SHORT_BREAK_DURATION, LONG_BREAK_DURATION,
                                BREAK_NAME, BREAK_TYPE)

    else:
        _set_up_break_or_tomato(args, SHORT_TOMATO_DURATION, LONG_TOMATO_DURATION,
                                TOMATO_NAME, TOMATO_TYPE)

    if args.project:
        # this will have the default value from conf.py if not changed here
        parameters.project_name = args.project

    parameters.clean = args.clean
    parameters.listAndExit = args.list
    parameters.delete = args.delete

    return parameters


def main(parameters, args):

    if args.cli:
        import timer
        timer = timer.Timer(parameters)
    else:
        try:
            import guitimer
            timer = guitimer.GUITimer(parameters)
        except ImportError as exc:
            print("Could not create GUI timer, you need PyQt5 installed! Or run with --cli for console mode.")
            return

    timer.run(parameters)


if __name__ == '__main__':
    parser = setupParser()
    args = parser.parse_args()

    parameters = RunParameters()
    parameters = setUpRunParameters(parameters, args)

    main(parameters, args)
