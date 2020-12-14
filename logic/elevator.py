import json
import requests 

GENERAL_URL = "http://127.0.0.1:5000/api/raspberry/"

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

    def __init__(self, code):
        self.code = code
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend
        self.get_from_backend()
        #Go to first floor
        self.call(0)
    
    @property
    def configuration_url(self):
        return GENERAL_URL + str(self.code)

    def get_from_backend(self):
        print(f"ELEV: Getting configuration from backend")
        r = requests.get(url = self.configuration_url) 
       
        try:
            data = r.json() 
            self.functionalities = data['activeFunctionalities']
            self.floors = data['activeFloors']
            self.capacity = data['capacity']
            self.status = True

        except Exception as e:
            self.exceptions.append(str(e))
            self.status = False
    
    #business logic
    def call(self, where):
        print(f"ELEV: Going to {where}")
        try:
            self.where = self.floors[where]
        
        except Exception as e:
            self.status = False
