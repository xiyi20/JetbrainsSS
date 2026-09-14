from PyQt6.QtGui import QGuiApplication, QIcon
from qfluentwidgets import FluentIcon as FI, FluentWindow

from src.main.app.component.AboutWidget import AboutWidget
from src.main.app.component.Frame import Frame
from src.main.app.component.HomeWidget import HomeWidget


class MainWindow(FluentWindow):
    def __init__(self, logo: QIcon):
        super().__init__()
        self.logo = logo
        self.screen = QGuiApplication.primaryScreen().size()
        self.homeWidgets = HomeWidget(self)
        self.homeInterface = Frame('主页', self.homeWidgets, self)
        self.aboutWidgets = AboutWidget(self)
        self.aboutInterface = Frame('关于', self.aboutWidgets, self)
        self.initUI()

    def initUI(self):
        # 响应式: 允许自由缩放, 限制最小尺寸防止内容挤压
        self.setMinimumSize(520, 480)
        self.resize(600, 700)
        self.move(self.screen.width() // 2 - self.width() // 2, self.screen.height() // 2 - self.height() // 2)
        self.setWindowTitle('JetbrainsSS')
        self.setWindowIcon(self.logo)
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FI.HOME, '主页')
        self.addSubInterface(self.aboutInterface, FI.INFO, '关于')
