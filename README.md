__Minpass__ is a minimalistic cross-platform password manager.

__Generate__ and __store__ your account passwords in secured keyring files, then get your passwords in your clipboard.

You only need to remember a master passphrase per keyring.

* Choose passphrases wisely (if you manage a lot of keyrings you may want to store passphrases in a super keyring)
* Save your keyrings in multiple places
* Optional: configure encryption in a single config.json file located in your working directory

## Requirements

* linux: python3 python3-tk python3-crypto
* windows: a packaged python3 installation such as anaconda

## Example

```
./minpass.py example.sav
Loading configuration from config.json
example.sav does not exist. Create new? [Y/n] 
Enter passphrase: 
Re-enter passphrase: 
New keyring saved in example.sav
example.sav $ help
add account_name - register a new account
chpp  - change keyring passphrase
exit  - exit program
get account_name - copy account password into clipboard
help  - print help
ls  - list all accounts (names only)
print account_name - (use with caution) print complete account, including password
rm account_name - remove account
example.sav $ add yahoo/john.doe
Generate password? [Y/n] 
Generating yahoo/john.doe password...
Clipboard updated with yahoo/john.doe password
example.sav $ add yahoo/jane.doe
Generate password? [Y/n] 
Generating yahoo/jane.doe password...
Clipboard updated with yahoo/jane.doe password
example.sav $ get yahoo
Multiple accounts found:
yahoo/john.doe
yahoo/jane.doe
example.sav $ get yahoo/john
Clipboard updated with yahoo/john.doe password
example.sav $ exit
Reminder: if passwords were printed on screen, remember to reset your console output (linux: clear, windows: cls)
```
