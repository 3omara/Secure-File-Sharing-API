from typing import Callable, Iterator, List
from ciphers.Cipher import SymmetricCipher


class FileCipher:
    def __init__(self, ciphers: List[SymmetricCipher]):
        self.ciphers = ciphers

    def encrypt(self, filepath: str, set_keys: Callable[[List[bytes]], None]) -> Iterator[bytes]:
        keys = [cipher.generate_key() for cipher in self.ciphers]
        set_keys(keys)
        cipher_index = -1

        def next_cipher():
            nonlocal cipher_index
            cipher_index += 1
            cipher_index %= len(self.ciphers)
            return self.ciphers[cipher_index]

        with open(filepath, "rb") as file:
            cipher = next_cipher()
            part = file.read(cipher.BLOCK_SIZE)
            while part:
                part = cipher.encrypt(part, keys[cipher_index])
                yield part
                cipher = next_cipher()
                part = file.read(cipher.BLOCK_SIZE)

    def decrypt(self, filepath: str, keys: List[bytes]) -> Iterator[bytes]:
        cipher_index = -1

        def next_cipher():
            nonlocal cipher_index
            cipher_index += 1
            cipher_index %= len(self.ciphers)
            return self.ciphers[cipher_index]

        with open(filepath, "rb") as file:
            cipher = next_cipher()
            part = file.read(cipher.BLOCK_SIZE)
            while part:
                part = cipher.decrypt(part, keys[cipher_index])
                yield part
                cipher = next_cipher()
                part = file.read(cipher.BLOCK_SIZE)
