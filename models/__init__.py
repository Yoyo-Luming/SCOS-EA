from .O0 import O0
from .OS import OS
from .GREEDY import GREEDY
from .GA import GA
from .AGENTGA import AGENTGA


def model_select(name):
    name = name.upper()

    if name == 'O0':
        return O0
    elif name == 'OS':
        return OS
    elif name == 'GREEDY':
        return GREEDY
    elif name == 'GA':
        return GA
    elif name =='AGENTGA':
        return AGENTGA
