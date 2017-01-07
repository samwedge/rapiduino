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

    def test_pin_mode_sets_mode(self):
        self.assertEqual(self.device.pins[0].pin_mode, 'INPUT')
        self.device.pin_mode(0, 'OUTPUT')
        self.assertEqual(self.device.pins[0].pin_mode, 'OUTPUT')

    def test_pin_mode_with_incorrect_mode(self):
        with self.assertRaises(ValueError):
            self.device.pin_mode(0, 'INVALID_MODE')

    def test_pin_mode_with_pin_no_out_of_range(self):
        with self.assertRaises(IndexError):
            self.device.pin_mode(500, 'OUTPUT')


if __name__ == '__main__':
    unittest.main()
