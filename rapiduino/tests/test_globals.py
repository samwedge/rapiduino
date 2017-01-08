import unittest

from rapiduino.globals import *


class GlobalsTestCase(unittest.TestCase):

    def test_global_type(self):
        self.assertIsInstance(HIGH, int)
        self.assertIsInstance(LOW, int)
        self.assertIsInstance(INPUT, int)
        self.assertIsInstance(OUTPUT, int)
        self.assertIsInstance(INPUT_PULLUP, int)


if __name__ == '__main__':
    unittest.main()
