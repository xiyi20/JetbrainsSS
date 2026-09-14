from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import BodyLabel, CaptionLabel, PrimaryPushButton, PushButton, ProgressBar, qconfig

from src.main.app.common.JarEditor import JarEditor
from src.main.app.common.AppTheme import separatorStyle
from src.main.app.component.FLineEdit import FLineEdit
from src.main.app.component.PressButton import PressButton


class OptionWidget(QWidget):
    def __init__(self, IDE: Enum, pathTool, config: {}, parent):
        super().__init__()
        self.setVisible(False)
        self.IDE = IDE
        self.config = config['IDE']
        self.progressBar = ProgressBar(self)
        self.parent = parent
        baseDir: str = self.config[self.IDE.name]["path"]
        version: str = self.config[self.IDE.name]["version"][:4]
        self.pathTool = pathTool
        self.jarEditor = None if not baseDir else JarEditor(self.IDE, baseDir, version, self.progressBar, self.parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)

        # 与安装路径行之间的分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet(separatorStyle())
        self.separator.setFixedHeight(1)
        self.layout.addWidget(self.separator)

        self.tipLabel = CaptionLabel("启动图需与指定尺寸完全一致, 否则无法修补")
        self.layout.addWidget(self.tipLabel)

        self.topLayout = QHBoxLayout()
        self.topLayout.setSpacing(8)
        self.splashLabel1 = BodyLabel()
        self.splashLabel1.setText("启动图1:")
        self.splashPath1 = FLineEdit()
        self.splashPath1.setPlaceholderText("640*400px")
        self.splashPath1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.splashPath1.focusOut.connect(
            lambda: self.checkPath(self.splashPath1, self.splashPath2, "splash1", self.splashPath1.text(),
                                   self.modButton)
        )
        self.splashButton1 = PressButton("选择", self)
        self.splashButton1.clicked.connect(
            lambda: pathTool.getSplashPath(self.IDE.name, "splash1(640*400px)", self.splashPath1, self.splashPath2,
                                           self.modButton)
        )
        self.splashButton1.pressed.connect(
            lambda: pathTool.unlockLabel(self.splashPath1, self.modButton)
        )
        self.splashLabel1.setFixedWidth(70)
        self.splashButton1.setFixedWidth(64)
        self.topLayout.addWidget(self.splashLabel1)
        self.topLayout.addWidget(self.splashPath1, 1)
        self.topLayout.addWidget(self.splashButton1)
        self.layout.addLayout(self.topLayout)

        self.centerLayout = QHBoxLayout()
        self.centerLayout.setSpacing(8)
        self.splashLabel2 = BodyLabel()
        self.splashLabel2.setText("启动图2:")
        self.splashPath2 = FLineEdit()
        self.splashPath2.setPlaceholderText("1280*800px")
        self.splashPath2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.splashPath2.focusOut.connect(
            lambda: self.checkPath(self.splashPath2, self.splashPath1, "splash2", self.splashPath2.text(),
                                   self.modButton)
        )
        self.splashButton2 = PressButton("选择", self)
        self.splashButton2.clicked.connect(
            lambda: pathTool.getSplashPath(self.IDE.name, "splash2(1280*800px)", self.splashPath2, self.splashPath1,
                                           self.modButton)
        )
        self.splashButton2.pressed.connect(
            lambda: pathTool.unlockLabel(self.splashPath2, self.modButton)
        )
        self.splashLabel2.setFixedWidth(70)
        self.splashButton2.setFixedWidth(64)
        self.centerLayout.addWidget(self.splashLabel2)
        self.centerLayout.addWidget(self.splashPath2, 1)
        self.centerLayout.addWidget(self.splashButton2)
        self.layout.addLayout(self.centerLayout)

        self.bottomLayout = QHBoxLayout()
        self.modButton = PrimaryPushButton("开始修补", self)
        self.modButton.setEnabled(False)
        self.modButton.clicked.connect(
            lambda: self.jarEditor.edit([self.modButton, self.restoreButton],
                                        [self.splashPath1.text(), self.splashPath2.text()])
        )
        self.restoreButton = PushButton("还原", self)
        self.restoreButton.clicked.connect(
            lambda: self.jarEditor.restore(True, True, [self.modButton, self.restoreButton])
        )
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.restoreButton)
        self.bottomLayout.addWidget(self.modButton)
        self.layout.addLayout(self.bottomLayout)

        self.progressBar.setVisible(False)
        self.layout.addWidget(self.progressBar)
        qconfig.themeChangedFinished.connect(lambda: self.separator.setStyleSheet(separatorStyle()))
        self.loadConfig()

    def checkPath(self, splashPath: FLineEdit, checkPath: FLineEdit, splashName: str, path: str,
                  button: PrimaryPushButton):
        if self.splashPath2.text():
            self.pathTool.checkSplashPath(self.IDE.name, splashPath, checkPath, splashName, path, button)
        else:
            self.modButton.setEnabled(False)

    def initJarEditor(self, baseDir: str, version: str):
        self.jarEditor = JarEditor(self.IDE, baseDir, version, self.progressBar, self.parent)

    def loadConfig(self):
        splash = {"splash1": self.splashPath1, "splash2": self.splashPath2}
        check = 0
        for logo in splash.keys():
            path: str = self.config[self.IDE.name][logo]
            if path:
                splash[logo].setText(path)
                splash[logo].setEnabled(False)
                check += 1
        if check == 2:
            self.modButton.setEnabled(True)
