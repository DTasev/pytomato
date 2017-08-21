import datetime
import time

import entries
from defaults import (DEFAULT_BREAK_TYPE, DEFAULT_SHORT_TOMATO_DURATION,
                      DEFAULT_TOMATO_TYPE, DefaultRun)
from utility import formatToHHMM


class Timer(object):
    def __init__(self):
        self.name = None
        self.runType = None
        self.notifyString = None
        self.entries = entries.Entries(self)

    def run(self, parameters: DefaultRun):
        if parameters.clean:
            self.entries.clean()

        self.entries.initialise()

        # convert to minutes
        targetTime = parameters.duration
        self.name = parameters.name
        self.runType = parameters.runType

        self.createMessagesForRun(self.runType, targetTime)

        print(self.name, "target time", targetTime // 60, "minutes")

        startDateTime = datetime.datetime.now()
        elapsedTime = 0
        userNotified = False

        targetTimeString = formatToHHMM(targetTime)
        try:
            while True:
                self.updateVisuals(elapsedTime, targetTime, targetTimeString)
                time.sleep(0.9)
                elapsedTime += 1

                # warn the user only when we're over the target time and we haven't previously notified them
                if not userNotified and elapsedTime > targetTime:
                    self.notify()
                    userNotified = True

        # if anything happens try to end and save out the file
        except KeyboardInterrupt:
            print("Interripting timer and saving entry.")

        endDateTime = datetime.datetime.now()
        self.entries.add(startDateTime, endDateTime, elapsedTime, targetTime)
        self.entries.save()

    def notify(self):
        """
        This function is a wrapper to the notifyUser function to provide sanity checks.
        """
        assert self.notifyString is not None, "The notify function was called but "\
            "the notify message has not been created! Tomato Panic!"

        self.notifyUser()

    def createMessagesForRun(self, runType, targetTime):
        if runType == DEFAULT_BREAK_TYPE:
            self.notifyString = "Your break was {0} minutes long and is now over!".format(targetTime // 60)

        elif runType == DEFAULT_TOMATO_TYPE:
            self.notifyString = "Going Overtime! You should take a {0} break.".format(
                "5 minute" if targetTime <= DEFAULT_SHORT_TOMATO_DURATION else "15 minute")

    def notifyUser(self):
        print(self.notifyString)

    def updateVisuals(self, elapsedTime, targetTime, targetTimeString):
        output = "Elapsed time: {0}/{1} - Tomato is {2:.3f}% eaten.".format(formatToHHMM(
            elapsedTime), targetTimeString, (elapsedTime / targetTime) * 100)
        print(output, end="\r")
