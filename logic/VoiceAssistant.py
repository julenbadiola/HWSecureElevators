import random
import sys
import time
import os
import speech_recognition as sr
import pyaudio

from logic.Singleton import SingletonMeta
from logic.threading import threaded
from func.numparser import Text2Int

from time import sleep

class VoiceAssistant(metaclass=SingletonMeta):
    pool = []
    threads = []
    status = False

    def __init__(self):
        self.status = True
        self.elevator = Elevator()
        self.threads.append(self.thread_check_pool())

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

    def ask_for_keyboard_input(self):
        print('A qué piso quieres ir:')
        x = input()
        self.elevator.ride(int(x))

    def ask_for_voice_input(self):
        r = sr.Recognizer()
        speech = sr.Microphone(device_index=0)
        self.add_to_pool("Pronuncie a qué piso desea ir")
        with speech as source:
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            recog = r.recognize_google(audio, language='es-ES')
            floor = Text2Int(recog)
            print("Yendo al piso " + str(floor))
            self.add_to_pool("Entendido. Te mando al piso " + str(floor))
            self.elevator.ride(floor)

        except sr.UnknownValueError:
            self.add_to_pool("No he entendido. Pulse los botones.")
            self.ask_for_keyboard_input()

        except sr.RequestError as e:
            self.add_to_pool(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            self.ask_for_keyboard_input()


def print_available_micros():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ",
                  p.get_device_info_by_host_api_device_index(0, i).get('name'))
