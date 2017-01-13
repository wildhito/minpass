import json
import os


class Config(object):
    """ Module configuration
    """
    def __init__(self, config_path="config.json"):
        user_config = {}
        if os.path.exists(config_path):
            print("Loading configuration from %s" % config_path)
            with open(config_path) as f:
                user_config = json.load(f)
        else:
            print("No config found")

        # Load user defined values or set default values
        self._pbkdf2_hmac_algo = user_config.get("pbkdf2_hmac_algo", 'sha256')
        self._pbkdf2_rounds = user_config.get("pbkdf2_rounds", 100000)
        self._pbkdf2_dklen = user_config.get("pbkdf2_dklen", 32)
        self._pbkdf2_salt_algo = user_config.get("pbkdf2_salt_algo", 'sha256')
        self._aes_counter_length = user_config.get("aes_counter_length", 128)
        self._aes_counter_initial_value = user_config.get(
                                        "aes_counter_initial_value", 89012345)

    @property
    def pbkdf2_hmac_algo(self):
        return self._pbkdf2_hmac_algo

    @property
    def pbkdf2_rounds(self):
        return self._pbkdf2_rounds

    @property
    def pbkdf2_dklen(self):
        return self._pbkdf2_dklen

    @property
    def pbkdf2_salt_algo(self):
        return self._pbkdf2_salt_algo

    @property
    def aes_counter_length(self):
        return self._aes_counter_length

    @property
    def aes_counter_initial_value(self):
        return self._aes_counter_initial_value
