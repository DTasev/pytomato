import datetime
import os
import json

from pytomato.conf import (GIT_EXECUTABLE_PATH, GIT_REMOTE_REPOSITORY_URI,
                           PROJECT_EXTENSION, PYTOMATO_PROJECTS_DIR)
from pytomato.git_handler import GitHandler
from pytomato.utility import formatToHHMM


class Entries(object):
    def __init__(self, run_type, run_name, project_name):
        """
        :param timer: The timer object
        :param project_name: This will be used as the file name inside the projects directory.
        """
        self.run_type = run_type
        self.run_name = run_name

        self.project_name = project_name + PROJECT_EXTENSION
        self.project_directory = os.path.expanduser(PYTOMATO_PROJECTS_DIR)

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
            self.past_entries = json.load(open(self.timer_pickle_file, 'r'))
            print(len(self.past_entries), "entries loaded in total.")
        else:
            self.past_entries = []

    def listEntries(self):
        """
        :param list_all_entires: List all of the entries regardless of when they were added.
        """

        # pretty format the entries
        pretty_entires = list(map(lambda entry: self.pretty_format(entry), self.past_entries))

        if pretty_entires:
            for i, e in enumerate(pretty_entires):
                print(i, "-", e)

    @staticmethod
    def pretty_format(entry):
        return "{} T:{} S: {} - {} elapsed: {}, target: {}min".format(
               entry["name"],
               entry["type"],
               entry["entry"]["entryStart"],
               entry["entry"]["entryEnd"][-8:],
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

    def add(self, start_datetime, end_datetime, elapsed_time, target_time):
        string_format = "%Y-%m-%dT%H:%M:%S"
        self.past_entries.append(
            {
                "name": self.run_name,
                "type": self.run_type,
                "entry":
                {
                    "entryStart": start_datetime.strftime(string_format),
                    "entryEnd": end_datetime.strftime(string_format),
                    "elapsedTime": elapsed_time,
                    "targetTime": target_time
                }
            }
        )

    def ensure_directory_exists(self):
        if not os.path.isdir(self.project_directory):
            os.mkdir(self.project_directory)

    def save(self, force_upload=False):
        self.ensure_directory_exists()
        # don't save in original file, save in a backup copy
        json.dump(self.past_entries, open(self.backup_timer_pickle_file, 'w'), indent=4)
        # then overwrite the original
        os.replace(self.backup_timer_pickle_file, self.timer_pickle_file)

        self.backup_entries(self.run_name, force_upload)

    def delete_entry(self, id):
        try:
            print("Removing entry", id, ":", self.pretty_format(self.past_entries[id]))
            del self.past_entries[id]

        except IndexError:
            print("Could not find entry. Nothing is changed")

    def backup_entries(self, name, force_upload):
        self.gh.upload("{} {}".format(name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), force_upload)
