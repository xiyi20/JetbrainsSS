from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import PrimaryPushButton, BodyLabel, LineEdit

from src.main.app.common.PathTool import PathTool
from src.main.app.common.RwConfig import RwConfig
from src.main.app.component.OptionWidget import OptionWidget


class IDEWidget(QWidget):
    def __init__(self, IDE:Enum, pathTool: PathTool):
        super().__init__()
        self.config = RwConfig().config
        self.IDE = IDE
        self.pathTool = pathTool
        self.layout = QVBoxLayout(self)
        self.panel = OptionWidget(IDE)
        self.contentLayout = QHBoxLayout()
        self.label = BodyLabel()
        self.label.setText(f"{IDE.name}路径:")
        self.label.setFixedWidth(95)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path = LineEdit()
        self.path.setFixedWidth(300)
        self.path.setClearButtonEnabled(True)
        self.path.editingFinished.connect(
            lambda: pathTool.checkPath(self.path.text(), IDE.name, self.panel)
            if RwConfig().config["IDE"][IDE.name]["path"] != self.path.text() else None
        )
        self.ideaButton = PrimaryPushButton("选择", self)
        self.ideaButton.clicked.connect(
            lambda: pathTool.getDirectory(IDE.name, self.path, self.panel)
        )
        self.contentLayout.addWidget(self.label)
        self.contentLayout.addWidget(self.path)
        self.contentLayout.addWidget(self.ideaButton)
        self.layout.addLayout(self.contentLayout)
        self.layout.addWidget(self.panel)

        self.loadConfig()

    def loadConfig(self):
        path:str = self.config["IDE"][self.IDE.name]["path"]
        if path:
            self.path.setText(path)
            self.panel.setVisible(True)

