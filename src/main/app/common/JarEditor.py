import os.path
import shutil
from enum import Enum
from zipfile import ZipFile

from PyQt6.QtCore import Qt, QObject
from qfluentwidgets import ProgressBar, InfoBar, InfoBarPosition

from src.main.app.common.RwConfig import RwConfig


class JarEditor(QObject):

    def __init__(self, IDE: Enum, baseDir: str, version: str, progress: ProgressBar, parent=None):
        super().__init__(parent)
        self.IDE = IDE
        self.jarPath = f"{baseDir}{self.IDE.value[version][0]}"
        self.version = version
        self.bakPath = self.jarPath + ".bak"
        self.cachePath = f"C:/Users/{os.getlogin()}/AppData/Local/JetBrains/"
        self.progress = progress
        self.parent = parent

    def edit(self, buttons: list, logoPath: list):
        targetName = self.IDE.value[self.version][1]
        tempJar = self.jarPath + ".tmp"
        for button in buttons: button.setEnabled(False)
        try:
            self.restore(False, False)
            self.progress.setValue(0)
            shutil.copy(self.jarPath, self.jarPath + ".bak")
            targets = [
                targetName + '.png',
                targetName + '@2x.png'
            ]
            self.progress.resume()
            with ZipFile(self.jarPath, "r") as old:
                total = len(old.namelist())
                current = 0
                with ZipFile(tempJar, "w") as new:
                    for file in old.infolist():
                        fileName = file.filename
                        if fileName in targets:
                            with open(logoPath[targets.index(fileName)], "rb") as logo:
                                data = logo.read()
                        else:
                            data = old.read(fileName)
                        new.writestr(file, data, compress_type=file.compress_type)
                        current += 1
                        self.progress.setValue(int(current / total) * 80)
            shutil.move(tempJar, self.jarPath)
            self.clearCache()
            self.progress.setValue(100)
            InfoBar.success(
                title="splash修补成功",
                content="运行IDE以查看效果,如遇报错打不开请点击[还原]",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.parent,
            )
        except OSError:
            InfoBar.error(
                title=f"{self.IDE.name}修补失败",
                content=f"{self.IDE.name}正在运行中,请关闭后重试",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=4500,
                parent=self.parent,
            )
            return
        except Exception as e:
            self.restore(True, False)
            self.progress.setError(True)
            InfoBar.error(
                title="splash修补出错,已强制还原备份",
                content=e,
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.parent,
            )
        finally:
            if os.path.exists(tempJar) and os.path.isfile(tempJar):
                os.remove(tempJar)
            for button in buttons: button.setEnabled(True)

    def restore(self, clear: bool, dialog: bool, buttons=None):
        self.progress.setValue(0)
        enabled = False
        if buttons is not None:
            enabled = buttons[0].isEnabled()
            for button in buttons: button.setEnabled(False)
        if os.path.exists(self.bakPath) and os.path.isfile(self.bakPath):
            try:
                shutil.move(self.bakPath, self.jarPath)
            except OSError:
                InfoBar.error(
                    title=f"{self.IDE.name}还原失败",
                    content=f"{self.IDE.name}正在运行中,请关闭后重试",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=4500,
                    parent=self.parent,
                )
                return
            finally:
                if buttons is not None:
                    buttons[0].setEnabled(enabled)
                    buttons[1].setEnabled(True)
            self.progress.setValue(100)
            if clear: self.clearCache()
            if dialog:
                InfoBar.success(
                    title=f"{self.IDE.name}还原成功",
                    content=f"已还原对于{self.IDE.name}的splash修改",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=4500,
                    parent=self.parent,
                )
        else:
            self.progress.setError(True)
            self.progress.setValue(100)
            if buttons is not None:
                buttons[0].setEnabled(enabled)
                buttons[1].setEnabled(True)
            if dialog:
                InfoBar.warning(
                    title=f"{self.IDE.name}还原失败",
                    content=f"当前没有对于{self.IDE.name}的任何修改,无需还原",
                    orient=Qt.AlignmentFlag.AlignHCenter,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self.parent,
                )

    def clearCache(self):
        version = RwConfig().config["IDE"][self.IDE.name]["version"]
        if not (os.path.exists(self.cachePath) and os.path.isdir(self.cachePath)):
            return
        rm = False
        for directory in os.listdir(self.cachePath):
            if self.IDE.name in directory and directory.endswith(version):
                cachePath = f"{self.cachePath}{directory}/splash"
                if os.path.exists(cachePath) and os.path.isdir(cachePath):
                    for filename in os.listdir(cachePath):
                        if filename.endswith(".ij"):
                            os.remove(os.path.join(cachePath, filename))
                            rm = True
                break
        if rm:
            InfoBar.success(
                title="清理缓存成功",
                content="已清理当前IDE的缓存文件",
                orient=Qt.AlignmentFlag.AlignHCenter,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self.parent,
            )
