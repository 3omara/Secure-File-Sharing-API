from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class RSACipher:
    def generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return public_key, private_key

    def encrypt(self, public_key: bytes, master_key: bytes) -> bytes:
        public_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_master_key = cipher_rsa.encrypt(master_key)
        return enc_master_key

    def decrypt(self, private_key: bytes, enc_master_key: bytes) -> bytes:
        private_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        dec_master_key = cipher_rsa.decrypt(enc_master_key)
        return dec_master_key
