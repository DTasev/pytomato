import sys

from PyQt5 import Qt

from pytomato import timer


class GUITimer(timer.Timer):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.app = Qt.QApplication(sys.argv)
        pixmap = Qt.QPixmap("pytomato/tomato.png")
        assert not pixmap.isNull(), "The icon specified was not found!"
        self.icon = Qt.QIcon(pixmap) 
        self.systemtray_icon = Qt.QSystemTrayIcon(self.icon, self.app)
        self.systemtray_icon.show()

    def notifyUser(self):
        self.systemtray_icon.showMessage('Going Overtime!', self.notifyString, self.icon)
