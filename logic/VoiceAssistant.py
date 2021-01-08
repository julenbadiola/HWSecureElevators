import random
import sys
import time
import os
from logic.Singleton import SingletonMeta
from logic.threading import threaded
from time import sleep

class VoiceAssistant(metaclass=SingletonMeta):
    pool = []
    main_thread = None

    @property
    def status(self):
        if self.main_thread:
            return self.main_thread.is_alive()
        return False

    def __init__(self, elevator):
        self.elevator = elevator
        self.main_thread = self.thread_check_pool()
        
    def add_to_pool(self, string):
        self.pool.append(string)

    @threaded
    def thread_check_pool(self):
        while True:
            sleep(1)
            if len(self.pool) > 0:
                tosay = self.pool[0]
                if tosay:
                    print(f"VOICEASSIST: Saying {tosay}")
                    os.system(f'pico2wave -w temp.wav "{tosay}" && aplay temp.wav')
                    del self.pool[0]