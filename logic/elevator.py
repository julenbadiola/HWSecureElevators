import json
from logic.singleton import SingletonMeta
from func.properties import Properties

class Elevator(metaclass=SingletonMeta):
    code = None
    config = None
    functionalities = []
    floors = []
    capacity = None

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
            self.floors = json.loads(self.config['DEFAULT']['FUNCTIONALITIES'])
            self.capacity = int(self.config['DEFAULT']['CAPACITY'])
            return True
        except Exception as e:
            raise e
            return False

    #BUSINESS LOGIC
    def call(self, where):
        print(f"ELEV: Going to {where}")
        try:
            self.where = self.floors[where]
        
        except Exception as e:
            self.status = False
