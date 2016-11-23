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

    def test_number_of_pins(self):
        self.assertEqual(len(self.device.pins), 20)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.device.pins = []
        self.device.pins[0] = ''
        self.assertNotEqual(self.device.pins[0], '')


if __name__ == '__main__':
    unittest.main()
