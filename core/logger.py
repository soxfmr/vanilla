import time
import logging
from os import path
from os import mkdir

def initlog(level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(module)s - %(message)s',
        '%Y-%m-%d %H:%I:%S')

    if not path.exists('log'):
        mkdir('log')

    # Log to file
    fileHandler = logging.FileHandler(filename='log/server-log-{}.log'.format( \
        time.strftime('%Y-%m-%d', time.localtime())))
    fileHandler.setFormatter(formatter)

    # Log to stdout
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    rootLogger = logging.getLogger()

    rootLogger.addHandler(fileHandler)
    rootLogger.addHandler(streamHandler)
    rootLogger.setLevel(level)
