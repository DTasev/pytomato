import datetime
import time

from pytomato import entries
from pytomato.conf import BREAK_TYPE, SHORT_TOMATO_DURATION, TOMATO_TYPE
from pytomato.run_parameters import RunParameters
from pytomato.soundboard import SoundBoard
from pytomato.utility import formatToHHMM


class Timer(object):
    def __init__(self, parameters: RunParameters) -> None:
        self.name = parameters.name
        self.runType = parameters.runType
        self.project_name = parameters.project_name
        self.parameters = parameters

        self.entries = entries.Entries(self, self.project_name, parameters.force_upload)
        self.notifyString = None
        self.soundboard = SoundBoard(parameters.mute)

    def run(self):
        if self.parameters.clean:
            self.entries.clean()
            return

        self.entries.initialise()
        if self.parameters.listAndExit:
            # List all entries if list is specified
            self.entries.listEntries(list_all_entires=True)
            return
        else:
            # otherwise list just today
            self.entries.listEntries()

        # check if not none, because single integers get cast to booleans..
        if self.parameters.delete is not None:
            self.entries.deleteEntry(self.parameters.delete)
            print("List state after deletion")
            self.entries.listEntries()
            self.entries.save(self.name)
            return

        # convert to minutes
        targetTime = self.parameters.duration

        self.createMessagesForRun(self.runType, targetTime)

        print("Project:", self.project_name)
        print("Entry name:", self.name)
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
                time.sleep(1 - (time.time()-update_compensation_timer))
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
        self.entries.add(startDateTime, endDateTime, elapsedTime, targetTime)
        self.entries.save(self.name)

    def closeEvent(self):
        # nothing to do for the CLI timer
        pass

    def notify(self):
        """
        This function is a wrapper to the notifyUser function to provide sanity checks.
        """
        assert self.notifyString is not None, "The notify function was called but "\
            "the notify message has not been created! Tomato Panic!"

        self.notifyUser()

    def createMessagesForRun(self, runType, targetTime):
        # note: the strings below are intended to have empty spaces, to make sure they overwrite the whole line
        # because the print in the while loop uses \r to rewrite the line
        if runType == BREAK_TYPE:
            self.notifyString = "Your break was {0} minutes long and is now over!         ".format(targetTime // 60)

        elif runType == TOMATO_TYPE:
            self.notifyString = "Going Overtime! You should take a {0} break.             ".format(
                "5 minute" if targetTime <= SHORT_TOMATO_DURATION else "15 minute")

    def notifyUser(self):
        print(self.notifyString)
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
