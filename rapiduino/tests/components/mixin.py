from rapiduino.pin import ComponentPin
from rapiduino.components.base import BaseComponent


class TestComponentMixin(object):

    def test_subclass(self):
        self.assertTrue(isinstance(self.component, BaseComponent))
        for pin in self.component.pins:
            self.assertTrue(isinstance(pin, ComponentPin))

    def test_number_of_pins(self):
        self.assertEqual(len(self.component.pins), 1)

    def test_pin_ids(self):
        for pin_no, pin in enumerate(self.component.pins):
            self.assertEqual(pin_no, pin.id)

    def test_pins_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.component.pins = []
        self.assertIsInstance(self.component.pins, tuple)

    def test_device_is_readonly(self):
        with self.assertRaises(AttributeError):
            self.component.bound_device = 0
