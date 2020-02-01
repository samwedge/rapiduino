
__all__ = ['LOW', 'HIGH', 'INPUT', 'OUTPUT', 'INPUT_PULLUP']

from rapiduino import GlobalParameter

LOW = GlobalParameter('LOW', 0)
HIGH = GlobalParameter('HIGH', 1)

INPUT = GlobalParameter('INPUT', 0)
OUTPUT = GlobalParameter('OUTPUT', 1)
INPUT_PULLUP = GlobalParameter('INPUT_PULLUP', 2)
