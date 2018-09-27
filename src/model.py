import json
import base64
import nacl.secret
import nacl.utils
import nacl.encoding
import nacl.hash


class SecretDictionary(object):

    # -------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -------------------------------------------------------------------------
    def __init__(self, secrete_key):
        self.protected_data = {}
        self.hash_impl = nacl.hash.sha256
        self.secure_box = nacl.secret.SecretBox(self.__hash_secret_key(secrete_key.encode('utf-8')))

    @property
    def data(self):
        return self.protected_data

    def add_secret(self, name, value):
        self.protected_data[name] = value

    # -------------------------------------------------------------------------
    # METHOD CURRENT DATA STATE
    # -------------------------------------------------------------------------
    def __current_data_state(self) -> str:
        return json.dumps(self.protected_data)

    # -------------------------------------------------------------------------
    # METHOD HASH SECRET KEY
    # -------------------------------------------------------------------------
    def __hash_secret_key(self, key):
        return self.hash_impl(key, encoder=nacl.encoding.RawEncoder)

    # -------------------------------------------------------------------------
    # CLASS CURRENT DATA STATE
    # -------------------------------------------------------------------------
    def lock(self) -> str:
        encrypted_data = self.secure_box.encrypt(self.__current_data_state().encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')

    # -------------------------------------------------------------------------
    # CLASS CURRENT DATA STATE
    # -------------------------------------------------------------------------
    def unlock(self, locked_secret):
        cipher_bytes = base64.b64decode(locked_secret.encode('utf-8'))
        dict_str = self.secure_box.decrypt(cipher_bytes).decode('utf-8')
        self.protected_data = json.loads(dict_str)

