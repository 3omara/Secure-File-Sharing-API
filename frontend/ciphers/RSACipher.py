from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import requests


class RSACipher:
    def generate_keys(self, user_id: str) -> str:
        key = RSA.generate(2048)
        private_key = key.export_key()

        # generating a private key and storing it locally
        file_out = open("private_key.pem", "wb")
        file_out.write(private_key)
        file_out.close()

        # generating a public key and uploading it to the server
        public_key = key.publickey().export_key()
        file_out = open("public_key.pem", "wb")
        file_out.write(public_key)
        file_out.close()

        # upload file holding public key information 
        dictToSend = {'user_id':user_id, 'file_name': 'public_key.pem', 'file_type':0}
        message = requests.post('http://127.0.0.1:5000/api/upload', json=dictToSend)

        return message

    def encrypt(self, public_key: bytes, master_key: bytes) -> bytes:
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_master_key = cipher_rsa.encrypt(master_key)
        return enc_master_key

    def decrypt(self, private_key: bytes, enc_master_key: bytes) -> bytes:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        dec_master_key = cipher_rsa.decrypt(enc_master_key)
        return dec_master_key
