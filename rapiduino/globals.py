from collections import namedtuple

GlobalParameter = namedtuple('GlobalParameter', ['name', 'value'])

LOW = GlobalParameter('LOW', 0)
HIGH = GlobalParameter('HIGH', 1)

INPUT = GlobalParameter('INPUT', 0)
OUTPUT = GlobalParameter('OUTPUT', 1)
INPUT_PULLUP = GlobalParameter('INPUT_PULLUP', 2)
