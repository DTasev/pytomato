import os
import pickle

from utility import formatToHHMM

DEFAULT_TIMER_PICKLE_FILE = os.path.expanduser("~/.pytomato")
BACKUP_TIMER_PICKLE_FILE = os.path.expanduser("~/.pytomato.bak")


class Entries(object):
    def __init__(self, timer):
        self.timer = timer

    def initialise(self):
        if os.path.isfile(DEFAULT_TIMER_PICKLE_FILE):
            self.past_entries = pickle.load(open(DEFAULT_TIMER_PICKLE_FILE, 'rb'))
        else:
            self.past_entries = []

        entries = map(lambda entry: "{} T:{} S: {} - {} elapsed: {}, target: {}min".format(
            entry["name"],
            entry["type"],
            entry["entry"]["entryStart"].strftime("%Y-%m-%d %H:%M"),
            entry["entry"]["entryEnd"].strftime("%H:%M"),
            formatToHHMM(entry["entry"]["elapsedTime"]),
            formatToHHMM(entry["entry"]["targetTime"])),
            self.past_entries)

        if entries:
            for e in entries:
                print(e)

    def clean(self):
        """
        Clean the entries if the --clean parameter is specified.

        If the file is not found we silently fail
        """

        print("Deleting entries file", DEFAULT_TIMER_PICKLE_FILE)
        try:
            os.remove(DEFAULT_TIMER_PICKLE_FILE)
        except:
            print("File not found, continuing")

    def add(self, startDateTime, endDateTime, elapsedTime, targetTime):
        self.past_entries.append(
            {
                "name": self.timer.name,
                "type": self.timer.runType,
                "entry":
                {
                    "entryStart": startDateTime,
                    "entryEnd": endDateTime,
                    "elapsedTime": elapsedTime,
                    "targetTime": targetTime
                }
            }
        )

    def save(self):
        # don't save in original file, save in a backup copy
        pickle.dump(self.past_entries, open(BACKUP_TIMER_PICKLE_FILE, 'wb'))
        # then overwrite the original
        os.replace(BACKUP_TIMER_PICKLE_FILE, DEFAULT_TIMER_PICKLE_FILE)
