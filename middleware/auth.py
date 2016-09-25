import time

class Auth(object):

    def __init__(self, key, encryptor, timeout=8):
        self.key = encryptor.hash(key)
        self.encryptor = encryptor
        self.timeout = timeout

    def denied(self, client, addr):
        bRet = True
        try:
            # Do not block the recv function, and drop the connection after timeout
            client.settimeout(self.timeout)
            keydata = client.recv(4096)

            if keydata:
                # Not equals, connection will be drop
                bRet = self.encryptor.decrypt(keydata) != self.key
        finally:
            # Restore in blocking mode
            if client: client.setblocking(1)

        return bRet
