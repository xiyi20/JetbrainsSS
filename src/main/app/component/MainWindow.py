from qfluentwidgets import FluentIcon as FI, FluentWindow

from src.main.app.component.Frame import Frame
from src.main.app.component.HomeWidget import HomeWidget


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.homeWidgets = HomeWidget(self)
        self.homeInterface = Frame('主页', self.homeWidgets, self)
        self.initUI()

    def initUI(self):
        self.resize(650, 550)
        self.setWindowTitle('JetbrainsSS')
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FI.HOME, '主页')

