import os.path
import shutil
from enum import Enum
from zipfile import ZipFile

from PyQt6.QtCore import Qt, QObject, QTimer
from qfluentwidgets import ProgressBar, InfoBar, InfoBarPosition

from src.main.app.common.RwConfig import RwConfig


class JarEditor(QObject):

    def __init__(self, IDE: Enum, baseDir: str, version: str, progress: ProgressBar, parent=None):
        super().__init__(parent)
        self.IDE = IDE
        self.version = version
        # 任务列表: [(jarPath, [logo 基础名, ...]), ...], 同一版本可含多个 jar
        self.tasks = []
        for jarMap in self.IDE.value[version]:
            for jarRel, names in jarMap.items():
                self.tasks.append((f"{baseDir}{jarRel}", names))
        self.cachePath = f"C:/Users/{os.getlogin()}/AppData/Local/JetBrains/"
        self.progress = progress
        self.parent = parent

    @staticmethod
    def _bakOf(jarPath: str) -> str:
        return jarPath + ".bak"

    def edit(self, buttons: list, logoPath: list):
        tempJars = []
        for button in buttons: button.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        try:
            self.restore(False, False)
            # restore 在无备份时会置红色错误态, 需在其后复位
            self.progress.setError(False)
            # 备份所有目标 jar
            for jarPath, _names in self.tasks:
                shutil.copy(jarPath, self._bakOf(jarPath))
            # 每个 jar 占总进度的份额
            perJar = 80 // len(self.tasks) if self.tasks else 80
            for taskIdx, (jarPath, targetNames) in enumerate(self.tasks):
                tempJar = jarPath + ".tmp"
                tempJars.append(tempJar)
                logoMap = {}
                for name in targetNames:
                    for ext, logo in (('.png', logoPath[0]), ('@2x.png', logoPath[1])):
                        logoMap[name + ext] = logo
                with ZipFile(jarPath, "r") as old:
                    total = len(old.namelist())
                    current = 0
                    with ZipFile(tempJar, "w") as new:
                        for file in old.infolist():
                            fileName = file.filename
                            if fileName in logoMap:
                                with open(logoMap[fileName], "rb") as logo:
                                    data = logo.read()
                            else:
                                data = old.read(fileName)
                            new.writestr(file, data, compress_type=file.compress_type)
                            current += 1
                            self.progress.setValue(int(taskIdx * perJar + current / total * perJar))
                shutil.move(tempJar, jarPath)
                if tempJar in tempJars:
                    tempJars.remove(tempJar)
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
            for tempJar in tempJars:
                if os.path.exists(tempJar) and os.path.isfile(tempJar):
                    os.remove(tempJar)
            for button in buttons: button.setEnabled(True)
            QTimer.singleShot(1500, lambda: self.progress.setVisible(False))

    def restore(self, clear: bool, dialog: bool, buttons=None):
        if dialog:
            self.progress.setVisible(True)
            self.progress.setError(False)
        self.progress.setValue(0)
        enabled = False
        if buttons is not None:
            enabled = buttons[0].isEnabled()
            for button in buttons: button.setEnabled(False)
        # 只要存在任意备份就还原; 全部还原成功才计为成功
        baks = [(jarPath, self._bakOf(jarPath)) for jarPath, _ in self.tasks]
        hasBak = any(os.path.exists(bak) and os.path.isfile(bak) for _jar, bak in baks)
        if hasBak:
            try:
                for jarPath, bak in baks:
                    if os.path.exists(bak) and os.path.isfile(bak):
                        shutil.move(bak, jarPath)
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
                if dialog:
                    QTimer.singleShot(1500, lambda: self.progress.setVisible(False))
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
                QTimer.singleShot(1500, lambda: self.progress.setVisible(False))
        else:
            self.progress.setError(True)
            self.progress.setValue(100)
            if dialog:
                QTimer.singleShot(1500, lambda: self.progress.setVisible(False))
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
        version:str = RwConfig().config["IDE"][self.IDE.name]["version"]
        version = f"{version[:-1]}.{version[-1:]}"  # '25.3'
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
