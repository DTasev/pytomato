import sys

from PyQt5 import Qt

from pytomato import timer


class GUITimer(timer.Timer):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.app = Qt.QApplication(sys.argv)

    def notifyUser(self):
        systemtray_icon = Qt.QSystemTrayIcon(self.app)
        systemtray_icon.show()
        systemtray_icon.showMessage('Going Overtime!', self.notifyString, Qt.QSystemTrayIcon.Warning)
