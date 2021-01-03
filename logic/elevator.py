import json

from properties.properties import PropertiesManager
from time import sleep

from logic.Singleton import SingletonMeta
from logic.VoiceAssistant import VoiceAssistant
from logic.VoiceRecognition import wait_voice_input
from logic.threading import threaded
from time import sleep
import asyncio

class Elevator(metaclass=SingletonMeta):
    #Static
    code = None
    config = None
    functionalities = []
    floors = []
    capacity = None

    #Dynamic
    status = False
    doors_open = False
    where = 0

    #Functionality
    calls_pool = []
    main_thread = None
    calls_thread = None
    ride_thread = None
    voice_recog_thread = None

    @property
    def overall_status(self):
        return self.status and self.voice_assistant.status and self.main_thread.is_alive()

    @property
    def riding(self):
        return not self.ride_thread == None
    
    def clean_thread(self, t):
        if t != None and not t.is_alive():
            return None
        else:
            return t

    @threaded
    def check_threads(self):
        while True:
            sleep(1)
            #print(self.ride_thread, self.riding)
            #print(self.calls_thread, self.calls_pool)
            self.ride_thread = self.clean_thread(self.ride_thread)

    @threaded
    def thread_check_calls(self):
        while True:
            sleep(1)
            if not self.riding and len(self.calls_pool) > 0:
                #print(f"ELEV: {self.calls_pool}.")
                toFloor = self.calls_pool[0]
                if toFloor is not None:
                    self.ride(False, toFloor)
            """else:
                print(f"ELEV: There are not rides.")"""

    #BUSINESS LOGIC
    def call(self, where):
        if(self.valid_floor_selection(False, where)):
            print(f"ELEV: Elevator called in {where}")
            #self.voice_assistant.add_to_pool(f"Elevador llamado en el piso {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False

    def ask_for_input(self):
        self.voice_recog_thread = self.thread_ask_for_input()
     
    @threaded
    def thread_ask_for_input(self):
        asyncio.run(wait_voice_input(self))

    def ride(self, destination, floor):
        self.ride_thread = self.thread_ride(destination, floor)

    @threaded
    def thread_ride(self, destination, floor):
        if (floor == None):
            return

        indexFrom = self.floors.index(self.where)
        indexTo = self.floors.index(floor)
        
        if not self.valid_floor_selection(False, floor):
            print(f"ELEV: The floor {floor} is disabled.")

        elif(indexFrom == indexTo):
            print(f"ELEV: Elevator already on floor {floor}.")

        else:
            diff = abs(indexFrom - indexTo)
            self.close_doors()
            self.voice_assistant.add_to_pool(f"Elevador yendo a {floor}.")
            for i in range(0, diff):
                sleep(2)
                #self.voice_assistant.add_to_pool(f"Elevador yendo a {floor}. Ahora en {i}")
                print(f"ELEV: Riding to {floor}. Now in {i}")

            self.where = floor
            self.open_doors()
            
            if not destination:
                self.ask_for_input()
            
        
        print(f"ELEV: Ride to {floor} finished.")
        try:
            self.calls_pool.remove(floor)
        except Exception as e:
            #Si tira error es porque no es un call, el ride se ha activado desde el recog o los botones
            pass
    
    ## OTHERS
    def valid_floor_selection(self, voice, floor):
        if floor > len(self.floors) - 1:
            return False

        if self.floors[floor] == True:
            return True
        else:
            if voice:
                self.voice_assistant.add_to_pool(f"El piso {floor} está inhabilitado.")
            return False

    def add_to_voice_assistant(self, tosay):
        self.voice_assistant.add_to_pool(tosay)

    def open_doors(self):
        self.voice_assistant.add_to_pool("Abriendo cabina.")
        sleep(2)
        self.doors_open = True
    
    def close_doors(self):
        self.voice_assistant.add_to_pool("Cerrando cabina.")
        sleep(2)
        self.doors_open = False

    #INITIALIZATION
    def __init__(self, code):
        self.voice_assistant = VoiceAssistant(self)
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            self.status = True
            print("ELEV: Status = successful.")
        else:
            self.status = False
            print("ELEV: Status = error.")   
        
        self.main_thread = self.check_threads()
        self.calls_thread = self.thread_check_calls()
    
    def activate(self):
        config = PropertiesManager().get_elevator_configuration()
        try:
            self.functionalities = json.loads(config['DEFAULT']['FUNCTIONALITIES'])
            self.floors = json.loads(config['DEFAULT']['FLOORS'])
            self.capacity = int(config['DEFAULT']['CAPACITY'])
            return True
        except Exception as e:
            print("ELEV: Could not set configuration. The configuration does not exist or is corrupt.")
            return False 
        
        