import json
import requests 
import configparser
from logic.singleton import SingletonMeta
from func.servercommunication import get_from_backend, post_to_backend

class PropertiesManager(metaclass=SingletonMeta):
    MAIN_CONFIGURATION_FILE = "main.properties"
    SERVER_CONFIGURATION_FILE = None
    HARDWARE_CONFIGURATION_FILE = None
    ELEVATOR_CONFIGURATION_FILE = None

    #INITIALIZATION
    def __init__(self):
        config = configparser.RawConfigParser()
        config.read("properties/"+self.MAIN_CONFIGURATION_FILE)
        
        path = str(config.get('SETTINGS', 'PROPERTIES_PATH'))
        self.SERVER_CONFIGURATION_FILE = str(path + config.get('SETTINGS', 'SERVER_CONFIGURATION_FILE'))
        self.HARDWARE_CONFIGURATION_FILE = str(path + config.get('SETTINGS', 'HARDWARE_CONFIGURATION_FILE'))
        self.ELEVATOR_CONFIGURATION_FILE = str(path + config.get('SETTINGS', 'ELEVATOR_CONFIGURATION_FILE'))
    
    #BACKEND PROPERTIES
    @property   
    def backend_url(self):
        config = configparser.RawConfigParser()
        config.read(self.SERVER_CONFIGURATION_FILE)
        return config.get('SERVER', 'SERVER_URL')
    
    #ELEVATOR PROPERTIES
    @property
    def elevator_code(self):
        config = configparser.RawConfigParser()
        config.read(self.HARDWARE_CONFIGURATION_FILE)
        return str(config.get('MAIN', 'CODE'))

    def get_elevator_configuration(self):
        print(f"PROPERT: Getting configuration from backend")
        try:
            data = get_from_backend(self.backend_url + self.elevator_code)
            config = configparser.RawConfigParser()
            config.read(self.ELEVATOR_CONFIGURATION_FILE)

            #comprobación de si existen los keys
            config['DEFAULT']['FUNCTIONALITIES'] = json.dumps(data['activeFunctionalities'])
            config['DEFAULT']['FLOORS'] = json.dumps(data['activeFloors'])
            config['DEFAULT']['CAPACITY'] = str(data['capacity'])
            return self.write_config_file(self.ELEVATOR_CONFIGURATION_FILE, config)
        
        except Exception as e:
            raise e
            return self.ELEVATOR_CONFIGURATION
    
    #GENERIC
    def write_config_file(self, file, config):
        print(f"PROPERT: Writing file {file}")
        with open(file, 'w') as configfile:
            config.write(configfile)
        return config
    
    