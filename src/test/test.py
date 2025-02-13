import unittest

from src.main.app.common.JarPath import JarPath


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(type(JarPath.WebStorm.name))


if __name__ == '__main__':
    unittest.main()
