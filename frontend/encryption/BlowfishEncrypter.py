from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from encryption.Encrypter import Encrypter


class BlowfishEncrypter(Encrypter):
    @property
    def BLOCK_SIZE(self) -> int:
        return Blowfish.block_size

    def generate_key(self) -> bytes:
        return get_random_bytes(Blowfish.key_size[0])

    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        plaintext = pad(plaintext, self.BLOCK_SIZE)
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return unpad(plaintext, self.BLOCK_SIZE)
