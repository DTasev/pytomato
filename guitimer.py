import sys

from PyQt5 import Qt

import timer


class GUITimer(timer.Timer):
    def __init__(self):
        super().__init__()
        self.app = Qt.QApplication(sys.argv)

    def notifyUser(self, elapsedTime, targetTime):
        systemtray_icon = Qt.QSystemTrayIcon(self.app)
        systemtray_icon.show()
        systemtray_icon.showMessage('Going Overtime!', self.notifyString, Qt.QSystemTrayIcon.Warning)
