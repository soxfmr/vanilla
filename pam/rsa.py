from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS


class RSAEncryptor(object):

    def __init__(self, key, keyfile, passphrase=None):
        self.key = key
        self.keyfile = keyfile
        self.passphrase = passphrase

    def encrypt(self, data=None):
        with open(self.keyfile, 'r') as handle:
            key = RSA.importKey(handle.read(), self.passphrase)
            encryptor = PKCS1_PSS.new(key)
            return encryptor.sign( self.hash( self.key ) )

    def decrypt(self, data=None):
        pass

    def verify(self, keydata):
        with open(self.keyfile, 'r') as handle:
            key = RSA.importKey(handle.read(), self.passphrase)
            encryptor = PKCS1_PSS.new(key)
            return encryptor.verify( self.hash( self.key ) )

    def hash(self, key):
        return SHA512.new(key)
