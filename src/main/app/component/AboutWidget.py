import sys
import webbrowser
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import TitleLabel, CaptionLabel, PushButton, FluentIcon, CardWidget

from src.main.app.common.RwConfig import RwConfig


def resourcesDir() -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            p = Path(meipass) / "src" / "main" / "resources"
            if p.exists():
                return p
        return Path(sys.executable).parent / "resources"
    return Path(__file__).resolve().parents[2] / "resources"


class AboutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

        self.card = CardWidget()
        cardLayout = QVBoxLayout(self.card)
        cardLayout.setContentsMargins(24, 24, 24, 24)
        cardLayout.setSpacing(8)

        self.logoLabel = QLabel()
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logoPath = resourcesDir() / "logo.png"
        if logoPath.exists():
            self.logoLabel.setPixmap(
                QPixmap(str(logoPath)).scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
            )
        cardLayout.addWidget(self.logoLabel)

        self.title = TitleLabel("JetbrainsSS")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(self.title)

        version = RwConfig().config.get("version", "")
        self.version = CaptionLabel(f"Version {version}" if version else "Version")
        self.version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLayout.addWidget(self.version)

        self.desc = CaptionLabel(
            "JetBrains IDE 启动图自定义工具\n"
            "支持 IntelliJ IDEA / PyCharm / WebStorm\n"
            "选择安装目录并上传指定尺寸的启动图,一键修补 IDE 的 splash 资源"
        )
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc.setWordWrap(True)
        cardLayout.addWidget(self.desc)

        self.githubButton = PushButton(FluentIcon.GITHUB, "GitHub 仓库")
        self.githubButton.clicked.connect(
            lambda: webbrowser.open("https://github.com/xiyi20/JetbrainsSS")
        )
        buttonRow = QHBoxLayout()
        buttonRow.addStretch(1)
        buttonRow.addWidget(self.githubButton)
        buttonRow.addStretch(1)
        cardLayout.addLayout(buttonRow)

        # 卡片随窗口宽度扩展, 顶部对齐不做垂直居中
        self.layout.addWidget(self.card)
        self.layout.addStretch(1)
