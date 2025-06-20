from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel

from src.main.app.common.PathTool import PathTool
from src.main.app.common.RwConfig import RwConfig
from src.main.app.component.FLineEdit import FLineEdit
from src.main.app.component.OptionWidget import OptionWidget
from src.main.app.component.PressButton import PressButton


class IDEWidget(QWidget):
    def __init__(self, IDE: Enum, pathTool: PathTool, parent):
        super().__init__()
        self.config = RwConfig().config
        self.IDE = IDE
        self.pathTool = pathTool
        self.layout = QVBoxLayout(self)
        self.panel = OptionWidget(IDE, self.pathTool, self.config, parent)
        self.contentLayout = QHBoxLayout()
        self.ideName = BodyLabel()
        self.ideName.setText(f"{IDE.name}路径:")
        self.ideName.setFixedWidth(95)
        self.ideName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.idePath = FLineEdit()
        self.idePath.setFixedWidth(230)
        self.idePath.setClearButtonEnabled(True)
        self.idePath.focusOut.connect(
            lambda: pathTool.checkIdePath(self.idePath.text(), IDE.name, self.idePath, self.ideVersion, self.panel)
            if self.idePath.text() else None
        )
        self.ideButton = PressButton("选择", self)
        self.ideButton.clicked.connect(
            lambda: pathTool.getIdeDirectory(IDE.name, self.idePath, self.ideVersion, self.panel)
        )
        self.ideButton.pressed.connect(
            lambda: pathTool.unlockLabel(self.idePath)
        )
        self.ideVersion = BodyLabel()
        self.ideVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ideVersion.setStyleSheet(
            "background-color: orange;"
            "border-radius: 6px;"
            "font-weight: bold"
        )
        self.ideVersion.setFixedWidth(50)
        self.contentLayout.addWidget(self.ideName)
        self.contentLayout.addWidget(self.idePath)
        self.contentLayout.addWidget(self.ideVersion)
        self.contentLayout.addWidget(self.ideButton)
        self.layout.addLayout(self.contentLayout)
        self.layout.addWidget(self.panel)

        self.loadConfig()

    def loadConfig(self):
        path: str = self.config["IDE"][self.IDE.name]["path"]
        version: str = self.config["IDE"][self.IDE.name]["version"]
        if path:
            self.idePath.setText(path)
            self.idePath.setEnabled(False)
            self.ideVersion.setText(version)
            self.panel.setVisible(True)
