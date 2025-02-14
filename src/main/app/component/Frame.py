from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout


class Frame(QFrame):
    def __init__(self, text:str, widget:QWidget, parent=None):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(widget, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text)
