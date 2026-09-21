import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QFileDialog, QSizePolicy, QApplication, QLabel,
)
from qfluentwidgets import (
    TitleLabel, CaptionLabel, StrongBodyLabel, PushButton, PrimaryPushButton,
    ScrollArea, CardWidget, VBoxLayout, ProgressBar, InfoBar, InfoBarPosition,
    FluentIcon, SubtitleLabel, qconfig,
)

from src.main.app.common.JarScanner import scanDirectory
from src.main.app.common.AppTheme import pngListStyle, summaryBannerStyle, versionBadgeStyle


def _logoBaseNames(pngs: list) -> list:
    """从 jar 内匹配到的 png 路径推导 logo 基础名(保留目录前缀, 去掉 @2x.png/.png 扩展名并去重)。"""
    bases = []
    for path in pngs:
        if path.endswith("@2x.png"):
            base = path[:-len("@2x.png")]
        elif path.endswith(".png"):
            base = path[:-len(".png")]
        else:
            base = path
        if base not in bases:
            bases.append(base)
    return bases


class _ScanResultCard(CardWidget):
    """扫描结果卡片: 右键生成 JarPath 配置片段并复制到剪贴板。"""

    def __init__(self, jarPath: str, pngs: list, scanRoot: str, onCopied):
        super().__init__()
        self._jarPath = jarPath
        self._pngs = pngs
        self._scanRoot = scanRoot
        self._onCopied = onCopied

    def _buildConfig(self) -> str:
        rel = os.path.relpath(self._jarPath, self._scanRoot).replace("\\", "/")
        key = "/" + rel
        value = _logoBaseNames(self._pngs) or ["*", "*"]
        return json.dumps({key: value}, ensure_ascii=False)

    def contextMenuEvent(self, event):
        text = self._buildConfig()
        QApplication.clipboard().setText(text)
        self._onCopied(text)
        event.accept()


class JarScanWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_ = parent
        self.setWidgetResizable(True)
        self.setFrameShape(self.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.wrapper = QWidget()
        wrapperLayout = QHBoxLayout(self.wrapper)
        wrapperLayout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setMaximumWidth(720)
        self.layout = VBoxLayout(container)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

        self.title = TitleLabel("JAR 资源扫描")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle = CaptionLabel("扫描目录下所有 .jar 文件, 列出内含 *logo*.png 资源的 jar")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)

        # 操作卡片: 目录选择 + 扫描按钮
        opCard = CardWidget()
        opLayout = VBoxLayout(opCard)
        opLayout.setContentsMargins(16, 12, 16, 12)
        opLayout.setSpacing(8)

        self.dirHeader = SubtitleLabel("扫描目录")
        opLayout.addWidget(self.dirHeader)

        opRow = QHBoxLayout()
        opRow.setSpacing(8)
        self.selectButton = PushButton(FluentIcon.FOLDER, "选择目录", self)
        self.selectButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.selectButton.clicked.connect(self.chooseDirectory)
        self.scanButton = PrimaryPushButton(FluentIcon.SEARCH, "开始扫描", self)
        self.scanButton.setEnabled(False)
        self.scanButton.clicked.connect(self.startScan)
        opRow.addWidget(self.selectButton, 1)
        opRow.addWidget(self.scanButton)
        opLayout.addLayout(opRow)

        self.dirLabel = CaptionLabel("尚未选择目录")
        self.dirLabel.setWordWrap(True)
        opLayout.addWidget(self.dirLabel)

        self.progressBar = ProgressBar()
        # 进度条放入固定高度容器: 容器始终占位, 进度条显隐不再改变卡片高度
        self.progressHolder = QWidget()
        self.progressHolder.setFixedHeight(self.progressBar.height())
        holderLayout = QHBoxLayout(self.progressHolder)
        holderLayout.setContentsMargins(0, 0, 0, 0)
        holderLayout.addWidget(self.progressBar)
        opLayout.addWidget(self.progressHolder)
        # 必须在加入布局后隐藏, 否则父窗口 show 时会覆盖隐藏状态
        self.progressBar.setVisible(False)

        self.layout.addWidget(opCard)

        # 扫描目标信息 (IDE 名称 + 版本)
        self.scanInfoLabel = SubtitleLabel("")
        self.scanInfoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.scanInfoLabel)
        self.scanInfoLabel.setVisible(False)

        # 结果统计条
        self.resultLabel = StrongBodyLabel("")
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._applySummaryStyle()
        self.layout.addWidget(self.resultLabel)
        self.resultLabel.setVisible(False)

        # 扫描完成后的适配提示(带可点击链接)
        self.adaptHint = CaptionLabel()
        self.adaptHint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adaptHint.setWordWrap(True)
        self.adaptHint.setTextFormat(Qt.TextFormat.RichText)
        self.adaptHint.setText(
            '如需适配此版本, 可向 <a href="https://github.com/xiyi20/JetbrainsSS/issues">GitHub Issues</a>'
            ' 提适配要求, 需提供扫描出的完整结果截图和对应的 jar 文件'
        )
        self.adaptHint.setOpenExternalLinks(True)
        self.layout.addWidget(self.adaptHint)
        self.adaptHint.setVisible(False)

        # 空状态提示
        self.emptyHint = QLabel()
        self.emptyHint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emptyHint.setText("选择目录并开始扫描, 匹配结果将显示在这里")
        self.emptyHint.setStyleSheet("color: rgba(128, 128, 128, 0.7); padding: 24px 0;")
        self.layout.addWidget(self.emptyHint)

        # 结果卡片区
        self.resultsArea = QWidget()
        self.resultsLayout = VBoxLayout(self.resultsArea)
        self.resultsLayout.setContentsMargins(0, 0, 0, 0)
        self.resultsLayout.setSpacing(8)
        self.layout.addWidget(self.resultsArea)

        self.layout.addStretch(1)

        wrapperLayout.addWidget(container)
        self.setWidget(self.wrapper)

        qconfig.themeChangedFinished.connect(self._applySummaryStyle)
        self.selectedDir = ""

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 视口宽度超过内容上限时, 用对称边距实现居中
        margin = max(0, (self.viewport().width() - 720) // 2)
        self.widget().layout().setContentsMargins(margin, 0, margin, 0)

    def _applySummaryStyle(self):
        self.resultLabel.setStyleSheet(summaryBannerStyle())

    def loadDirectory(self, path: str, ideName: str = "", version: str = ""):
        """由外部(如主页版本徽章右键)设置扫描目录。
        安装根目录下 lib/ 才是 logo 资源所在, 优先扫描 lib 以跳过 jbr/plugins 的海量无关 jar。"""
        if not path or not os.path.isdir(path):
            return
        libDir = os.path.join(path, "lib").replace("\\", "/").rstrip("/")
        target = libDir if os.path.isdir(libDir) else path
        self.selectedDir = target
        self.dirLabel.setText(f"📂 {target}")
        self.scanButton.setEnabled(True)
        if ideName:
            self.scanInfoLabel.setText(f"{ideName}  {version}".strip())

    def chooseDirectory(self):
        folder = QFileDialog.getExistingDirectory(self.parent_, "选择要扫描的目录")
        if folder:
            self.selectedDir = folder
            self.dirLabel.setText(f"📂 {folder}")
            self.scanButton.setEnabled(True)
            self.scanInfoLabel.setVisible(False)

    def clearResults(self):
        while self.resultsLayout.count():
            item = self.resultsLayout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def startScan(self):
        if not self.selectedDir or not os.path.isdir(self.selectedDir):
            return
        self.scanInfoLabel.setVisible(True)
        self.clearResults()
        self.scanButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.emptyHint.setVisible(False)
        self.resultLabel.setVisible(False)
        self.adaptHint.setVisible(False)
        self.progressBar.setVisible(True)
        self.progressBar.setRange(0, 0)  # 忙碌态, 扫描完成前不定量
        QApplication.processEvents()  # 让忙碌进度条先渲染

        found = 0
        totalJars = 0
        for idx, total, jarPath, pngs in scanDirectory(self.selectedDir):
            totalJars = total
            if pngs:
                found += 1
                self._addResultCard(jarPath, pngs)
            # 定期刷新界面, 避免长时间无响应
            if idx % 5 == 0:
                QApplication.processEvents()

        self.progressBar.setVisible(False)
        self.selectButton.setEnabled(True)
        self.scanButton.setEnabled(True)

        self.resultLabel.setText(f"共扫描 {totalJars} 个 jar · {found} 个含 *logo*.png 资源")
        self.resultLabel.setVisible(True)
        self.adaptHint.setVisible(True)
        if found == 0:
            self.emptyHint.setText("未找到匹配的资源")
            self.emptyHint.setVisible(True)
            InfoBar.info(
                title="未找到匹配资源",
                content="所选目录下没有包含 *logo*.png 的 jar 文件",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent_,
            )

    def _copyHint(self, text: str):
        InfoBar.success(
            title="配置已复制到剪贴板",
            content=text,
            orient=Qt.AlignmentFlag.AlignHCenter,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent_,
        )

    def _addResultCard(self, jarPath: str, pngs: list):
        card = _ScanResultCard(jarPath, pngs, self.selectedDir, self._copyHint)
        layout = VBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        # 头部: 文件名 + 数量徽章
        header = QHBoxLayout()
        header.setSpacing(8)
        fileIcon = QLabel()
        fileIcon.setPixmap(FluentIcon.DOCUMENT.icon().pixmap(20, 20))
        header.addWidget(fileIcon)
        nameLabel = StrongBodyLabel(os.path.basename(jarPath))
        # 长文件名中间省略, 避免撑破卡片宽度
        fm = nameLabel.fontMetrics()
        nameLabel.setText(fm.elidedText(os.path.basename(jarPath), Qt.TextElideMode.ElideMiddle, 300))
        header.addWidget(nameLabel, 1)
        countBadge = QLabel(f"{len(pngs)} 项")
        countBadge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        countBadge.setStyleSheet(versionBadgeStyle())
        header.addWidget(countBadge)
        layout.addLayout(header)

        dirLabel = CaptionLabel(os.path.dirname(jarPath))
        dirLabel.setWordWrap(True)
        layout.addWidget(dirLabel)

        # 资源列表: 放入柔和底色容器
        listPanel = QWidget()
        listPanel.setStyleSheet(pngListStyle())
        listLayout = VBoxLayout(listPanel)
        listLayout.setContentsMargins(12, 8, 12, 8)
        listLayout.setSpacing(2)
        for name in pngs:
            item = CaptionLabel()
            ifm = item.fontMetrics()
            item.setText(ifm.elidedText(f"• {name}", Qt.TextElideMode.ElideMiddle, 430))
            item.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            # 不弹 Qt 内置文本菜单, 让右键事件透传到卡片(生成配置)
            item.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            listLayout.addWidget(item)
        layout.addWidget(listPanel)

        self.resultsLayout.addWidget(card)
