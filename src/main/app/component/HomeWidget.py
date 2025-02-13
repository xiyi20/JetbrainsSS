import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from qfluentwidgets import PrimaryPushButton, LineEdit, BodyLabel, TitleLabel, InfoBar, InfoBarPosition
from src.main.app.common.JarPath import JarPath
from src.main.app.common.RwConfig import RwConfig


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(parent.size())
        self.parent = parent
        self.layout = QVBoxLayout()

        self.centerLayout = QVBoxLayout()
        self.tittle = TitleLabel()
        self.tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tittle.setText("请选择IDE的安装路径")
        self.layout.addWidget(self.tittle)

        self.centerLayout1 = QHBoxLayout()

        self.ideaLabel = BodyLabel()
        self.ideaLabel.setText(f"{JarPath.IDEA.name}路径:")
        self.ideaLabel.setMinimumSize(95,0)
        self.ideaLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ideaPath = LineEdit()
        self.ideaPath.setMinimumSize(350, 10)
        self.ideaPath.setClearButtonEnabled(True)
        self.ideaPath.editingFinished.connect(
            lambda: self.checkPath(self.ideaPath.text(), JarPath.IDEA.name)
            if RwConfig().config["Path"][JarPath.IDEA.name] != self.ideaPath.text() else None
        )
        self.ideaButton = PrimaryPushButton("选择", self)
        self.ideaButton.clicked.connect(lambda: self.getDirectory(JarPath.IDEA.name, self.ideaPath))
        self.centerLayout1.addWidget(self.ideaLabel)
        self.centerLayout1.addWidget(self.ideaPath)
        self.centerLayout1.addWidget(self.ideaButton)

        self.centerLayout2 = QHBoxLayout()
        self.pycharmLabel = BodyLabel()
        self.pycharmLabel.setMinimumSize(95,0)
        self.pycharmLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pycharmLabel.setText(f"{JarPath.PyCharm.name}路径:")
        self.pycharmPath = LineEdit()
        self.pycharmPath.setMinimumSize(350, 10)
        self.pycharmPath.setClearButtonEnabled(True)
        self.pycharmPath.editingFinished.connect(
            lambda: self.checkPath(self.pycharmPath.text(), JarPath.PyCharm.name)
            if RwConfig().config["Path"][JarPath.PyCharm.name] != self.pycharmPath.text() else None
        )
        self.pycharmButton = PrimaryPushButton("选择", self)
        self.pycharmButton.clicked.connect(lambda: self.getDirectory(JarPath.PyCharm.name, self.pycharmPath))
        self.centerLayout2.addWidget(self.pycharmLabel)
        self.centerLayout2.addWidget(self.pycharmPath)
        self.centerLayout2.addWidget(self.pycharmButton)

        self.centerLayout3 = QHBoxLayout()
        self.webstormLabel = BodyLabel()
        self.webstormLabel.setMinimumSize(95,0)
        self.webstormLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.webstormLabel.setText(f"{JarPath.WebStorm.name}路径:")
        self.webstormPath = LineEdit()
        self.webstormPath.setMinimumSize(350, 10)
        self.webstormPath.setClearButtonEnabled(True)
        self.webstormPath.editingFinished.connect(
            lambda: self.checkPath(self.webstormPath.text(), JarPath.WebStorm.name)
            if RwConfig().config["Path"][JarPath.WebStorm.name] != self.webstormPath.text() else None
        )
        self.webstormButton = PrimaryPushButton("选择", self)
        self.webstormButton.clicked.connect(lambda: self.getDirectory(JarPath.WebStorm.name, self.webstormPath))
        self.centerLayout3.addWidget(self.webstormLabel)
        self.centerLayout3.addWidget(self.webstormPath)
        self.centerLayout3.addWidget(self.webstormButton)

        self.centerLayout.addLayout(self.centerLayout1)
        self.centerLayout.addStretch(1)
        self.centerLayout.addLayout(self.centerLayout2)
        self.centerLayout.addStretch(1)
        self.centerLayout.addLayout(self.centerLayout3)
        self.centerLayout.addStretch(3)
        self.layout.addLayout(self.centerLayout)

        self.setLayout(self.layout)

    def getDirectory(self, text: str, label: LineEdit):
        folder = QFileDialog.getExistingDirectory(None, f"选择{text}的目录")
        if folder and self.checkPath(folder, text):
            label.setText(folder)
            RwConfig().wConfig("Path", text, folder)
        else:
            RwConfig().wConfig("Path", text, "")

    def checkPath(self, folder: str, text: str):
        check_exe = False
        exe1 = f"{folder}/bin/{text.lower()}64.exe"
        exe2 = f"{folder}/bin/{text.lower()}32.exe"
        for exe in [exe1, exe2]:
            if os.path.exists(exe) and os.path.isfile(exe):
                check_exe = True
                break
        jar = f"{folder}{JarPath[text].value[:JarPath[text].value.index('.')+4]}"
        result = os.path.exists(jar) and os.path.isfile(jar) and check_exe
        if result:
            InfoBar.success(
                title=folder,
                content=f"该目录已被绑定为{text}的安装目录",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
        else:
            InfoBar.warning(
                title=folder,
                content=f"该目录不是有效的{text}安装目录",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
        return result
