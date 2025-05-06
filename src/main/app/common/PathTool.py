import os

import win32api
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from qfluentwidgets import InfoBar, InfoBarPosition, PrimaryPushButton

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

    from src.main.app.component.OptionWidget import OptionWidget
    def getIdeDirectory(self, ide: str, label: FLineEdit, panel: OptionWidget):
        folder = QFileDialog.getExistingDirectory(None, f"选择{ide}的目录")
        if folder:
            self.checkIdePath(folder, ide, label, panel)

    def checkIdePath(self, folder: str, ide: str, label: FLineEdit, panel: OptionWidget):
        check_exe = False
        platforms = [64, 32]
        version = ''
        for platform in platforms:
            exe = f"{folder}/bin/{ide.lower()}{platform}.exe"
            if os.path.exists(exe) and os.path.isfile(exe):
                check_exe = True
                info = win32api.GetFileVersionInfo(exe, "\\")
                ms = str(win32api.HIWORD(info["ProductVersionMS"]))
                version = f"20{ms[:2]}.{ms[2:]}"
                RwConfig().wConfig("IDE", ide, "version", version)
                version = version[:4]
                break
        jar = f"{folder}{JarPath[ide].value[version][0]}"
        result = os.path.exists(jar) and os.path.isfile(jar) and check_exe
        if result:
            InfoBar.success(
                title=folder,
                content=f"该目录已被绑定为{ide}的安装目录\n手动输入已锁定,长按对应[选择]按钮解锁",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
            panel.setVisible(True)
            panel.initJarEditor(folder, version)
            label.setText(folder)
            label.setEnabled(False)
            RwConfig().wConfig("IDE", ide, "path", folder)
        else:
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
            label.setText("")
            label.setEnabled(True)
            RwConfig().wConfig("IDE", ide, "path", "")
        return result

    def getSplashPath(self, ide: str, splash: str, targetLabel: FLineEdit, checkLabel: FLineEdit,
                      button: PrimaryPushButton):
        splashPath, _ = QFileDialog.getOpenFileName(None, f"请选择{ide}的{splash}", "", "图片文件 (*.png)")
        if splashPath:
            self.checkSplashPath(ide, targetLabel, checkLabel, splash[:7], splashPath, button)

    def checkSplashPath(self, ide: str, targetLabel: FLineEdit, checkLabel: FLineEdit, splash: str, splashPath: str,
                        button: PrimaryPushButton):
        if os.path.exists(splashPath) and os.path.isfile(splashPath) and splashPath.endswith(".png"):
            splashSize = {"splash1": (640, 400), "splash2": (1280, 800)}[splash]
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
                    content=f"该文件的大小应为{splashSize}px,而不是{imgSize}px",
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
