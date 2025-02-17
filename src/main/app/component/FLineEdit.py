from PyQt6.QtCore import pyqtSignal
from qfluentwidgets import LineEdit


# noinspection PyUnresolvedReferences
class FLineEdit(LineEdit):
    focusOut = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focusOut.emit()
