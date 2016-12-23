import os
from minpass.clipboard import Clipboard
from minpass.command import Command
from minpass.debug import debug
from minpass.keyring import Keyring
from minpass.keyring_controler import KeyringControler
from minpass.security import Security
from minpass.ui import UI


class Console(object):
    """ Console execution

    Attributes:
        clipboard: Clipboard object
        keyring_controler: KeyringControler object
        running: True if the console is running
        commands: list of Command objects
    """
    def __init__(self):
        self._clipboard = Clipboard()
        self._keyring_controler = None
        self._running = False
        self._commands = []

    def __load_commands(self):
        self._commands = [
            Command("add", ["account_name"], self.__add_account,
                    "register a new account"),
            Command("chpp", [], self._keyring_controler.change_passphrase,
                    "change keyring passphrase"),
            Command("exit", [], self.__stop, "exit program"),
            Command("get", ["account_name"], self.__copy_password,
                    "copy account password into clipboard"),
            Command("help", [], self.__help, "print help"),
            Command("ls", [], self.__list, "list all accounts (names only)"),
            Command("print", ["account_name"], self.__print,
                    "(use with caution) print complete account, including password"),
            Command("rm", ["account_name"], self._keyring_controler.remove_account,
                    "remove account"),
        ]

    def __add_account(self, account_name):
        if UI.confirm("Generate password?", default_yes=True):
            print("Generating %s password..." % account_name)
            password = Security.generate_password()
        else:
            password = UI.create_secret("password")
        if self._keyring_controler.register_account(account_name, password):
            self.__copy_password(account_name)

    def __copy_password(self, user_input):
        account = self._keyring_controler.get_account(user_input)
        if not account:
            return
        self._clipboard.copy(account.password)
        print("Clipboard updated with %s password" % account.name)

    def __execute_command(self, user_input):
        user_input = user_input.split(" ", maxsplit=1)
        for command in self._commands:
            if command.name == user_input[0]:
                if len(command.args) == 0:
                    command.func()
                else:
                    if len(user_input) > 1:
                        command.func(user_input[1].strip())
                    else:
                        print("Bad arguments")
                return
        print("Command not found")

    def __help(self):
        for command in self._commands:
            print("%s %s - %s" % (command.name, "".join(command.args),
                                  command.help))

    def __list(self):
        accounts = self._keyring_controler.accounts
        sorted_accounts = sorted(accounts, key=lambda a:a.name)
        for account in sorted_accounts:
            print(account.name)

    def __print(self, user_input):
        print("Warning: When calling 'print', " \
              "beware console output redirections or logs")
        print("         Be sure to reset console output")
        print("         Prefer the use of 'get'")
        account = self._keyring_controler.get_account(user_input)
        if not account:
            return
        print("account: %s" % account.name)
        print("password: %s" % account.password)

    def __stop(self):
        """ Stop console loop
        """
        self._running = False

    def load_keyring(self, keyring_path):
        """ Load keyring from filesystem
        Ask user passphrase then load keyring
        Create keyring if non-existing

        Args:
            keyring_path: filesystem path to a keyring

        Returns: boolean result
        """
        passphrase = ""
        if not os.path.exists(keyring_path):
            if not UI.confirm("%s does not exist. Create new?" % keyring_path,
                              default_yes=True):
                return False
            passphrase = UI.create_secret("passphrase")
        else:
            passphrase = UI.type_secret("passphrase")
        if not passphrase:
            return False

        keyring = Keyring(keyring_path, passphrase)
        if not os.path.exists(keyring_path):
            keyring.save()
            print("New keyring saved in %s" % keyring_path)

        if not keyring.load():
            print("Loading failed")
            return False

        self._keyring_controler = KeyringControler(keyring)
        return True

    def run(self):
        """ Start console loop
        """
        self.__load_commands()
        user_input = ""
        self._running = True
        while self._running:
            user_input = input("%s $ "\
                               % self._keyring_controler.keyring_name).strip()
            if not user_input:
                continue
            self.__execute_command(user_input)
