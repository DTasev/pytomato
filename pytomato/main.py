import datetime
import time
from argparse import ArgumentParser

from pytomato.argument_parser import setupParser
from pytomato.conf import (BREAK_TYPE, DEFAULT_BREAK_NAME, DEFAULT_TOMATO_NAME,
                           LONG_BREAK_DURATION, LONG_TOMATO_DURATION,
                           SHORT_BREAK_DURATION, SHORT_TOMATO_DURATION,
                           TOMATO_TYPE)
from pytomato.run_parameters import RunParameters
from pytomato.utility import formatToHHMM


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
        parameters.run_name = args.name  # type: ignore
    else:
        parameters.run_name = default_name

    parameters.run_type = run_type

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
                                             LONG_BREAK_DURATION, DEFAULT_BREAK_NAME, BREAK_TYPE)

    else:
        parameters = _set_up_break_or_tomato(parameters, args, SHORT_TOMATO_DURATION,
                                             LONG_TOMATO_DURATION, DEFAULT_TOMATO_NAME, TOMATO_TYPE)

    if args.project:  # type: ignore
        # this will have the default value from conf.py if not changed here
        parameters.project_name = args.project  # type: ignore

    parameters.clean = args.clean  # type: ignore
    parameters.list_and_exit = args.list  # type: ignore
    parameters.delete = args.delete  # type: ignore
    parameters.mute = args.mute  # type: ignore
    parameters.force_upload = args.upload  # type: ignore

    return parameters


def main():
    parser = setupParser()
    args = parser.parse_args()

    parameters = set_up_run_parameters(RunParameters(), args)

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

    run(timer, parameters)


def run(timer, parameters):
    if parameters.clean:
        timer.clean()
        return

    target_time = parameters.duration
    timer.init(parameters.run_type, target_time)
    timer.list_entries()

    if parameters.list_and_exit:
        return

    # check if not none, because single integers get cast to booleans..
    if parameters.delete is not None:
        timer.delete(parameters.delete)
        return

    if parameters.force_upload:
        # The parameter is set on initialisation, we only need to call save and it will be upload
        timer.force_upload()
        return

    print("Project:", parameters.project_name)
    print("Entry name:", parameters.run_name)
    print("Target time", target_time // 60, "minutes")

    start_datetime = datetime.datetime.now()
    elapsed_time = 0
    user_notified = False

    target_timeString = formatToHHMM(target_time)
    # start the initial update timer
    update_compensation_timer = time.time()
    try:
        while True:
            timer.updateVisuals(elapsed_time, target_time, target_timeString)
            # sleep for the rest of the 1 second, by subtracting the time spent processing
            time.sleep(abs(1 - (time.time() - update_compensation_timer)))
            elapsed_time += 1

            # warn the user only when we're over the target time and we haven't previously notified them
            if not user_notified and elapsed_time >= target_time:
                timer.notify()
                user_notified = True
            # update the update timer after everything has been completed timer
            update_compensation_timer = time.time()

    # if anything happens try to end and save out the file
    # note: the strings below are intended to have empty spaces, to make sure they overwrite the whole line
    # because the print in the while loop uses \r to rewrite the line
    except KeyboardInterrupt:
        print("Interripting timer and saving entry.                  ")
    except SystemExit:
        print("System exiting, saving entry.                         ")

    end_datetime = datetime.datetime.now()
    timer.closeEvent()
    timer.process_entry(start_datetime, end_datetime, elapsed_time, target_time)
