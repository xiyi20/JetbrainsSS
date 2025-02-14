from PyQt6.QtWidgets import QWidget

from src.main.app.common.JarPath import JarPath
from src.main.app.common.PathTool import PathTool
from src.main.app.component.IDEWidget import IDEWidget


class WebstormWidget(IDEWidget):
    def __init__(self, pathTool: PathTool):
        super().__init__(JarPath.WebStorm, pathTool)
