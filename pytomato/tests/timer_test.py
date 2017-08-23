import unittest
import mock
from pytomato.run_parameters import RunParameters
from pytomato.timer import Timer
from pytomato.entries import Entries

import sys
print(sys.path)


class TimerTest(unittest.TestCase):

    def test_clean(self):
        run_par = RunParameters()
        run_par.clean = True
        timer = Timer(run_par)
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock

        timer.run()
        entries_mock.clean.assert_called_once()

    def test_listAndExit(self):
        run_par = RunParameters()
        run_par.listAndExit = True
        timer = Timer(run_par)
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock

        timer.run()
        entries_mock.initialise.assert_called_once()
        entries_mock.listEntries.assert_called_once()

    def test_delete(self):
        run_par = RunParameters()
        run_par.delete = 0
        timer = Timer(run_par)
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock

        timer.run()
        entries_mock.deleteEntry.assert_called_once()
        entries_mock.listEntries.assert_called()
        entries_mock.save.assert_called_once()

    def test_run_exit_on_keyboard_interrupt(self):
        run_par = RunParameters()
        run_par.duration = 1
        timer = Timer(run_par)

        def fake_notify():
            raise KeyboardInterrupt()

        timer.notify = fake_notify
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock
        update_visuals_mock = mock.Mock()
        timer.updateVisuals = update_visuals_mock
        timer.run()

        update_visuals_mock.assert_called_once()
        entries_mock.add.assert_called_once()
        entries_mock.save.assert_called_once()

    def test_run_number_of_calls_to_update_visuals(self):
        run_par = RunParameters()
        run_par.duration = 2
        timer = Timer(run_par)

        def fake_notify():
            raise KeyboardInterrupt()

        timer.notify = fake_notify
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock
        update_visuals_mock = mock.Mock()
        timer.updateVisuals = update_visuals_mock
        timer.run()

        self.assertEqual(len(update_visuals_mock.mock_calls), 2)
        entries_mock.add.assert_called_once()
        entries_mock.save.assert_called_once()

    def test_run_exit_on_system_exit(self):
        run_par = RunParameters()
        run_par.duration = 1
        timer = Timer(run_par)

        def fake_notify():
            raise SystemExit()

        timer.notify = fake_notify
        entries_mock = mock.create_autospec(Entries)
        timer.entries = entries_mock
        update_visuals_mock = mock.Mock()
        timer.updateVisuals = update_visuals_mock
        timer.run()

        update_visuals_mock.assert_called_once()
        entries_mock.add.assert_called_once()
        entries_mock.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
