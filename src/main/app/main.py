import ctypes
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import setThemeColor, setTheme, Theme

from src.main.app.common.AppTheme import APP_THEME_COLOR
from src.main.app.component.MainWindow import MainWindow


def logoPath() -> str:
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).parent / "resources" / "logo.ico")
    return str(Path(__file__).resolve().parents[1] / "resources" / "logo.ico")


appid = 'com.xiyi.JetbrainsSS'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    setThemeColor(APP_THEME_COLOR)
    window = MainWindow(QIcon(logoPath()))
    window.show()
    app.exec()
