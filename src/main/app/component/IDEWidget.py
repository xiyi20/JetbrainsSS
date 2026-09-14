import sys
from enum import Enum
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import CardWidget, StrongBodyLabel, BodyLabel, CaptionLabel, qconfig

from src.main.app.common.PathTool import PathTool
from src.main.app.common.RwConfig import RwConfig
from src.main.app.common.AppTheme import versionBadgeStyle
from src.main.app.component.FLineEdit import FLineEdit
from src.main.app.component.OptionWidget import OptionWidget
from src.main.app.component.PressButton import PressButton


def imagesDir() -> Path:
    """Locate src/main/resources/images in both dev and PyInstaller modes."""
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            p = Path(meipass) / "src" / "main" / "resources" / "images"
            if p.exists():
                return p
        return Path(sys.executable).parent / "resources" / "images"
    return Path(__file__).resolve().parents[2] / "resources" / "images"


IDE_DISPLAY_NAMES = {"Idea": "IntelliJ IDEA", "PyCharm": "PyCharm", "WebStorm": "WebStorm"}
IDE_LOGOS = {"Idea": "idea_logo.png", "PyCharm": "pycharm_logo.png", "WebStorm": "webide_logo.png"}


class IDEWidget(CardWidget):
    def __init__(self, IDE: Enum, pathTool: PathTool, parent):
        super().__init__(parent)
        self.config = RwConfig().config
        self.IDE = IDE
        self.pathTool = pathTool
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 12)
        self.layout.setSpacing(8)
        self.panel = OptionWidget(IDE, self.pathTool, self.config, parent)

        # header: IDE logo + name + version badge
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(8)
        self.ideIcon = QLabel()
        self.ideIcon.setFixedSize(32, 32)
        logoPath = imagesDir() / IDE_LOGOS[IDE.name]
        if logoPath.exists():
            self.ideIcon.setPixmap(
                QPixmap(str(logoPath)).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
            )
        self.ideName = StrongBodyLabel(IDE_DISPLAY_NAMES.get(IDE.name, IDE.name))
        self.ideVersion = CaptionLabel()
        self.ideVersion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ideVersion.setFixedWidth(52)
        self.ideVersion.setVisible(False)
        self.ideVersion.setStyleSheet(versionBadgeStyle())
        self.headerLayout.addWidget(self.ideIcon)
        self.headerLayout.addWidget(self.ideName)
        self.headerLayout.addStretch(1)
        self.headerLayout.addWidget(self.ideVersion)
        self.layout.addLayout(self.headerLayout)

        # path row
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(8)
        self.pathLabel = BodyLabel("安装路径:")
        self.pathLabel.setFixedWidth(70)
        self.idePath = FLineEdit()
        self.idePath.setMinimumWidth(200)
        self.idePath.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.idePath.setClearButtonEnabled(True)
        self.idePath.focusOut.connect(
            lambda: pathTool.checkIdePath(self.idePath.text(), IDE.name, self.idePath, self.ideVersion, self.panel)
            if self.idePath.text() else None
            )
        self.ideButton = PressButton("选择", self)
        self.ideButton.setFixedWidth(64)
        self.ideButton.clicked.connect(
            lambda: pathTool.getIdeDirectory(IDE.name, self.idePath, self.ideVersion, self.panel)
        )
        self.ideButton.pressed.connect(
            lambda: pathTool.unlockLabel(self.idePath)
        )
        self.contentLayout.addWidget(self.pathLabel)
        self.contentLayout.addWidget(self.idePath, 1)
        self.contentLayout.addWidget(self.ideButton)
        self.layout.addLayout(self.contentLayout)

        self.layout.addWidget(self.panel)

        qconfig.themeChangedFinished.connect(lambda: self.ideVersion.setStyleSheet(versionBadgeStyle()))

        self.loadConfig()

    def loadConfig(self):
        path: str = self.config["IDE"][self.IDE.name]["path"]
        version: str = self.config["IDE"][self.IDE.name]["version"]
        if path:
            self.idePath.setText(path)
            self.idePath.setEnabled(False)
            if version:
                self.ideVersion.setText(f"v{version}")
                self.ideVersion.setVisible(True)
            self.panel.setVisible(True)
