import hashlib
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Util import Counter
from minpass.config import Config
from minpass.debug import debug


class Security(object):
    __config = Config()  # global private config

    """ Provide AES encryption / decryption and random password generation
    All methods are based on pycrypto module
    """
    @staticmethod
    def __create_aes(passphrase):
        """ Create an AES cipher
        Passphrase is PBKDF2 derivated into a 32-bit length key
        PBKDF2 salt comes from "MP" + reversed passphrase
        Data is encrypted / decrypted with AES CTR
        AES counter is the same for everyone

        Args:
            passphrase: the user passphrase in a string

        Returns:
            an AESCipher object
        """
        debug("Key derivation")
        salt = Security.__salt(bytes("MP" + passphrase[::-1], "utf8"))
        debug("Salt: %s" % salt)
        dk = hashlib.pbkdf2_hmac(Security.__config.pbkdf2_hmac_algo,
                                 bytes(passphrase, "utf8"),
                                 bytes(salt, "utf8"),
                                 Security.__config.pbkdf2_rounds,
                                 dklen=Security.__config.pbkdf2_dklen)

        debug("AES initialization")
        ctr = Counter.new(Security.__config.aes_counter_length,
                      initial_value=Security.__config.aes_counter_initial_value)
        c = AES.new(dk, AES.MODE_CTR, counter=ctr)
        return c

    @staticmethod
    def __salt(source_bytes):
        # Here we use hashlib rather than Crypto.Hash as it provides a
        # simple way to instanciate a given algorithm
        h = hashlib.new(Security.__config.pbkdf2_salt_algo)
        h.update(source_bytes)
        return h.hexdigest()

    @staticmethod
    def __password_chars():
        """ Get a list of all chars (ASCII codes) allowed in a password

        Returns:
            all chars list
        """
        chars = []
        def append(start, end):
            for i in range(start, end):
                chars.append(i)
        append(97, 97 + 26)  # lower letters
        append(65, 65 + 26)  # upper letters
        append(48, 48 + 10)  # numbers
        append(32, 47);append(58, 64);append(91, 91)  # special chars
        append(93, 96);append(123, 126)  # more special chars
        return chars

    @staticmethod
    def decrypt(passphrase, raw):
        """ Decrypt data

        Args:
            passphrase: the user passphrase in a string
            raw: cipher data

        Returns:
            plain data
        """
        c = Security.__create_aes(passphrase)
        debug("Decryption")
        return c.decrypt(raw)

    @staticmethod
    def encrypt(passphrase, data):
        """ Encrypt plain data

        Args:
            passphrase: the user passphrase in a string
            data: plain data

        Returns:
            cipher data
        """
        c = Security.__create_aes(passphrase)
        debug("Encryption")
        return c.encrypt(data)

    @staticmethod
    def generate_password(size=32):
        """ Generate a random password

        Args:
            size: password size

        Returns:
            a random password
        """
        chars = Security.__password_chars()
        password_array = []
        for i in range(0, size):
            password_array.append(random.choice(chars))

        random.shuffle(password_array)

        password = ""
        for i in range(0, len(password_array)):
            password += chr(password_array[i])

        debug("Generated password: %s" % password)
        return password
