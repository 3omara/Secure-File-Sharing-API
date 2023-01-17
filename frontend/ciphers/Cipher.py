from abc import ABC, abstractmethod
from Crypto.Util.Padding import pad, unpad


class SymmetricCipher(ABC):
    @property
    @abstractmethod
    def BLOCK_SIZE(self) -> int:
        pass

    @property
    @abstractmethod
    def KEY_SIZE(self) -> int:
        pass

    @abstractmethod
    def generate_key(self) -> bytes:
        pass

    @abstractmethod
    def encrypt(self, plaintext: str, key: bytes) -> str:
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str, key: bytes) -> str:
        pass

    def pad(self, plaintext: bytes) -> bytes:
        if len(plaintext) % self.BLOCK_SIZE != 0:
            plaintext = pad(plaintext, self.BLOCK_SIZE)
        return plaintext

    def unpad(self, plaintext: bytes) -> bytes:
        try:
            return unpad(plaintext, self.BLOCK_SIZE)
        except ValueError:
            return plaintext
