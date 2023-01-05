from abc import ABC


class Encrypter(ABC):
    @property
    def BLOCK_SIZE(self) -> int:
        pass

    def generate_key(self) -> bytes:
        pass

    def encrypt(self, plaintext: str, key: bytes) -> str:
        pass

    def decrypt(self, ciphertext: str, key: bytes) -> str:
        pass
