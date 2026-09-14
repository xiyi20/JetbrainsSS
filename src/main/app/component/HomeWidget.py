from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import TitleLabel, CaptionLabel, ScrollArea, VBoxLayout, qconfig

from src.main.app.common.PathTool import PathTool
from src.main.app.common.RwConfig import RwConfig
from src.main.app.common.AppTheme import warningBannerStyle
from src.main.app.component.IdeaWidget import IdeaWidget
from src.main.app.component.PycharmWidget import PycharmWidget
from src.main.app.component.WebstormWidget import WebstormWidget


class HomeWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self.pathTool = PathTool(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(self.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.wrapper = QWidget()
        self.wrapperLayout = QHBoxLayout(self.wrapper)
        self.wrapperLayout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setMaximumWidth(720)
        self.layout = VBoxLayout(container)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

        self.tittle = TitleLabel("欢迎使用 JetbrainsSS")
        self.tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle = CaptionLabel("自定义 JetBrains IDE 启动图 · 选择安装目录后开始修补")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 修补后的 jar 会导致 IDE 更新校验失败, 只要有任意 IDE 绑定就显示
        self.warningLabel = CaptionLabel("⚠ 更新 IDE 前请先点击[还原]撤销修补, 否则会导致更新校验失败")
        self.warningLabel.setStyleSheet(warningBannerStyle())
        self.warningLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warningLabel.setWordWrap(True)

        self.layout.addWidget(self.tittle)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.warningLabel)
        self.layout.addSpacing(4)
        self.layout.addWidget(IdeaWidget(self.pathTool, parent))
        self.layout.addWidget(PycharmWidget(self.pathTool, parent))
        self.layout.addWidget(WebstormWidget(self.pathTool, parent))
        self.layout.addStretch(1)

        # 容器随窗口扩展, 超过 720px 后由 resizeEvent 中的动态边距使其居中
        self.wrapperLayout.addWidget(container)

        self.setWidget(self.wrapper)

        self.pathTool.onBindingChanged = self.refreshWarning
        self.refreshWarning()
        qconfig.themeChangedFinished.connect(self.refreshWarning)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 视口宽度超过内容上限时, 用对称边距实现居中
        margin = max(0, (self.viewport().width() - 720) // 2)
        self.wrapperLayout.setContentsMargins(margin, 0, margin, 0)

    def refreshWarning(self):
        self.warningLabel.setStyleSheet(warningBannerStyle())
        config = RwConfig().config["IDE"]
        bound = any(config[ide]["path"] for ide in config)
        self.warningLabel.setVisible(bound)
