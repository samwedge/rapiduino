import unittest

from rapiduino.devices import ArduinoBase, ArduinoUno


class TestArduinoUno(unittest.TestCase):

    def setUp(self):
        self.device = ArduinoUno()

    def test_subclass(self):
        self.assertIsInstance(self.device, ArduinoBase)

    def test_number_of_pins(self):
        self.assertEqual(len(self.device.pins), 20)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.device.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.device.pins = []
        self.assertIsInstance(self.device.pins, tuple)


if __name__ == '__main__':
    unittest.main()
