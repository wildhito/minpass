class Command(object):
    """ Command representation

    Attributes:
        name: command name
        args: argument list
        func: callback function
        help: help string
    """
    def __init__(self, name, args, func, help):
        self._name = name
        self._args = args
        self._func = func
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args

    @property
    def func(self):
        return self._func

    @property
    def help(self):
        return self._help
