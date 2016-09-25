from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class RSAEncryptor(object):

    def __init__(self, keyfile, passphrase=None):
        self.keyfile = keyfile
        self.passphrase = passphrase

    def encrypt(self, data):
        with open(self.keyfile, 'r') as handle:
            key = RSA.importKey(handle.read(), self.passphrase)
            chiper = PKCS1_OAEP.new(key)
            return chiper.encrypt(data)

    def decrypt(self, data):
        with open(self.keyfile, 'r') as handle:
            key = RSA.importKey(handle.read(), self.passphrase)
            chiper = PKCS1_OAEP.new(key)
            return chiper.decrypt(data)

    def hash(self, key):
        return SHA512.new(key)
