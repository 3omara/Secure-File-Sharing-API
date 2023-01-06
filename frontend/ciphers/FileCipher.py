from typing import Callable, Iterator, List
from itertools import cycle
from ciphers.Cipher import SymmetricCipher


class FileCipher:
    def __init__(self, ciphers: List[SymmetricCipher]):
        self.ciphers = ciphers

    def generate_keys(self) -> List[bytes]:
        return [cipher.generate_key() for cipher in self.ciphers]

    def encrypt(self, read: Callable[[int], bytes], write: Callable[[bytes], int], keys: List[bytes]) -> None:
        cipher_key_pairs = cycle(zip(self.ciphers, keys))
        while (ck := next(cipher_key_pairs)) and (part := read(ck[0].BLOCK_SIZE)):
            write(ck[0].encrypt(part, ck[1]))

    def decrypt(self, read: Callable[[int], bytes], write: Callable[[bytes], int], keys: List[bytes]) -> None:
        cipher_key_pairs = cycle(zip(self.ciphers, keys))
        while (ck := next(cipher_key_pairs)) and (part := read(ck[0].BLOCK_SIZE)):
            write(ck[0].decrypt(part, ck[1]))
