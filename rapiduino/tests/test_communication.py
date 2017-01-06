import unittest
from rapiduino.communication import Commands, SerialConnection
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
        self.commands.add_command((1, 0, 9))
        self.commands.add_command((0,))
        self.commands.add_command((3, 0, 3, 7, 8))
        self.commands.add_command((4,))
        self.commands.add_command((5, 6, 2))

    def test_commands_have_been_added(self):
        expected_commands = (
            (1, 0, 9),
            (0,),
            (3, 0, 3, 7, 8),
            (4,),
            (5, 6, 2),
        )
        self.assertEqual(self.commands.command_list, expected_commands)

    def test_commands_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.commands.command_list = []

    def test_next_command(self):
        expected_first_command = (1, 0, 9)
        expected_remaining_commands = (
            (0,),
            (3, 0, 3, 7, 8),
            (4,),
            (5, 6, 2),
        )
        popped_command = self.commands.next_command()
        self.assertEqual(popped_command, expected_first_command)
        self.assertEqual(self.commands.command_list, expected_remaining_commands)

    def test_add_command_rejects_non_tuple(self):
        with self.assertRaises(TypeError):
            self.commands.add_command(0)


if __name__ == '__main__':
    unittest.main()
