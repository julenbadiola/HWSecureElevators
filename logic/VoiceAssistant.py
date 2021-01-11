import os
from func.Singleton import SingletonMeta
from func.threading import threaded
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
                    #print(f"VOICEASSIST: Saying {tosay}")
                    #El "ei" es porque si no, no se reproduce bien
                    os.system(f'pico2wave -l es-ES -w temp.wav "ei. {tosay}" && aplay temp.wav > /dev/null 2>&1')
                    del self.pool[0]