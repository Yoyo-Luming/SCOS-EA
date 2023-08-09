from .O0 import O0


def model_select(name):
    name = name.upper()

    if name == 'O0':
        return O0
