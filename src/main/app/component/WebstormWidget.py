from src.main.app.common.JarPath import JarPath
from src.main.app.common.PathTool import PathTool
from src.main.app.component.IDEWidget import IDEWidget


class WebstormWidget(IDEWidget):
    def __init__(self, pathTool: PathTool, parent):
        super().__init__(JarPath.WebStorm, pathTool, parent)
