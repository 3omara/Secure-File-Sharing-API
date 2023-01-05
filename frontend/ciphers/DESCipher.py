from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from ciphers.Cipher import SymmetricCipher


class DESCipher(SymmetricCipher):
    @property
    def BLOCK_SIZE(self) -> int:
        return DES.block_size

    @property
    def KEY_SIZE(self) -> int:
        return DES.key_size

    def generate_key(self) -> bytes:
        return get_random_bytes(self.KEY_SIZE)

    def encrypt(self, plaintext: bytes, key: bytes) -> str:
        plaintext = pad(plaintext, self.BLOCK_SIZE)
        cipher = DES.new(key, DES.MODE_ECB)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes, key: bytes) -> str:
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return unpad(plaintext, self.BLOCK_SIZE)
