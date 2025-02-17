import os
import sys

from PyQt6.QtWidgets import QApplication

from src.main.app.component.MainWindow import MainWindow


# noinspection PyProtectedMember
def getResource(relativePath: str):
    base_path = f"{sys._MEIPASS}/src/main/" if getattr(sys, 'frozen', False) else "../"
    ret_path = os.path.join(base_path, relativePath)
    return ret_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    logo = getResource(os.path.join("resources/", "logo.ico"))
    window = MainWindow(logo)
    window.show()
    app.exec()
