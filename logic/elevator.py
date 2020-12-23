import json
import requests 
import configparser
from properties import GENERAL_URL, ACTIVE_CONFIGURATION_FILE

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Elevator(metaclass=SingletonMeta):
    code = None
    functionalities = []
    floors = []
    capacity = None
    where = None
    status = False
    exceptions = []

    #INITIALIZATION
    def __init__(self, code):
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            print("ELEV: Started successfully")
        else:
            print("ELEV: Error")
        #Go to first floor
        self.call(0)
    
    #ELEVATOR CONFIGURATION STUFF
    @property
    def configuration_url(self):
        return GENERAL_URL + str(self.code)

    def activate(self):
        if self.get_from_backend():
            self.status = True
        elif self.get_config_from_file():
            self.status = True
        else:
            self.status = False
        return self.status

    def get_from_backend(self):
        print(f"ELEV: Getting configuration from backend")
        r = requests.get(url = self.configuration_url) 
        try:
            data = r.json()
            self.functionalities = data['activeFunctionalities']
            self.floors = data['activeFloors']
            self.capacity = data['capacity']
            return self.save_configuration_file()

        except Exception as e:
            raise e
            return False
    
    def save_configuration_file(self):
        print(f"ELEV: Saving configuration file")
        try:
            config = configparser.ConfigParser()
            config['DEFAULT']['FUNCTIONALITIES'] = json.dumps(self.functionalities)
            config['DEFAULT']['FLOORS'] = json.dumps(self.floors)
            config['DEFAULT']['CAPACITY'] = str(self.capacity)

            with open(ACTIVE_CONFIGURATION_FILE, 'w') as configfile:
                config.write(configfile)
            return True

        except Exception as e:
            raise e
            return False

    def get_config_from_file(self):
        print(f"ELEV: Getting configuration from file")
        try:
            config = configparser.ConfigParser()
            config.read(ACTIVE_CONFIGURATION_FILE)
            self.functionalities = json.loads(config['DEFAULT']['FUNCTIONALITIES'])
            self.floors = json.loads(config['DEFAULT']['FUNCTIONALITIES'])
            self.capacity = int(config['DEFAULT']['CAPACITY'])
            
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
