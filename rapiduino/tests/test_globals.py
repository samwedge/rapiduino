import unittest2

from rapiduino.globals.common import HIGH, LOW, INPUT, OUTPUT, INPUT_PULLUP


class GlobalsTestCase(unittest2.TestCase):

    def test_global_type(self):
        parameters = [HIGH, LOW, INPUT, OUTPUT, INPUT_PULLUP]
        for parameter in parameters:
            self.assertIsInstance(parameter, tuple)
            self.assertEqual(len(parameter), 2)
            self.assertIsInstance(parameter[0], str)
            self.assertIsInstance(parameter[1], int)
