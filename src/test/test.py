import os.path
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(os.getlogin())


if __name__ == '__main__':
    unittest.main()
