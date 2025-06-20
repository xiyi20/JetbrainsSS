import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

import common.Icon
from src.main.app.component.MainWindow import MainWindow

appid = 'com.xiyi.JetbrainsSS'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
common.Icon.init()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(QIcon(':/logo.ico'))
    window.show()
    app.exec()
