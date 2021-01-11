import sys
from grove.gpio import GPIO
from func.threading import threaded
import time

usleep = lambda x: time.sleep(x / 1000000.0)
 
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000
 
class LED(object):
    led = None
    blinking = False
    thread = None
 
    def __init__(self, _pin):
        self.led = GPIO(_pin, GPIO.OUT)
        self.thread = self.thread_blink()
 
    def blink(self):
        self.blinking = True
 
    def stop_blink(self):
        self.blinking = False
        self.led.write(0)

    @threaded
    def thread_blink(self):
        while True:
            if self.blinking:
                self.led.write(1)
                time.sleep(1)
                self.led.write(0)
                time.sleep(1)
            else:
                time.sleep(1)
 
class Button(object):
    button = None
    pressed = False
    callback = None

    def __init__(self, _pin, _callback = None):
        # High = pressed
        self.button = GPIO(_pin, GPIO.IN)
        self.callback = _callback
        self.thread_button()
    
    @threaded
    def thread_button(self):
        while True:
            time.sleep(1)
            if self.button.read():
                if not self.pressed:
                    self.pressed = True
                    if self.callback:
                        self.callback()
            else:
                self.pressed = False

class GroveUltrasonicRanger(object):
    def __init__(self, _pin):
        self.dio =GPIO(_pin)
 
    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)
 
        self.dio.dir(GPIO.IN)
 
        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None
 
        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None
 
        t2 = time.time()
 
        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None
 
        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm
 
        return distance
 
    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist
 