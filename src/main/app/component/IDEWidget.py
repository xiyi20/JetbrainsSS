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
        self.label = BodyLabel()
        self.label.setText(f"{IDE.name}路径:")
        self.label.setFixedWidth(95)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path = FLineEdit()
        self.path.setFixedWidth(300)
        self.path.setClearButtonEnabled(True)
        self.path.focusOut.connect(
            lambda: pathTool.checkIdePath(self.path.text(), IDE.name, self.path, self.panel)
            if self.path.text() else None
        )
        self.ideButton = PressButton("选择", self)
        self.ideButton.clicked.connect(
            lambda: pathTool.getIdeDirectory(IDE.name, self.path, self.panel)
        )
        self.ideButton.pressed.connect(
            lambda: pathTool.unlockLabel(self.path)
        )
        self.contentLayout.addWidget(self.label)
        self.contentLayout.addWidget(self.path)
        self.contentLayout.addWidget(self.ideButton)
        self.layout.addLayout(self.contentLayout)
        self.layout.addWidget(self.panel)

        self.loadConfig()

    def loadConfig(self):
        path: str = self.config["IDE"][self.IDE.name]["path"]
        if path:
            self.path.setText(path)
            self.path.setEnabled(False)
            self.panel.setVisible(True)
