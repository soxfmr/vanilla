import time
import Queue
import threading
from socket import *
from package import isnewpackage
from package import PackageBuilder
from middleware.auth import Auth
from middleware.shield import Shield

lock = threading.Lock()

def log(message):
    with lock:
        print message

def import_modules():
    pass

class ModuleFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def addModule(self, method):
        pass

    @staticmethod
    def createModule(self, mdoule):
        pass

class Dispatcher(object):

    def __init__(self, encryptor):
        self.encryptor = encryptor
        self.lastpkg = None
        self.channel = None

    def setchannel(self, channel):
        self.channel = channel

    def dispatch(self, data):
        if isnewpackage(data):
            if self.lastpkg:
                log('[-] New package present, previous package deprecated.')
            self.lastpkg = PackageBuilder(data, self.encryptor)
        else:
            if not self.lastpkg:
                log('[-] Incomplete package, discarded.')
                return
            self.lastpkg.append(data)

        if self.lastpkg.iscomplete():
            module, action, params = self.lastpkg.unpack()

            module = ModuleFactory.createModule(module)
            result = module.execute(action, params)

            if result: self.channel.put(result)

        # marked
        self.lastpkg = None
        # log('[+] Receive: ' + data)

class Worker(threading.Thread):

    def __init__(self, socket, addr, dispatcher):
        threading.Thread.__init__(self)

        self.socket = socket
        self.addr = addr

        self.channel = Queue.Queue()
        self.running = True
        self.lock = threading.Lock()

        self.dispatcher = dispatcher
        self.dispatcher.setchannel(self.channel)

    def run(self):
        self.__start()

    def __start(self):
        threads = ( threading.Thread(target=self.__receive),
            threading.Thread(target=self.__send) )

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        for thread in threads:
            thread.join()

    def __receive(self):
        try:
            while self.running:
                data = self.socket.recv(4096)
                if not data:
                    self.__stop()
                    break

                self.dispatcher.dispatch(data)
        except IOError, e:
            log('[-] Exception in receive thread:' + str(e))
        finally:
            self.__stop()

    def __send(self):
        try:
            while self.running:
                data = self.channel.get()
                self.socket.sendall(data)

                self.channel.task_done()
        except IOError, e:
            log('[-] Exception in sending thread:' + str(e))
        finally:
            self.__stop()

    def __stop(self):
        with self.lock:
            if self.running and self.socket:
                self.running = False

                self.socket.close()
                self.socket = None

                log('[-] Client out.')

class Server(object):

    def __init__(self, addr, encryptor=None, middlewares=dict()):
        self.addr = addr
        self.encryptor = encryptor
        self.middlewares = middleware

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

        log('[+] Server running: ' + str(self.addr))

    def wait(self):
        while True:
            self.listen_thread.join(1024)
            if not self.listen_thread.isAlive():
                break

            time.sleep(1)

    def stop(self):
        if self.server:
            self.server.close()
            log('[+] Server quit')

    def __handle(self):
        try:
            while True:
                client, addr = self.server.accept()
                # Go to ask for hr if he let you go
                thread = threading.Thread(target=self.__hr, args=(client, addr))
                thread.setDaemon(True)
                thread.start()

                log('[+] Client join: ' + str(addr))
        except IOError, e:
            log('[-] Exception in handle thread: ' + str(e))


    def __hr(self, client, addr):
        for name, middleware in self.middlewares.items():
            if middleware.denied(client, addr):
                log('[-] Client {} Auth failed in middleware {}'.format( addr, name ))

        work = Worker(client, addr, Dispatcher(self.encryptor))
        work.setDaemon(True)
        work.start()

        log('[+] Client {} auth successfully, worker thread started'.format( addr ))
try:
    middlewares = { 'shield' : Shield(), 'auth' : Auth() }
    server = Server(addr=('0.0.0.0', 8080), middlewares=middlewares)
    server.start()
    server.wait()
except KeyboardInterrupt:
    print '[-] User abort'
finally:
    server.stop()
