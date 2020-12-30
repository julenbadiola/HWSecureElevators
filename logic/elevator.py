import json

from properties.properties import PropertiesManager
from time import sleep

from logic.Singleton import SingletonMeta
from logic.VoiceAssistant import VoiceAssistant
from logic.threading import threaded
from time import sleep

class Elevator(metaclass=SingletonMeta):
    code = None
    config = None
    functionalities = []
    floors = []
    capacity = None
    status = False

    #Functionality
    calls_pool = []
    where = 0
    threads = []
    riding = False

    #INITIALIZATION
    def __init__(self, code):
        self.voiceAssistant = VoiceAssistant()
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            self.status = True
            print("ELEV: Status = successful.")
        else:
            self.status = False
            print("ELEV: Status = error.")   
        self.thread_check_calls()     
    
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

    @threaded
    def thread_check_calls(self):
        while True:
            sleep(1)
            if not self.riding and len(self.calls_pool) > 0:
                print(f"ELEV: {self.calls_pool}.")
                toFloor = self.calls_pool[0]
                if toFloor is not None:
                    self.ride(toFloor)
            """else:
                print(f"ELEV: There are not rides.")"""

    #BUSINESS LOGIC
    def call(self, where):
        if(self.floors[where] == True):
            print(f"ELEV: Elevator called in {where}")
            self.voiceAssistant.add_to_pool(f"Elevador llamado en el piso {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False
        """else:
            print(f"ELEV: Elevator called from or to disabled floor - {where}")"""

    def ask_for_input(self):
        pass
    
    def lock(self):
        self.riding = True

    def unlock(self):
        self.riding = False

    def ride(self, floor):
        if(floor == None):
            return

        indexFrom = self.floors.index(self.where)
        indexTo = self.floors.index(floor)
        
        if(self.floors[floor] == False):
            print(f"ELEV: The floor {floor} is disabled.")

        elif(indexFrom == indexTo):
            print(f"ELEV: Elevator already on floor {floor}.")

        else:
            diff = abs(indexFrom - indexTo)
            self.lock()
            for i in range(0, diff):
                sleep(5)
                self.voiceAssistant.add_to_pool(f"Elevador yendo a {floor}. Ahora en {i}")
                print(f"ELEV: Riding to {floor}. Now in {i}")

            print(f"ELEV: Ride to {floor} finished.")
            self.where = floor
            print(f"ELEV: Estás en {floor}.")
            self.voiceAssistant.ask_for_voice_input()
        
        self.calls_pool.remove(floor)
        
        