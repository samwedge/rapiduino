import unittest
from rapiduino.communication import Commands, SerialConnection, CommandSpec
from rapiduino.exceptions import SerialConnectionError


class TestSerialConnection(unittest.TestCase):

    def setUp(self):
        self.conn = SerialConnection()

    def test_init(self):
        self.assertIsInstance(self.conn, SerialConnection)

    def test_connection_fails_with_no_port(self):
        with self.assertRaises(SerialConnectionError):
            self.conn.connect()


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()
        self.commands.add_command('poll')
        self.commands.add_command('parrot', 7)
        self.commands.add_command('pinMode', 3, 1)
        self.commands.add_command('analogRead', 5)
        self.commands.add_command('analogWrite', 17, 1)

    def test_commands_have_been_added(self):
        expected_commands = (
            (0,),
            (1, 7),
            (10, 3, 1),
            (30, 5),
            (31, 17, 1)
        )
        self.assertEqual(self.commands.command_list, expected_commands)

    def test_invalid_command_raises_error(self):
        with self.assertRaises(KeyError):
            self.commands.add_command('invalidCommand')

    def test_invalid_args_raises_error(self):
        with self.assertRaises(TypeError):
            self.commands.add_command('parrot', 3.7)

    def test_invalid_number_of_args_raises_error(self):
        with self.assertRaises(ValueError):
            self.commands.add_command('parrot', 0, 0)

    def test_commands_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.commands.command_list = []

    def test_next_command(self):
        expected_first_command = (0,)
        expected_remaining_commands = (
            (1, 7),
            (10, 3, 1),
            (30, 5),
            (31, 17, 1)
        )
        popped_command = self.commands.next_command()
        self.assertEqual(popped_command, expected_first_command)
        self.assertEqual(self.commands.command_list, expected_remaining_commands)

    def test_add_command_rejects_non_tuple(self):
        with self.assertRaises(TypeError):
            self.commands.add_command(0)

    def test_command_spec(self):
        self.assertIsInstance(self.commands.command_spec, dict)
        for key in self.commands.command_spec.keys():
            self.assertIn('cmd', self.commands.command_spec[key])
            self.assertIn('nargs', self.commands.command_spec[key])
            self.assertEqual(len(self.commands.command_spec[key]), 2)
            self.assertIsInstance(self.commands.command_spec[key]['cmd'], int)
            self.assertIsInstance(self.commands.command_spec[key]['nargs'], int)

    def test_command_spec_readonly(self):
        with self.assertRaises(AttributeError):
            self.commands.command_spec = 5


if __name__ == '__main__':
    unittest.main()
