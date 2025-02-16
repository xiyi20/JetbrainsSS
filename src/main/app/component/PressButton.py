from PyQt6.QtCore import QTimer, pyqtSignal
from qfluentwidgets import PrimaryPushButton


# noinspection PyUnresolvedReferences
class PressButton(PrimaryPushButton):
    clicked = pyqtSignal()
    pressed = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.timer = QTimer()
        self.timer.timeout.connect(self.onLongPress)
        self.pressTime = 0
        self.threshold = 1000

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressTime = 0
        self.timer.start(100)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.timer.stop()
        if self.pressTime < self.threshold:
            self.clicked.emit()

    def onLongPress(self):
        self.pressTime += 100
        if self.pressTime > self.threshold:
            self.pressed.emit()
            self.timer.stop()