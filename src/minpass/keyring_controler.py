from minpass.ui import UI


class KeyringControler(object):
    """ Key high level manipulation
    Manage a keyring with user interactions

    Attributes:
        keyring: a keyring
    """
    def __init__(self, keyring):
        self._keyring = keyring

    @property
    def keyring_name(self):
        return self._keyring.name

    @property
    def accounts(self):
        return self._keyring.accounts
    
    def register_account(self, account_name, password):
        """ Register a new account if it does not already exist in keyring

        Args:
            account_name: new account name
            password: new account password

        Returns: boolean result
        """
        if self._keyring.find_account(account_name):
            print("%s is already registered. Please delete it first." \
                  % account_name)
            return False

        self._keyring.add_account(account_name, password)
        return True

    def remove_account(self, account_input):
        """ Remove an account from keyring with user confirmation

        Args:
            account_input: partial account name
        """
        account = self.get_account(account_input)
        if account and UI.confirm("Remove %s?" % account.name):
            self._keyring.rm_account(account)
            print("%s removed" % account.name)
        else:
            print("Removal aborted")

    def get_account(self, account_input):
        """ Find one account in keyring from a partial user input

        Args:
            account_input: partial account name

        Returns: the matching account if one and only account matches
        """
        accounts = self._keyring.find_account(account_input)
        if not accounts:
            print("No matching account found")
            return None

        if len(accounts) > 1:
            print("Multiple accounts found:")
            for account in accounts:
                print(account.name)
            return None

        return accounts[0]

    def change_passphrase(self):
        """ Change keyring passphrase

        Returns: boolean result
        """
        old_pp = UI.type_secret("current passphrase")
        self._keyring.set_passphrase(old_pp)
        if not self._keyring.load():
            print("Bad passphrase")
            return False

        new_pp = UI.create_secret("new passphrase")
        if not new_pp:
            return False

        self._keyring.set_passphrase(new_pp)
        return self._keyring.save()
