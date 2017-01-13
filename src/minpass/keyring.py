import os
import pickle
from minpass.account import Account
from minpass.debug import debug
from minpass.security import Security


class Keyring(object):
    """ Account list management

    Attributes:
        filepath: path on filesystem where the keyring file is saved
        name: keyring name
        accounts: account list
        passphrase: security passphrase
    """
    def __init__(self, filepath, passphrase):
        self._filepath = filepath
        self._name = os.path.basename(filepath)
        self._accounts = []
        self._passphrase = passphrase

    @property
    def name(self):
        return self._name

    @property
    def accounts(self):
        return self._accounts

    def set_passphrase(self, passphrase):
        self._passphrase = passphrase

    def load(self):
        """ Load keyring from a file

        Returns: boolean result
        """
        data = None
        with open(self._filepath, "rb") as f:
            data = Security.decrypt(self._passphrase, f.read())
        try:
            saved_content = pickle.loads(data)
        except Exception as e:
            return False

        if saved_content.get("version", "") == "1.0":
            self._accounts = saved_content.get("accounts", [])
        else:
            return False

        debug("Keyring loaded")
        return True

    def save(self):
        """ Save keyring in a file

        Returns: boolean result
        """
        saved_content = { "version": "1.0", "accounts": self._accounts}
        data = pickle.dumps(saved_content)
        raw = Security.encrypt(self._passphrase, data)
        if not raw:
            return False

        with open(self._filepath, "wb") as f:
            f.write(raw)

        debug("Keyring saved")
        return True

    def add_account(self, name, password):
        """ Add a new item to account list and save keyring

        Args:
            name: new account name
            password: new account password

        Returns: boolean result
        """
        self._accounts.append(Account(name, password))
        return self.save()

    def rm_account(self, account):
        """ Remove an existing item from account list and save keyring

        Args:
            account: account to remove

        Returns: boolean result
        """
        self._accounts.remove(account)
        return self.save()

    def find_account(self, search_str):
        """ Search for an item in account list

        Args:
            search_str: search string, exact match or starting with

        Returns: a list of matching accounts
        """
        res = []
        if not search_str:
            return res

        for account in self._accounts:
            if account.name == search_str:
                # Exact match: empty result list and return
                res = [ account ]
                break
            if account.name.startswith(search_str):
                # Partial match: populate result list
                res.append(account)

        return res
