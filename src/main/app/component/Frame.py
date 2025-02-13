from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout


class Frame(QFrame):
    def __init__(self, text:str, widgets:QWidget, parent=None):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(widgets, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text)
