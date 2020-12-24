import json
from logic.singleton import SingletonMeta
from func.properties import Properties
from time import sleep

class Elevator(metaclass=SingletonMeta):
    code = None
    config = None
    functionalities = []
    floors = []
    capacity = None

    calls_pool = []
    where = None
    status = False

    #INITIALIZATION
    def __init__(self, code):
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            self.status = True
            print("ELEV: Started successfully")
        else:
            self.status = False
            print("ELEV: Error")
        #Go to first floor
        self.call(0)

    def activate(self):
        self.config = Properties().get_elevator_configuration_from_backend()
        if not self.config:
            self.config = Properties().get_elevator_configuration_from_file()
        return self.apply_config()

    def apply_config(self):
        try:
            self.functionalities = json.loads(self.config['DEFAULT']['FUNCTIONALITIES'])
            self.floors = json.loads(self.config['DEFAULT']['FLOORS'])
            self.capacity = int(self.config['DEFAULT']['CAPACITY'])
            return True
        except Exception as e:
            raise e
            return False

    #BUSINESS LOGIC
    def call(self, where):
        if(self.floors[where] == True):
            print(f"ELEV: Elevator called in {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False
        else:
            print(f"ELEV: Elevator called in disabled floor - {where}")

    def ride(self):
        print(len(self.calls_pool))
        if len(self.calls_pool) > 0:
            
            ride = self.calls_pool[0]
            
            indexFrom = self.floors.index(self.where)
            indexTo = self.floors.index(toFloor)
            diff = abs(indexFrom - indexTo)

            print(f"ELEV: Ride to {ride} {indexFrom} {indexTo} {diff}.")
            for i in range(1, diff):
                print(f"ELEV: Ride to {ride}. Now in {i}")
                sleep(1)

            self.where = self.floors[where]
            self.calls_pool.remove(ride)
            print(f"ELEV: Ride to {ride} finished.")