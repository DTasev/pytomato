import unittest
import datetime
from pytomato.entries import Entries
import tempfile
from pytomato import conf
import os


class EntriesTest(unittest.TestCase):
    def setUp(self):
        conf.GIT_EXECUTABLE_PATH = ""
        with tempfile.NamedTemporaryFile() as f:
            conf.PYTOMATO_PROJECTS_DIR = os.path.dirname(f.name)

        self.entries = Entries("Test Run", "Testing", "test")
        self.entries.initialise()

    def tearDown(self):
        file = self.entries.timer_pickle_file
        if os.path.isfile(file):
            os.remove(file)

    def test_add(self):
        self.entries.add(
            datetime.datetime(2017, 11, 11, 11, 11),
            datetime.datetime(2017, 11, 11, 12, 11),
            3600,
            2000)

        assert len(self.entries.past_entries) == 1

    def test_add_many(self):
        self.entries.add(
            datetime.datetime(2017, 11, 11, 11, 11),
            datetime.datetime(2017, 11, 11, 12, 11),
            3600,
            2000)

        self.entries.add(
            datetime.datetime(2017, 11, 11, 12, 11),
            datetime.datetime(2017, 11, 11, 13, 11),
            3600,
            2000)

        print("len =", len(self.entries.past_entries))
        print("all entries =", self.entries)
        assert len(self.entries.past_entries) == 2

    def test_save_load(self):
        self.test_add_many()
        self.entries.save()

        self.entries = Entries("Test Run", "Testing", "test")
        self.entries.initialise()

        assert len(self.entries.past_entries) == 2


if __name__ == '__main__':
    unittest.main()
