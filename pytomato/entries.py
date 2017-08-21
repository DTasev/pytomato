import os
import pickle
import datetime

from utility import formatToHHMM

DEFAULT_TIMER_PICKLE_FILE = os.path.expanduser("~/.pytomato")
BACKUP_TIMER_PICKLE_FILE = os.path.expanduser("~/.pytomato.bak")


class Entries(object):
    def __init__(self, timer):
        self.timer = timer
        self.formattedEntries = None

    def initialise(self):
        if os.path.isfile(DEFAULT_TIMER_PICKLE_FILE):
            self.past_entries = pickle.load(open(DEFAULT_TIMER_PICKLE_FILE, 'rb'))
        else:
            self.past_entries = []

        self.listEntries()

    def listEntries(self):
        today = datetime.datetime.now().strftime("%Y%m%d")

        # filter out all of the entries that are not today
        self.formattedEntries = filter(lambda entry:
                                       entry["entry"]["entryEnd"].strftime("%Y%m%d") == today,
                                       self.past_entries)

        # pretty format
        self.formattedEntries = map(lambda entry: self.prettyFormat(entry), self.formattedEntries)

        if self.formattedEntries:
            for i, e in enumerate(self.formattedEntries):
                print(i, "-", e)

    def prettyFormat(self, entry):
        return "{} T:{} S: {} - {} elapsed: {}, target: {}min".format(
               entry["name"],
               entry["type"],
               entry["entry"]["entryStart"].strftime("%Y-%m-%d %H:%M"),
               entry["entry"]["entryEnd"].strftime("%H:%M"),
               formatToHHMM(entry["entry"]["elapsedTime"]),
               formatToHHMM(entry["entry"]["targetTime"]))

    def clean(self):
        """
        Clean the entries if the --clean parameter is specified.

        If the file is not found we silently fail
        """

        print("Deleting entries file", DEFAULT_TIMER_PICKLE_FILE)
        try:
            os.remove(DEFAULT_TIMER_PICKLE_FILE)
        except:
            print("File not found, nothing is changed.")

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

    def deleteEntry(self, id):
        try:
            print("Removing entry", id, ":", self.prettyFormat(self.past_entries[id]))
            del self.past_entries[id]

        except IndexError:
            print("Could not find entry. Nothing is changed")
