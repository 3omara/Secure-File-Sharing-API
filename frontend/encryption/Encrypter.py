from abc import ABC


class Encrypter(ABC):
    def encrypt(self, plaintext: str, key: str) -> str:
        pass

    def decrypt(self, ciphertext: str, key: str) -> str:
        pass
