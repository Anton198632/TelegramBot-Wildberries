import sys
import os
import threading
import socket
import json
import time


class Logger:

    __IP = '127.0.0.1'
    __PORT = 15000
    __WORK_SIGNAL_PERIOD = 15

    __database = None
    __applicationName = ''
    __sock = None
    __log_some = None
    __log_error = None
    stdout = None
    stderr = None

    def __new__(cls, applicationName, *args, **kwargs):

        if cls.__sock is None:
            # Соединение через socket
            cls.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        cls.__applicationName = applicationName

        cls.__log_some = cls.Log(applicationName, 'regular')
        cls.__log_error = cls.Log(applicationName, 'error')
        cls.stdout = sys.stdout
        cls.stderr = sys.stderr

    class Log:
        def __init__(self, applicationName, type):
            self.applicationName = applicationName
            self.type = type

        def write(self, text):
            if text != '\n':
                data = {'application_name': self.applicationName, 'type': self.type, 'text': text}
                Logger.write(data)

            # if self.type == 'regular':
            #     Logger.stdout.write(text)
            # if self.type == 'error':
            #     Logger.stderr.write(text)

    @classmethod
    def start(cls):
        sys.stdout = cls.__log_some
        sys.stderr = cls.__log_error

        task = threading.Thread(target=cls.__work_signal)
        task.start()

    @classmethod
    def stop(cls):
        sys.stdout = cls.stdout
        sys.stderr = cls.stderr

    @classmethod
    def write(cls, data):
        cls.__sock.sendto(bytes(json.dumps(data), 'utf-8'), (cls.__IP, cls.__PORT))

    @classmethod
    def __work_signal(cls):
        while True:
            data = {'application_name': cls.__applicationName, 'type': 'service', 'text': 'is work'}
            cls.write(data)
            time.sleep(cls.__WORK_SIGNAL_PERIOD)
