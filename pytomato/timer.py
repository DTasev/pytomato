import datetime
import time

from pytomato import entries
from pytomato.conf import BREAK_TYPE, SHORT_TOMATO_DURATION, TOMATO_TYPE, MINIMUM_DURATION_FOR_VALID_ENTRY
from pytomato.run_parameters import RunParameters
from pytomato.soundboard import SoundBoard
from pytomato.utility import formatToHHMM


class Timer(object):
    def __init__(self, parameters: RunParameters) -> None:
        self.entries = entries.Entries(parameters.run_type, parameters.name, parameters.project_name)
        self.notify_string = None
        self.soundboard = SoundBoard(parameters.mute)

    def init(self, run_type, target_time):
        self.entries.initialise()
        self.create_messages_for_run(run_type, target_time)

    def list_entries(self):
        self.entries.listEntries()

    def clean(self):
        self.entries.clean()

    def delete(self, entry):
        self.entries.delete_entry(self.parameters.delete)
        print("List state after deletion")
        self.entries.listEntries()
        self.entries.save()

    def force_upload(self):
        self.entries.save(True)
        return

    def process_entry(self, start_datetime, end_datetime, elapsed_time, target_time):
        if elapsed_time > MINIMUM_DURATION_FOR_VALID_ENTRY:
            self.entries.add(start_datetime, end_datetime, target_time)
            self.entries.save()
        else:
            print("Run is not long enough to be valid and it will not be saved. "
                  "Current mimimum duration for a valid run is {} seconds".format(
                      MINIMUM_DURATION_FOR_VALID_ENTRY))

    def closeEvent(self):
        # nothing to do for the CLI timer
        pass

    def notify(self):
        """
        This function is a wrapper to the notifyUser function to provide sanity checks.
        """
        assert self.notify_string is not None, "The notify function was called but "\
            "the notify message has not been created! Tomato Panic!"

        self.notifyUser()

    def create_messages_for_run(self, run_type, targetTime):
        # note: the strings below are intended to have empty spaces, to make sure they overwrite the whole line
        # because the print in the while loop uses \r to rewrite the line
        if run_type == BREAK_TYPE:
            self.notify_string = "Your break was {0} minutes long and is now over!         ".format(targetTime // 60)

        elif run_type == TOMATO_TYPE:
            self.notify_string = "Going Overtime! You should take a {0} break.             ".format(
                "5 minute" if targetTime <= SHORT_TOMATO_DURATION else "15 minute")

    def notifyUser(self):
        print(self.notify_string)
        self.soundboard.play_notification_sound()

    def updateVisuals(self, elapsedTime, targetTime, targetTimeString) -> str:
        """
        Create the CLI string, print to the command line window and return it

        :param elapsedTime: The elapsed time in seconds
        :param targetTime: The target time in seconds
        :param targetTimeString: The pretty-formatted target time toe HH:MM
        """
        output = "Elapsed time: {0}/{1} - Tomato is {2:.3f}% eaten.".format(formatToHHMM(
            elapsedTime), targetTimeString, (elapsedTime / targetTime) * 100)
        print(output, end="\r")
        return output
