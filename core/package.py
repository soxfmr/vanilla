from struct import pack
from struct import unpack
from struct import calcsize


'''
    Action package format:
    +----------------------------------------------------------------------------------------------------+
    | Magic Word 4 bytes | Data Length 4 bytes | Request Module 2 bytes | Module Action 1 byte | Variant |
    +----------------------------------------------------------------------------------------------------+
'''

PACKAGE_MAGIC_WORD = '\x01\x22\x33\x01'

FMT_PACKAGE_MAGIC_WORD = '>I'
FMT_PACKAGE_DATA_LENGTH = '<I'
FMT_REQUEST_MODUEL = '<H'
FMT_REQUEST_MODULE_ACTION = '<B'

LEN_PACKAGE_MAGIC_WORD = calcsize(FMT_PACKAGE_MAGIC_WORD)
LEN_PACKAGE_DATA_LENGTH = calcsize(FMT_PACKAGE_DATA_LENGTH)
LEN_REQUEST_MODUEL = calcsize(FMT_REQUEST_MODUEL)
LEN_REQUEST_MODULE_ACTION = calcsize(FMT_REQUEST_MODUEL)

class PackageBuilder(object):

    def __init__(self, data, encryptor):
        self.length = 0
        self.encryptor = encryptor
        self.data = data[LEN_PACKAGE_MAGIC_WORD:]

    def append(self, data):
        if not self.data:
            raise ValueError('empty data container')

        self.data += data

    def iscomplete(self):
        if not self.length:
            if len(self.data) >= LEN_PACKAGE_DATA_LENGTH:
                self.length = unpack(FMT_PACKAGE_DATA_LENGTH, self.data[:LEN_PACKAGE_DATA_LENGTH])
                self.data = self.data[LEN_PACKAGE_DATA_LENGTH:]

                if self.data <= 0:
                    raise ValueError('insufficient data length')

        return self.length >= len(self.data)

    def unpack(self):
        if not self.length:
            return

        if len(self.data) < self.length:
            raise Value('Incomplete package to unpack')

        data = self.encryptor.decrypt(data) if self.encryptor else \
            self.data

        module = unpack(FMT_REQUEST_MODUEL, data[:LEN_REQUEST_MODUEL])
        action = unpack(FMT_REQUEST_MODULE_ACTION, data[LEN_REQUEST_MODUEL:\
            LEN_REQUEST_MODULE_ACTION])

        params = data[LEN_REQUEST_MODUEL + LEN_REQUEST_MODULE_ACTION:]

        return (module, action, params)

    def build(self, data):
        pass


def isnewpackage(data):
    '''
    The result will be false if the length of package less than size of magic word
    '''
    return len(data) >= LEN_PACKAGE_MAGIC_WORD and \
        unpack(FMT_PACKAGE_MAGIC_WORD, data[:LEN_PACKAGE_MAGIC_WORD]) == PACKAGE_MAGIC_WORD
