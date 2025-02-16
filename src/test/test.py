import unittest

import win32api

from src.main.app.common.JarPath import JarPath
from src.main.app.common.RwConfig import RwConfig


class MyTestCase(unittest.TestCase):
    def test_something(self):
        exePath = RwConfig().config["IDE"][JarPath.Idea.name]["exec"]
        info = win32api.GetFileVersionInfo(exePath, "\\")
        ms = info["ProductVersionMS"]
        print(f"{win32api.HIWORD(ms)}")

if __name__ == '__main__':
    unittest.main()
