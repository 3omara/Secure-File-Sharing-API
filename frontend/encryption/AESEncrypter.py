from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from encryption.Encrypter import Encrypter


class AESEncrypter(Encrypter):
    @property
    def BLOCK_SIZE(self) -> int:
        return AES.block_size

    def generate_key(self) -> bytes:
        return get_random_bytes(16)

    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        plaintext = pad(plaintext, self.BLOCK_SIZE)
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return unpad(plaintext, self.BLOCK_SIZE)
