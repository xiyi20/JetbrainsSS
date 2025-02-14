from src.main.app.common.JarPath import JarPath
from src.main.app.common.PathTool import PathTool
from src.main.app.component.IDEWidget import IDEWidget


class PycharmWidget(IDEWidget):
    def __init__(self, pathTool: PathTool):
        super().__init__(JarPath.PyCharm, pathTool)
