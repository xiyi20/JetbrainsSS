import os

import win32api
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton, BodyLabel

from src.main.app.common.AppTheme import versionBadgeStyle, unsupportedBadgeStyle
from src.main.app.common.JarPath import JarPath
from src.main.app.common.RwConfig import RwConfig
from src.main.app.component.FLineEdit import FLineEdit


class PathTool:
    _pathTool = None

    def __new__(cls, *args, **kwargs):
        if not cls._pathTool:
            cls._pathTool = super(PathTool, cls).__new__(cls)
        return cls._pathTool

    def __init__(self, parent):
        self.parent = parent
        self.onBindingChanged = None

    from src.main.app.component.OptionWidget import OptionWidget
    def getIdeDirectory(self, ide: str, idePath: FLineEdit, ideVersion: BodyLabel, panel: OptionWidget):
        folder = QFileDialog.getExistingDirectory(None, f"选择{ide}的目录")
        if folder:
            self.checkIdePath(folder, ide, idePath, ideVersion, panel)

    def checkIdePath(self, folder: str, ide: str, idePath: FLineEdit, ideVersion: BodyLabel, panel: OptionWidget,
                     silent: bool = False):
        check_exe = False
        platforms = [64, 32]
        version = ''
        for platform in platforms:
            exe = f"{folder}/bin/{ide.lower()}{platform}.exe"
            if os.path.exists(exe) and os.path.isfile(exe):
                check_exe = True
                info = win32api.GetFileVersionInfo(exe, "\\")
                ms = str(win32api.HIWORD(info["ProductVersionMS"]))
                version = ms
                ideVersion.setText(f"v{version}")
                ideVersion.setVisible(True)
                RwConfig().wConfig("IDE", ide, "version", version)
                version = version[:4]
                break
        supported = check_exe and version in JarPath[ide].value
        # 仅当配置的所有 jar 文件都真实存在时才允许修补; 版本支持但 jar 缺失同样禁止
        jarExists = False
        if supported:
            jarExists = all(
                os.path.isfile(f"{folder}{jarRel}")
                for jarMap in JarPath[ide].value[version]
                for jarRel in jarMap
            )
        if not check_exe:
            # 目录本身无效(未找到启动程序) -> 清除绑定
            InfoBar.warning(
                title=folder,
                content=f"该目录不是有效的{ide}安装目录",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
            panel.setVisible(False)
            idePath.setText("")
            idePath.setEnabled(True)
            ideVersion.setVisible(False)
            RwConfig().wConfig("IDE", ide, "path", "")
            if self.onBindingChanged: self.onBindingChanged()
            return False
        # 目录有效: 保留绑定; 版本不支持或 jar 缺失时禁止修补
        panel.setVisible(True)
        idePath.setText(folder)
        idePath.setEnabled(False)
        RwConfig().wConfig("IDE", ide, "path", folder)
        ideVersion.setText(f"v{version}")
        if jarExists:
            ideVersion.setStyleSheet(versionBadgeStyle())
            panel.setPatchEnabled(True)
            if not silent:
                InfoBar.success(
                    title=folder,
                    content=f"该目录已被绑定为{ide}的安装目录\n手动输入已锁定,长按对应[选择]按钮解锁",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent,
                )
            panel.initJarEditor(folder, version)
        else:
            ideVersion.setStyleSheet(unsupportedBadgeStyle())
            panel.setPatchEnabled(False)
            if not silent:
                InfoBar.warning(
                    title=folder,
                    content=f"已绑定{ide}安装目录, 但版本 v{version} 暂不支持\n您可通过右键版本徽章对该版本进行快速扫描",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent,
                )
        if self.onBindingChanged: self.onBindingChanged()
        return jarExists

    def getSplashPath(self, ide: str, splash: str, targetLabel: FLineEdit, checkLabel: FLineEdit,
                      button: PrimaryPushButton):
        splashPath, _ = QFileDialog.getOpenFileName(None, f"请选择{ide}的{splash}", "", "图片文件 (*.png)")
        if splashPath:
            # splash 形如 "splash(640*400px)", 取括号前的键名; 不能用固定长度截取(splash@2x 长度不同)
            self.checkSplashPath(ide, targetLabel, checkLabel, splash.split("(")[0], splashPath, button)

    def checkSplashPath(self, ide: str, targetLabel: FLineEdit, checkLabel: FLineEdit, splash: str, splashPath: str,
                        button: PrimaryPushButton):
        if os.path.exists(splashPath) and os.path.isfile(splashPath) and splashPath.endswith(".png"):
            splashSize = {"splash": (640, 400), "splash@2x": (1280, 800)}[splash]
            imgSize = Image.open(splashPath).size
            if imgSize == splashSize:
                InfoBar.success(
                    title=splashPath,
                    content=f"该文件已被绑定为{ide}的{splash}\n手动输入已锁定,长按对应[选择]按钮解锁",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent,
                )
                targetLabel.setText(splashPath)
                targetLabel.setEnabled(False)
                RwConfig().wConfig("IDE", ide, splash, splashPath)
                if checkLabel.text(): button.setEnabled(True)
                # todo 输入框删除内容后需要禁用按钮
                return True
            else:
                InfoBar.error(
                    title=splashPath,
                    content=f"图片的分辨率应为{splashSize[0]}*{splashSize[1]}px,而不是{imgSize[0]}*{imgSize[1]}px",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent,
                )
                targetLabel.setText("")
                targetLabel.setEnabled(True)
                RwConfig().wConfig("IDE", ide, splash, "")
                return False
        else:
            InfoBar.warning(
                title=splashPath,
                content=f"该文件不符合要求",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
            targetLabel.setText("")
            targetLabel.setEnabled(True)
            return False

    def unlockLabel(self, label: FLineEdit, button: PrimaryPushButton = None):
        label.setEnabled(True)
        InfoBar.warning(
            title="手动输入已解锁",
            content="为避免错填可[输入框内长按右键]锁定",
            orient=Qt.AlignmentFlag.AlignHCenter,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.parent,
        )
        if button: button.setEnabled(False)
