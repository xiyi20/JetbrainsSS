from PyQt6.QtCore import pyqtSignal, QTimer, Qt
from qfluentwidgets import LineEdit


# noinspection PyUnresolvedReferences
class FLineEdit(LineEdit):
    focusOut = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.onLongPress)
        self.pressed = False
        self.threshold = 1000

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if self.pressed:
            self.pressed = False
            return
        self.focusOut.emit()

    def contextMenuEvent(self, event):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.pressed = True
            self.timer.start(self.threshold)
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
            self.pressed = False
            return
        super().mouseReleaseEvent(event)

    def onLongPress(self):
        if self.pressed:
            self.focusOut.emit()
            self.pressed = False
            self.timer.stop()
