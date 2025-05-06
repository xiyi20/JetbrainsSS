import os
import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        string = r"pyinstaller --onefile --windowed -i '.\src\main\resources\logo.png' .\src\main\app\mian.py"
        for folder in "common", "component":
            path = fr"E:\CODE\git\JetbrainsSS\src\main\app\{folder}"
            for filename in os.listdir(path):
                if filename.endswith(".py"):
                    string += fr" .\src\main\app\{folder}\{filename}"
        print('\n'+string)
        self.assertEqual(1, 1)
