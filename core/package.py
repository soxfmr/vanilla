import zlib
from struct import pack
from struct import unpack
from struct import calcsize


'''
    Action package format:
    +--------------------------------------------------------------------------------------------------+
    | Magic Word 4 bytes | Data Length 4 bytes | Request id | Request Module | Module Action | Variant |
    +--------------------------------------------------------------------------------------------------+
'''

PACKAGE_MAGIC_WORD = '\x01\x22\x33\x01'

FMT_PACKAGE_MAGIC_WORD = '>I'
FMT_PACKAGE_DATA_LENGTH = '<I'

LEN_PACKAGE_MAGIC_WORD = calcsize(FMT_PACKAGE_MAGIC_WORD)
LEN_PACKAGE_DATA_LENGTH = calcsize(FMT_PACKAGE_DATA_LENGTH)

LEN_PRE_REQUIREMENT = LEN_PACKAGE_MAGIC_WORD + LEN_PACKAGE_DATA_LENGTH

class PackageBuilder(object):

    def __init__(self, data=None, encryptor=None):
        self.uid = 0
        self.length = 0
        self.data = data
        self.encryptor = encryptor

    def append(self, data):
        if not self.data:
            self.data = data
            return

        self.data += data

    def iscomplete(self):
        if not self.data:
            return False

        length = len(self.data)
        if not self.length and length >= LEN_PRE_REQUIREMENT:
            self.length = unpack(FMT_PACKAGE_DATA_LENGTH, self.data[LEN_PACKAGE_MAGIC_WORD:LEN_PACKAGE_DATA_LENGTH])
            self.data = self.data[LEN_PRE_REQUIREMENT:] if length > LEN_PRE_REQUIREMENT \
                else None

        return self.length >= len(self.data)

    def unpack(self):
        if not self.data:
            raise ValueError('Invalid data to unpack')

        if len(self.data) < self.length:
            raise ValueError('Incomplete package to unpack')

        # Decrypt
        data = self.encryptor.decrypt(data) if self.encryptor else \
            self.data
        # Decompress
        data = zlib.decompress(data)

        self.uid, module, action, params = self.data.split('|', 3)
        return (module, action, params)

    def redraw(self, data):
        if not self.uid:
            raise ValueError('Invalid request id to reuse')

        data = '{}|{}'.format(self.uid, data)
        return self.__build(data)


    def build(self, module, action, params):
        # Request id
        self.uid = self.uid + 1 if self.uid < 0xffff else 1
        # Compose package data
        data = '{}|{}|{}|{}'.format(self.uid, module, action, params)

        return (self.uid, self.__build(data))

    def __build(self, data):
        # Compress
        data = zlib.compress(data)
        # Encrypt
        if self.encryptor:
            data = self.encryptor.encryt(data)

        return '{}{}{}'.format( pack(FMT_PACKAGE_MAGIC_WORD, PACKAGE_MAGIC_WORD),
            pack(FMT_PACKAGE_DATA_LENGTH, len(data)), data)

    @staticmethod
    def isnewpackage(data):
        '''
        The result will be false if the length of package less than size of magic word
        '''
        return len(data) >= LEN_PACKAGE_MAGIC_WORD and \
            unpack(FMT_PACKAGE_MAGIC_WORD, data[:LEN_PACKAGE_MAGIC_WORD]) == PACKAGE_MAGIC_WORD
