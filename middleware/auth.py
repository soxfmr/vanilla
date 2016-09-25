import time

def Auth(object):

    def __init__(self, encryptor, timeout=8):
        self.encryptor = encryptor
        self.timeout = timeout

    def denied(self, client, addr):
        try:
            # Do not block the recv function, and drop the connection after timeout
            client.settimeout(self.timeout)
            keydata = client.recv(4096)

            if not keydata:
                return True
            # Not equals, connection will be drop
            return encryptor.verify(keydata)
        finally:
            # Restore in blocking mode
            if client: client.setblocking(1)

        return True
