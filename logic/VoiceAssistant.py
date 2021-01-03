import random
import sys
import time
import os
from logic.Singleton import SingletonMeta
from logic.threading import threaded
from time import sleep

class VoiceAssistant(metaclass=SingletonMeta):
    pool = []
    thread = None
    status = False

    def __init__(self, elevator):
        self.status = True
        self.elevator = elevator
        self.thread = self.thread_check_pool()
        
    def add_to_pool(self, string):
        self.pool.append(string)

    @threaded
    def thread_check_pool(self):
        while True:
            sleep(1)
            if len(self.pool) > 0:
                tosay = self.pool[0]
                if tosay:
                    os.system(f'say {tosay}')
                    del self.pool[0]