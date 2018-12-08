import abc
import six
import unittest2

from rapiduino.pin import ComponentPin
from rapiduino.components.base import BaseComponent


class ComponentCommon(object):

    @six.add_metaclass(abc.ABCMeta)
    class TestCase(unittest2.TestCase):

        def test_subclass(self):
            self.assertTrue(isinstance(self.component, BaseComponent))
            for pin in self.component.pins:
                self.assertTrue(isinstance(pin, ComponentPin))

        def test_pins(self):
            for pin_num in range(len(self.pins)):
                self.assertEqual(self.component.pins[pin_num].is_analog, self.pins[pin_num].is_analog)
                self.assertEqual(self.component.pins[pin_num].is_pwm, self.pins[pin_num].is_pwm)

        def test_number_of_pins(self):
            self.assertEqual(len(self.component.pins), len(self.pins))

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
