import unittest
from rapiduino.base import Pin


class TestPin(unittest.TestCase):
    def setUp(self):
        self.pin = Pin()

    def test_init(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(issubclass(Pin, object))

    def test_defaults(self):
        self.assertEqual(self.pin.pin_mode, 'INPUT')

    def test_pin_mode_setget(self):
        self.pin.pin_mode = 'OUTPUT'
        self.assertEqual(self.pin.pin_mode, 'OUTPUT')
        self.pin.pin_mode = 'INPUT'
        self.assertEqual(self.pin.pin_mode, 'INPUT')
        self.pin.pin_mode = 'INPUT_PULLUP'
        self.assertEqual(self.pin.pin_mode, 'INPUT_PULLUP')
        with self.assertRaises(ValueError):
            self.pin.pin_mode = 'some_incorrect_value'


if __name__ == '__main__':
    unittest.main()
