from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from ciphers.Cipher import SymmetricCipher


class BlowfishCipher(SymmetricCipher):
    @property
    def BLOCK_SIZE(self) -> int:
        return Blowfish.block_size

    @property
    def KEY_SIZE(self) -> int:
        return Blowfish.key_size[0]

    def generate_key(self) -> bytes:
        return get_random_bytes(self.KEY_SIZE)

    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        plaintext = self.pad(plaintext)
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return self.unpad(plaintext)
