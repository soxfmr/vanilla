import logging
import threading
from socket import *
from worker import Worker
from dispatcher import Dispatcher


class Server(object):

    def __init__(self, addr, encryptor=None, middlewares=dict()):
        self.addr = addr
        self.encryptor = encryptor
        self.middlewares = middlewares

        self.server = None
        self.listen_thread = None

    def start(self):
        self.server = socket(family=AF_INET, type=SOCK_STREAM, proto=0)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.server.bind(self.addr)
        self.server.listen(100)

        self.listen_thread = threading.Thread(target=self.__handle)
        self.listen_thread.setDaemon(True)
        self.listen_thread.start()

        logging.info('Server running: {}'.format(self.addr))

    def wait(self):
        while True:
            self.listen_thread.join(1024)
            if not self.listen_thread.isAlive():
                break

            time.sleep(1)

    def stop(self):
        if self.server:
            self.server.close()
            logging.info('Server quit')

    def __handle(self):
        try:
            while True:
                client, addr = self.server.accept()
                logging.info('Client join: %s', str(addr))

                # Go to ask for hr if he let you go
                thread = threading.Thread(target=self.__hr, args=(client, addr))
                thread.setDaemon(True)
                thread.start()
        except IOError, e:
            logging.error('Exception in handle thread: %s', str(e))


    def __hr(self, client, addr):
        for name, middleware in self.middlewares.items():
            if middleware.denied(client, addr):
                logging.warn('Client {} auth failed in middleware {}'.format( addr, name ))

                client.close()
                logging.info('Client {} out.'.format(addr))

                return False

        worker = Worker(client, addr, Dispatcher(self.encryptor))
        worker.run()

        logging.info('Client {} auth successfully, worker thread started'.format( addr ))
