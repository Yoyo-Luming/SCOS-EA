from .O0 import O0
from .OS import OS


def model_select(name):
    name = name.upper()

    if name == 'O0':
        return O0
    elif name == 'OS':
        return OS

