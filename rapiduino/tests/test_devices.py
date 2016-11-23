import unittest

from rapiduino.devices import ArduinoBase, ArduinoUno

class TestArduinoBase(unittest.TestCase):

    def test_subclass(self):
        self.assertTrue(issubclass(ArduinoBase, object))

class TestArduinoUno(unittest.TestCase):

    def setUp(self):
        self.device = ArduinoUno()

    def test_subclass(self):
        self.assertIsInstance(self.device, ArduinoBase)


if __name__ == '__main__':
    unittest.main()
