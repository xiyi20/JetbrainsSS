from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import BodyLabel, LineEdit, PrimaryPushButton


class OptionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setVisible(False)
        self.layout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.splashLabel1 = BodyLabel()
        self.splashLabel1.setText("启动图1:")
        self.splashPath1 = LineEdit()
        self.splashPath1.setPlaceholderText("640*400px")
        self.splashButton1 = PrimaryPushButton("选择", self)
        self.topLayout.addWidget(self.splashLabel1)
        self.topLayout.addWidget(self.splashPath1)
        self.topLayout.addWidget(self.splashButton1)
        self.layout.addLayout(self.topLayout)

        self.centerLayout = QHBoxLayout()
        self.splashLabel2 = BodyLabel()
        self.splashLabel2.setText("启动图2:")
        self.splashPath2 = LineEdit()
        self.splashPath2.setPlaceholderText("1280*800px")
        self.splashButton2 = PrimaryPushButton("选择", self)
        self.centerLayout.addWidget(self.splashLabel2)
        self.centerLayout.addWidget(self.splashPath2)
        self.centerLayout.addWidget(self.splashButton2)
        self.layout.addLayout(self.centerLayout)

        self.bottomLayout = QHBoxLayout()
        self.modButton = PrimaryPushButton("开始修补", self)
        self.modButton.clicked.connect(lambda: print(111))
        self.restoreButton = PrimaryPushButton("还原", self)
        self.bottomLayout.addWidget(self.modButton)
        self.bottomLayout.addWidget(self.restoreButton)
        self.layout.addLayout(self.bottomLayout)