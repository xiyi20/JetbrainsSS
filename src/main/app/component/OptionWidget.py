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
        self.patchEnabled = version in self.IDE.value
        self.jarEditor = None
        if baseDir and self.patchEnabled:
            self.jarEditor = JarEditor(self.IDE, baseDir, version, self.progressBar, self.parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        # 与卡片的安装路径行共用同一内容列, 保证标签/按钮对齐
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 与安装路径行之间的分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet(separatorStyle())
        self.separator.setFixedHeight(1)
        self.layout.addWidget(self.separator)

        self.topLayout = QHBoxLayout()
        self.topLayout.setSpacing(5)
        self.splashLabel1 = BodyLabel()
        self.splashLabel1.setText("启动图1")
        self.splashLabel1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.splashPath = FLineEdit()
        self.splashPath.setPlaceholderText("640*400px")
        self.splashPath.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.splashPath.focusOut.connect(
            lambda: self.checkPath(self.splashPath, self.splashPath2x, "splash", self.splashPath.text(),
                                   self.modButton)
        )
        self.splashButton1 = PressButton("选择", self)
        self.splashButton1.clicked.connect(
            lambda: self.selectSplash("splash(640*400px)", self.splashPath, self.splashPath2x, self.modButton)
        )
        self.splashButton1.pressed.connect(
            lambda: pathTool.unlockLabel(self.splashPath, self.modButton)
        )
        self.splashLabel1.setFixedWidth(70)
        self.splashButton1.setFixedWidth(64)
        self.topLayout.addWidget(self.splashLabel1)
        self.topLayout.addWidget(self.splashPath, 1)
        self.topLayout.addSpacing(8)
        self.topLayout.addWidget(self.splashButton1)
        self.layout.addLayout(self.topLayout)

        self.centerLayout = QHBoxLayout()
        self.centerLayout.setSpacing(5)
        self.splashLabel2 = BodyLabel()
        self.splashLabel2.setText("启动图2")
        self.splashLabel2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.splashPath2x = FLineEdit()
        self.splashPath2x.setPlaceholderText("1280*800px")
        self.splashPath2x.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.splashPath2x.focusOut.connect(
            lambda: self.checkPath(self.splashPath2x, self.splashPath, "splash@2x", self.splashPath2x.text(),
                                   self.modButton)
        )
        self.splashButton2 = PressButton("选择", self)
        self.splashButton2.clicked.connect(
            lambda: self.selectSplash("splash@2x(1280*800px)", self.splashPath2x, self.splashPath, self.modButton)
        )
        self.splashButton2.pressed.connect(
            lambda: pathTool.unlockLabel(self.splashPath2x, self.modButton)
        )
        self.splashLabel2.setFixedWidth(70)
        self.splashButton2.setFixedWidth(64)
        self.centerLayout.addWidget(self.splashLabel2)
        self.centerLayout.addWidget(self.splashPath2x, 1)
        self.centerLayout.addSpacing(8)
        self.centerLayout.addWidget(self.splashButton2)
        self.layout.addLayout(self.centerLayout)

        self.bottomLayout = QHBoxLayout()
        self.modButton = PrimaryPushButton("开始修补", self)
        self.modButton.setEnabled(False)
        self.modButton.clicked.connect(
            lambda: self.jarEditor.edit([self.modButton, self.restoreButton],
                                        [self.splashPath.text(), self.splashPath2x.text()])
        )
        self.restoreButton = PushButton("还原", self)
        self.restoreButton.clicked.connect(
            lambda: self.jarEditor.restore(True, True, [self.modButton, self.restoreButton])
        )
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.restoreButton)
        self.bottomLayout.addWidget(self.modButton)
        self.layout.addLayout(self.bottomLayout)

        # 进度条放入固定高度容器: 容器始终占位, 进度条显隐不再改变卡片高度
        self.progressHolder = QWidget()
        self.progressHolder.setFixedHeight(self.progressBar.height())
        holderLayout = QVBoxLayout(self.progressHolder)
        holderLayout.setContentsMargins(0, 0, 0, 0)
        holderLayout.addWidget(self.progressBar)
        self.layout.addWidget(self.progressHolder)
        # 必须在加入布局后隐藏, 否则父窗口 show 时会覆盖隐藏状态
        self.progressBar.setVisible(False)
        qconfig.themeChangedFinished.connect(lambda: self.separator.setStyleSheet(separatorStyle()))
        self.loadConfig()

    def selectSplash(self, splash: str, targetLabel: FLineEdit, checkLabel: FLineEdit, button: PrimaryPushButton):
        if not self.patchEnabled:
            return
        self.pathTool.getSplashPath(self.IDE.name, splash, targetLabel, checkLabel, button)

    def setPatchEnabled(self, enabled: bool):
        """版本不支持修补时禁用[开始修补]与[还原](无 jarEditor 可操作)。"""
        self.patchEnabled = enabled
        if enabled:
            self.restoreButton.setEnabled(True)
            self.modButton.setEnabled(bool(self.splashPath.text() and self.splashPath2x.text()))
        else:
            self.modButton.setEnabled(False)
            self.restoreButton.setEnabled(False)

    def checkPath(self, splashPath: FLineEdit, checkPath: FLineEdit, splashName: str, path: str,
                  button: PrimaryPushButton):
        if not self.patchEnabled:
            self.modButton.setEnabled(False)
        elif self.splashPath2x.text():
            self.pathTool.checkSplashPath(self.IDE.name, splashPath, checkPath, splashName, path, button)
        else:
            self.modButton.setEnabled(False)

    def initJarEditor(self, baseDir: str, version: str):
        self.jarEditor = JarEditor(self.IDE, baseDir, version, self.progressBar, self.parent)

    def loadConfig(self):
        splash = {"splash": self.splashPath, "splash@2x": self.splashPath2x}
        check = 0
        for logo in splash.keys():
            path: str = self.config[self.IDE.name][logo]
            if path:
                splash[logo].setText(path)
                splash[logo].setEnabled(False)
                check += 1
        if check == 2 and self.patchEnabled:
            self.modButton.setEnabled(True)
