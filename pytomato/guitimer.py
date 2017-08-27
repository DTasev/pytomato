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

    def closeEvent(self):
        # hide the tray icon
        self.systemtray_icon.hide()

    def notifyUser(self):
        self.systemtray_icon.showMessage('Going Overtime!', self.notifyString, self.icon)

    def updateVisuals(self, elapsedTime, targetTime, targteTimeString):
        # update the CLI 
        cli_string = super().updateVisuals(elapsedTime, targetTime, targteTimeString)
        # update the GUI
        self.systemtray_icon.setToolTip(cli_string)
