import os
import sys

from PyQt5 import Qt

from pytomato import timer


class GUITimer(timer.Timer):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.app = Qt.QApplication(sys.argv)
        icon_path = os.path.abspath(os.path.join(sys.path[0], "pytomato/assets/tomato.png"))
        pixmap = Qt.QPixmap(icon_path)
        assert not pixmap.isNull(), "The icon specified was not found!"
        self.icon = Qt.QIcon(pixmap)
        self.systemtray_icon = Qt.QSystemTrayIcon(self.icon, self.app)
        self.systemtray_icon.show()
        self.overtime_message = 'Going Overtime!'

    def closeEvent(self):
        # hide the tray icon
        self.systemtray_icon.hide()

    def notifyUser(self):
        self.systemtray_icon.showMessage(self.overtime_message, self.notify_string, self.icon)

    def updateVisuals(self, elapsedTime, targetTime, targteTimeString):
        # update the CLI
        cli_string = super().updateVisuals(elapsedTime, targetTime, targteTimeString)
        # update the GUI
        self.systemtray_icon.setToolTip(cli_string)
