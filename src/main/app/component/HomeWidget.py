from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import TitleLabel, VBoxLayout

from src.main.app.common.PathTool import PathTool
from src.main.app.component.IdeaWidget import IdeaWidget
from src.main.app.component.PycharmWidget import PycharmWidget
from src.main.app.component.WebstormWidget import WebstormWidget


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pathTool = PathTool(self)
        self.layout = VBoxLayout(self)

        self.tittle = TitleLabel()
        self.tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tittle.setText("欢迎使用JetbrainsSS")

        self.layout.addWidget(self.tittle)
        self.layout.addWidget(IdeaWidget(self.pathTool))
        self.layout.addWidget(PycharmWidget(self.pathTool))
        self.layout.addWidget(WebstormWidget(self.pathTool))
