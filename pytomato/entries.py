import datetime
import os
import pickle

from pytomato.conf import (GIT_EXECUTABLE_PATH, GIT_REMOTE_REPOSITORY_URI,
                           PROJECT_EXTENSION, PYTOMATO_PROJECTS_DIR)
from pytomato.git_handler import GitHandler
from pytomato.utility import formatToHHMM


class Entries(object):
    def __init__(self, timer, run_name, project_name, force_upload):
        """
        :param timer: The timer object
        :param project_name: This will be used as the file name inside the projects directory.
        """
        self.timer = timer
        self.run_name = run_name
        self.formattedEntries = None

        self.project_name = project_name + PROJECT_EXTENSION
        self.project_directory = os.path.expanduser(PYTOMATO_PROJECTS_DIR)

        self.force_upload = force_upload

        self.timer_pickle_file = os.path.join(self.project_directory, self.project_name)
        # this is used to save first and then overwrite the original to not corrupt the file on save
        self.backup_timer_pickle_file = self.timer_pickle_file + ".bak"

    def initialise(self):
        self.ensure_directory_exists()
        self.gh = GitHandler(git=GIT_EXECUTABLE_PATH, repo_location=PYTOMATO_PROJECTS_DIR,
                             repo_remote_uri=GIT_REMOTE_REPOSITORY_URI)
        self.gh.init()

        if os.path.isfile(self.timer_pickle_file):
            print("Found existing file, loading entries")
            self.past_entries = pickle.load(open(self.timer_pickle_file, 'rb'))
            print(len(self.past_entries), "entries loaded in total.")
        else:
            self.past_entries = []

    def listEntries(self):
        """
        :param list_all_entires: List all of the entries regardless of when they were added.
        """

        # pretty format the entries
        self.past_entries = map(lambda entry: self.prettyFormat(entry), self.past_entries)

        if self.past_entries:
            for i, e in enumerate(self.past_entries):
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

        print("Deleting entries file", self.timer_pickle_file)
        try:
            os.remove(self.timer_pickle_file)
        except:
            print("File not found, nothing is changed.")

    def add(self, startDateTime, endDateTime, elapsedTime, targetTime):
        self.past_entries.append(
            {
                "name": self.run_name,
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

    def ensure_directory_exists(self):
        if not os.path.isdir(self.project_directory):
            os.mkdir(self.project_directory)

    def save(self):
        self.ensure_directory_exists()

        # don't save in original file, save in a backup copy
        pickle.dump(self.past_entries, open(self.backup_timer_pickle_file, 'wb'))
        # then overwrite the original
        os.replace(self.backup_timer_pickle_file, self.timer_pickle_file)

        self.backup_entries(self.run_name)

    def deleteEntry(self, id):
        print("List length before removal:", len(self.past_entries))
        try:
            print("Removing entry", id, ":", self.prettyFormat(self.past_entries[id]))
            del self.past_entries[id]

        except IndexError:
            print("Could not find entry. Nothing is changed")
        
        print("List length after removal:", len(self.past_entries))

    def backup_entries(self, name):
        self.gh.upload("{} {}".format(name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), self.force_upload)
