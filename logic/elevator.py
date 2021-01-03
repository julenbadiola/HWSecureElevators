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

    #Functionality
    calls_pool = []
    where = 0
    threads = []
    riding = False
    
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
        self.threads.append(self.thread_check_calls())  
    
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

    @property
    def overall_status(self):
        return self.status and self.voice_assistant.status

    @threaded
    def thread_check_calls(self):
        while True:
            sleep(1)
            if not self.riding and len(self.calls_pool) > 0:
                #print(f"ELEV: {self.calls_pool}.")
                toFloor = self.calls_pool[0]
                if toFloor is not None:
                    self.ride(toFloor)
            """else:
                print(f"ELEV: There are not rides.")"""

    #BUSINESS LOGIC
    def open_doors(self):
        self.voice_assistant.add_to_pool("Abriendo cabina.")
        sleep(2)
        self.doors_open = True
    
    def close_doors(self):
        self.voice_assistant.add_to_pool("Cerrando cabina.")
        sleep(2)
        self.doors_open = False
    
    def lock(self):
        self.riding = True

    def unlock(self):
        self.riding = False

    def call(self, where):
        if(self.floors[where] == True):
            print(f"ELEV: Elevator called in {where}")
            #self.voice_assistant.add_to_pool(f"Elevador llamado en el piso {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False
        """else:
            print(f"ELEV: Elevator called from or to disabled floor - {where}")"""

    def valid_floor_selection(self, floor):
        if self.floors[floor] == True:
            return True
        else:
            self.voice_assistant.add_to_pool(f"El piso {floor} está inhabilitado.")
            return False

    def add_to_voice_assistant(self, tosay):
        self.voice_assistant.add_to_pool(tosay)

    def wait_for_input(self):
        asyncio.run(wait_voice_input(self))

    def ride(self, floor):
        if (floor == None):
            return

        indexFrom = self.floors.index(self.where)
        indexTo = self.floors.index(floor)
        
        if not self.valid_floor_selection(floor):
            print(f"ELEV: The floor {floor} is disabled.")

        elif(indexFrom == indexTo):
            print(f"ELEV: Elevator already on floor {floor}.")

        else:
            diff = abs(indexFrom - indexTo)
            self.close_doors()
            self.lock()
            self.voice_assistant.add_to_pool(f"Elevador yendo a {floor}.")
            for i in range(0, diff):
                sleep(5)
                #self.voice_assistant.add_to_pool(f"Elevador yendo a {floor}. Ahora en {i}")
                print(f"ELEV: Riding to {floor}. Now in {i}")

            print(f"ELEV: Ride to {floor} finished.")
            self.where = floor
            self.open_doors()
            self.wait_for_input()
        
        try:
            self.calls_pool.remove(floor)
        except Exception as e:
            print(self.calls_pool, " ", floor)
            print(e)
        
        
        