from collections import namedtuple

__all__ = [
    'CMD_POLL', 'CMD_PARROT', 'CMD_VERSION', 'CMD_PINMODE', 'CMD_DIGITALREAD',
    'CMD_DIGITALWRITE', 'CMD_ANALOGREAD', 'CMD_ANALOGWRITE'
]

CommandSpec = namedtuple('CommandSchema', ['cmd', 'tx_len', 'tx_type', 'rx_len', 'rx_type'])
CMD_POLL = CommandSpec(cmd=0, tx_len=0, tx_type='B', rx_len=1, rx_type='B')
CMD_PARROT = CommandSpec(cmd=1, tx_len=1, tx_type='B', rx_len=1, rx_type='B')
CMD_VERSION = CommandSpec(cmd=2, tx_len=0, tx_type='B', rx_len=3, rx_type='B')
CMD_PINMODE = CommandSpec(cmd=10, tx_len=2, tx_type='B', rx_len=0, rx_type='')
CMD_DIGITALREAD = CommandSpec(cmd=20, tx_len=1, tx_type='B', rx_len=1, rx_type='B')
CMD_DIGITALWRITE = CommandSpec(cmd=21, tx_len=2, tx_type='B', rx_len=0, rx_type='')
CMD_ANALOGREAD = CommandSpec(cmd=30, tx_len=1, tx_type='B', rx_len=1, rx_type='H')
CMD_ANALOGWRITE = CommandSpec(cmd=31, tx_len=2, tx_type='B', rx_len=0, rx_type='')
