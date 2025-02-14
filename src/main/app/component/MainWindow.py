from PyQt6.QtGui import QGuiApplication
from qfluentwidgets import FluentIcon as FI, FluentWindow

from src.main.app.component.Frame import Frame
from src.main.app.component.HomeWidget import HomeWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.screen = QGuiApplication.primaryScreen().size()
        self.homeWidgets = HomeWidget()
        self.homeInterface = Frame('主页', self.homeWidgets, self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(650, 700)
        self.move(self.screen.width()//2 - self.width()//2,self.screen.height()//2 - self.height()//2)
        self.setWindowTitle('JetbrainsSS')
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FI.HOME, '主页')

