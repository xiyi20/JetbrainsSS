from enum import Enum

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, PrimaryPushButton

from src.main.app.common.JarEditor import JarEditor
from src.main.app.common.PathTool import PathTool
from src.main.app.component.FLineEdit import FLineEdit
from src.main.app.component.PressButton import PressButton


class OptionWidget(QWidget):
    def __init__(self, IDE: Enum, pathTool: PathTool, config: {}):
        super().__init__()
        self.setVisible(False)
        self.IDE = IDE
        self.config = config
        self.baseDir = self.config["IDE"][IDE.name]["path"]
        self.layout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.splashLabel1 = BodyLabel()
        self.splashLabel1.setText("启动图1:")
        self.splashPath1 = FLineEdit()
        self.splashPath1.setPlaceholderText("640*400px")
        self.splashPath1.unfocused.connect(
            lambda: pathTool.checkSplashPath(IDE.name, self.splashPath1, "splash1", self.splashPath1.text())
            if self.splashPath1.text() else None
        )
        self.splashButton1 = PressButton("选择", self)
        self.splashButton1.clicked.connect(
            lambda: pathTool.getSplashPath(IDE.name, "splash1(640*400px)", self.splashPath1)
        )
        self.splashButton1.pressed.connect(
            lambda: self.splashPath1.setEnabled(True)
        )
        self.topLayout.addWidget(self.splashLabel1)
        self.topLayout.addWidget(self.splashPath1)
        self.topLayout.addWidget(self.splashButton1)
        self.layout.addLayout(self.topLayout)

        self.centerLayout = QHBoxLayout()
        self.splashLabel2 = BodyLabel()
        self.splashLabel2.setText("启动图2:")
        self.splashPath2 = FLineEdit()
        self.splashPath2.setPlaceholderText("1280*800px")
        self.splashPath2.unfocused.connect(
            lambda: pathTool.checkSplashPath(IDE.name, self.splashPath2, "splash2", self.splashPath2.text())
            if self.splashPath2.text() else None
        )
        self.splashButton2 = PressButton("选择", self)
        self.splashButton2.clicked.connect(
            lambda: pathTool.getSplashPath(IDE.name, "splash2(1280*800px)", self.splashPath2)
        )
        self.splashButton2.pressed.connect(
            lambda: self.splashPath2.setEnabled(True)
        )
        self.centerLayout.addWidget(self.splashLabel2)
        self.centerLayout.addWidget(self.splashPath2)
        self.centerLayout.addWidget(self.splashButton2)
        self.layout.addLayout(self.centerLayout)

        self.bottomLayout = QHBoxLayout()
        self.modButton = PrimaryPushButton("开始修补", self)
        self.modButton.clicked.connect(
            lambda: JarEditor.edit([self.splashPath1.text(), self.splashPath2.text()], self.baseDir, IDE)
        )
        self.restoreButton = PrimaryPushButton("还原", self)
        self.restoreButton.clicked.connect(
            lambda: JarEditor.restore(self.baseDir, IDE)
        )
        self.bottomLayout.addWidget(self.modButton)
        self.bottomLayout.addWidget(self.restoreButton)
        self.layout.addLayout(self.bottomLayout)

        self.loadConfig()

    def loadConfig(self):
        splash = {"splash1": self.splashPath1, "splash2": self.splashPath2}
        for logo in splash.keys():
            path: str = self.config["IDE"][self.IDE.name][logo]
            if path:
                splash[logo].setText(path)
                splash[logo].setEnabled(False)
