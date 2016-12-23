class Account(object):
    """ User account representation

    Attributes:
        name: account name
        password: account password
    """
    def __init__(self, name, password):
        self._name = name
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password
