from pytomato.conf import (BREAK_NAME, BREAK_TYPE, LONG_BREAK_DURATION,
                           LONG_TOMATO_DURATION, SHORT_BREAK_DURATION,
                           SHORT_TOMATO_DURATION, TOMATO_NAME, TOMATO_TYPE)
from pytomato.run_parameters import RunParameters
from pytomato.argument_parser import setupParser
from argparse import ArgumentParser


def _set_up_break_or_tomato(parameters: RunParameters, args: ArgumentParser,
                            short_duration: int, long_duration: int, default_name: str, run_type: str) -> RunParameters:
    """
    :param args: The argument parser
    :param short_dur: Short duration for the run type
    :param long_dur: Long duration for the run type
    :param custom_dur: Custom duration provided by the user
    :param custom_name: Custom name provided by the user
    :param run_type: The run type
    """
    if args.short_break:  # type: ignore
        parameters.duration = short_duration

    if args.long_break:  # type: ignore
        parameters.duration = long_duration

    if args.duration:  # type: ignore
        parameters.duration = args.duration  # type: ignore

    if args.name:  # type: ignore
        parameters.name = args.name  # type: ignore
    else:
        parameters.name = default_name

    parameters.runType = run_type

    return parameters


def set_up_run_parameters(parameters: RunParameters, args: ArgumentParser) -> RunParameters:
    # can't do both at the same time, we prefer long
    if args.short and args.long:  # type: ignore
        args.short = False  # type: ignore

    # run without any parameters it will be a short run
    if not args.duration and not args.short and not args.long:  # type: ignore
        args.short = True  # type: ignore

    if args.short_break or args.long_break:  # type: ignore
        parameters = _set_up_break_or_tomato(parameters, args, SHORT_BREAK_DURATION,
                                             LONG_BREAK_DURATION, BREAK_NAME, BREAK_TYPE)

    else:
        parameters = _set_up_break_or_tomato(parameters, args, SHORT_TOMATO_DURATION,
                                             LONG_TOMATO_DURATION, TOMATO_NAME, TOMATO_TYPE)

    if args.project:  # type: ignore
        # this will have the default value from conf.py if not changed here
        parameters.project_name = args.project  # type: ignore

    parameters.clean = args.clean  # type: ignore
    parameters.listAndExit = args.list  # type: ignore
    parameters.delete = args.delete  # type: ignore
    parameters.mute = args.mute  # type: ignore

    return parameters


def main():
    parser = setupParser()
    args = parser.parse_args()

    parameters = RunParameters()
    parameters = set_up_run_parameters(parameters, args)

    if args.cli:  # type: ignore
        from pytomato.timer import Timer
        timer = Timer(parameters)
    else:
        try:
            from pytomato.guitimer import GUITimer
            timer = GUITimer(parameters)
        except ImportError as exc:
            print("Could not create GUI timer, you need PyQt5 installed! Or run with --cli for console mode.")
            return

    timer.run()
