import unittest
import mock
from pytomato.guitimer import GUITimer
from pytomato.run_parameters import RunParameters


class GUITimerTest(unittest.TestCase):
    def test_icon_found(self):
        """
        If this test fails, then the icon has been moved
        """
        try:
            GUITimer(RunParameters())
        except AssertionError:
            self.fail("The icon for the GUI timer was not found!")

    def setUp(self):
        self.guitimer = GUITimer(RunParameters())
        self.guitimer.systemtray_icon.hide = mock.MagicMock()
        self.guitimer.systemtray_icon.showMessage = mock.MagicMock()
        self.guitimer.systemtray_icon.setToolTip = mock.MagicMock()

    def test_close_event_hides_icon(self):
        self.guitimer.closeEvent()
        self.guitimer.systemtray_icon.hide.assert_called_once()

    def test_notify_user(self):
        self.guitimer.notifyUser()
        self.guitimer.systemtray_icon.showMessage.assert_called_once_with(
            self.guitimer.overtime_message, self.guitimer.notify_string, self.guitimer.icon)

    def test_update_visuals(self):
        self.guitimer.updateVisuals(1, 3, "33")
        self.guitimer.systemtray_icon.setToolTip.assert_called_once()


if __name__ == '__main__':
    unittest.main()
