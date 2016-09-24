import time
from socket import *

client = socket(family=AF_INET, type=SOCK_STREAM, proto=0)
client.connect(('127.0.0.1', 8080))

try:
    while True:
        client.sendall('transform')
        print client.recv(4096)

        time.sleep(2)
except KeyboardInterrupt:
    pass

client.close()
