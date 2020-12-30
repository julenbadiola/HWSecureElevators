import json
from logic.singleton import SingletonMeta
from properties.properties import PropertiesManager
from time import sleep
from speech.speechmanager import recognize_speech_from_mic, say

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
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            self.status = True
            print("ELEV: Status = successful.")
        else:
            self.status = False
            print("ELEV: Status = error.")        

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

    #BUSINESS LOGIC
    def call(self, where):
        if(self.floors[where] == True):
            print(f"ELEV: Elevator called in {where}")
            say(f"Elevador llamado en el piso {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False
        """else:
            print(f"ELEV: Elevator called from or to disabled floor - {where}")"""

    def check_calls(self):
        if not self.riding and len(self.calls_pool) > 0:
            print(f"ELEV: {self.calls_pool}.")
            toFloor = self.calls_pool[0]
            if toFloor is not None:
                self.ride(toFloor)
        """else:
            print(f"ELEV: There are not rides.")"""

    def ask_for_input(self):
        pass

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
            self.riding = True
            for i in range(0, diff):
                sleep(5)
                say(f"Elevador yendo a {floor}. Ahora en {i}")
                print(f"ELEV: Riding to {floor}. Now in {i}")

            print(f"ELEV: Ride to {floor} finished.")
            self.where = floor
        
        self.calls_pool.remove(floor)
        self.riding = False
        