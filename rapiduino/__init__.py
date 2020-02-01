__version__ = '1.0.0'

from collections import namedtuple

GlobalParameter = namedtuple('GlobalParameter', ['name', 'value'])
CommandSpec = namedtuple('CommandSchema', ['cmd', 'tx_len', 'tx_type', 'rx_len', 'rx_type'])
