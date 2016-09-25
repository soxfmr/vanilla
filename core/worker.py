import Queue
import logging
import threading


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
            logging.error('Exception in receive thread: %s', str(e))
        finally:
            self.__stop()

    def __send(self):
        try:
            while self.running:
                data = self.channel.get()
                self.socket.sendall(data)

                self.channel.task_done()
        except IOError, e:
            logging.error('Exception in sending thread: %s', str(e))
        finally:
            self.__stop()

    def __stop(self):
        with self.lock:
            if self.running and self.socket:
                self.running = False

                self.socket.close()
                self.socket = None

                logging.info('Client {} out.'.format(self.addr))
