import datetime
import time

from pytomato import entries
from pytomato.conf import BREAK_TYPE, SHORT_TOMATO_DURATION, TOMATO_TYPE, MINIMUM_DURATION_FOR_VALID_ENTRY
from pytomato.run_parameters import RunParameters
from pytomato.soundboard import SoundBoard
from pytomato.utility import formatToHHMM


class Timer(object):
    def __init__(self, parameters: RunParameters) -> None:
        self.run_name = parameters.name
        self.run_type = parameters.run_type
        self.project_name = parameters.project_name
        self.force_upload = parameters.force_upload
        self.parameters = parameters

        self.entries = entries.Entries(self.run_type, self.run_name, self.project_name)
        self.notify_string = None
        self.soundboard = SoundBoard(parameters.mute)

    def run(self):
        if self.parameters.clean:
            self.entries.clean()
            return

        self.entries.initialise()
        self.entries.listEntries()

        if self.parameters.list_and_exit:
            # List all entries if list is specified
            return

        # check if not none, because single integers get cast to booleans..
        if self.parameters.delete is not None:
            self.entries.delete_entry(self.parameters.delete)
            print("List state after deletion")
            self.entries.listEntries()
            self.entries.save()
            return

        if self.force_upload:
            # The parameter is set on initialisation, we only need to call save and it will be upload
            self.entries.save(self.force_upload)
            return

        # convert to minutes
        targetTime = self.parameters.duration

        self.create_messages_for_run(self.run_type, targetTime)

        print("Project:", self.project_name)
        print("Entry name:", self.run_name)
        print("Target time", targetTime // 60, "minutes")

        startDateTime = datetime.datetime.now()
        elapsedTime = 0
        userNotified = False

        targetTimeString = formatToHHMM(targetTime)
        # start the initial update timer
        update_compensation_timer = time.time()
        try:
            while True:
                self.updateVisuals(elapsedTime, targetTime, targetTimeString)
                # sleep for the rest of the 1 second, by subtracting the time spent processing
                time.sleep(abs(1 - (time.time() - update_compensation_timer)))
                elapsedTime += 1

                # warn the user only when we're over the target time and we haven't previously notified them
                if not userNotified and elapsedTime >= targetTime:
                    self.notify()
                    userNotified = True
                # update the update timer after everything has been completed timer
                update_compensation_timer = time.time()

        # if anything happens try to end and save out the file
        # note: the strings below are intended to have empty spaces, to make sure they overwrite the whole line
        # because the print in the while loop uses \r to rewrite the line
        except KeyboardInterrupt:
            print("Interripting timer and saving entry.                  ")
        except SystemExit:
            print("System exiting, saving entry.                         ")

        endDateTime = datetime.datetime.now()
        self.closeEvent()

        # only save if the run is long enough
        if elapsedTime > MINIMUM_DURATION_FOR_VALID_ENTRY:
            self.entries.add(startDateTime, endDateTime, elapsedTime, targetTime)
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
