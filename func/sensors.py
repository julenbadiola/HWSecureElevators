import sys
from grove.gpio import GPIO
from func.threading import threaded
import time
from grove.button import Button
from grove.factory import Factory
 
usleep = lambda x: time.sleep(x / 1000000.0)
 
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000
 
class LED(object):
    led = None
    blinking = False
    thread = None
 
    def __init__(self, PIN):
        self.led = GPIO(PIN, GPIO.OUT)
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
 
class GroveButton(object):
    pressed = False

    def __init__(self, pin):
        # High = pressed
        self.__btn = Factory.getButton("GPIO-HIGH", pin)
        self.__last_time = time.time()
        self.__on_press = None
        self.__on_release = None
        self.__btn.on_event(self, GroveButton.__handle_event)
 
    @property
    def on_press(self):
        print("PRESSED BUTTON")
        self.pressed = True
        return self.__on_press

    @on_press.setter
    def on_press(self, callback):
        if not callable(callback):
            return
        self.__on_press = callback
 
    @property
    def on_release(self):
        print("RELEASED BUTTON")
        self.pressed = False
        return self.__on_release
 
    @on_release.setter
    def on_release(self, callback):

        if not callable(callback):
            return
        self.__on_release = callback
 
    def __handle_event(self, evt):
        dt, self.__last_time = evt["time"] - self.__last_time, evt["time"]
        # print("event index:{} event:{} pressed:{}".format(evt["index"], evt["code"], evt["pressed"]))
        if evt["code"] == Button.EV_LEVEL_CHANGED:
            if evt["pressed"]:
                if callable(self.__on_press):
                    self.__on_press(dt)
            else:
                if callable(self.__on_release):
                    self.__on_release(dt)

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio =GPIO(pin)
 
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
 