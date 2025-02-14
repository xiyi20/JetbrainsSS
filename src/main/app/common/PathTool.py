import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import LineEdit, InfoBar, InfoBarPosition
from src.main.app.common.JarPath import JarPath
from src.main.app.common.RwConfig import RwConfig


class PathTool:
    _pathTool = None
    def __new__(cls, *args, **kwargs):
        if not cls._pathTool:
            cls._pathTool = super(PathTool, cls).__new__(cls)
        return cls._pathTool

    def __init__(self, parent):
        self.parent = parent

    def getDirectory(self, text: str, label: LineEdit, panel: QWidget):
        folder = QFileDialog.getExistingDirectory(None, f"选择{text}的目录")
        if folder and self.checkPath(folder, text, panel):
            label.setText(folder)

    def checkPath(self, folder: str, text: str, panel: QWidget):
        check_exe = False
        exe1 = f"{folder}/bin/{text.lower()}64.exe"
        exe2 = f"{folder}/bin/{text.lower()}32.exe"
        for exe in [exe1, exe2]:
            if os.path.exists(exe) and os.path.isfile(exe):
                check_exe = True
                break
        jar = f"{folder}{JarPath[text].value[:JarPath[text].value.index('.') + 4]}"
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
            panel.setVisible(True)
            RwConfig().wConfig("Path", text, folder)
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
            panel.setVisible(False)
            RwConfig().wConfig("Path", text, "")
        return result