from abc import ABC, abstractmethod


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
