import json
import requests 
import configparser
from logic.Singleton import SingletonMeta
from func.servercommunication import get_from_backend, post_to_backend

config = configparser.RawConfigParser()

class PropertiesManager(metaclass=SingletonMeta):
    MAIN_CONFIGURATION_FILE = "properties/main.properties"
    ELEVATOR_CONFIGURATION_FILE = "properties/elevator.properties"

    #BACKEND PROPERTIES
    @property   
    def BACKEND_URL(self):
        config.read(self.MAIN_CONFIGURATION_FILE)
        return config.get('SERVER', 'SERVER_URL')
    
    #ELEVATOR PROPERTIES
    @property
    def ELEVATOR_CODE(self):
        config.read(self.MAIN_CONFIGURATION_FILE)
        return str(config.get('MAIN', 'CODE'))

    @property
    def REFRESH_TIME(self):
        config.read(self.MAIN_CONFIGURATION_FILE)
        return int(config.get('MAIN', 'REFRESH_TIME'))

    def get_elevator_configuration(self):
        config.read(self.ELEVATOR_CONFIGURATION_FILE)
        try:
            data = get_from_backend(self.BACKEND_URL + self.ELEVATOR_CODE)
            if data:
                config['DEFAULT']['FUNCTIONALITIES'] = json.dumps(data['activeFunctionalities'])
                config['DEFAULT']['FLOORS'] = json.dumps(data['activeFloors'])
                config['DEFAULT']['CAPACITY'] = str(data['capacity'])
                return self.write_config_file(self.ELEVATOR_CONFIGURATION_FILE, config)

        except Exception as e:
            print(f"PROPERT: Error while trying to get configuration from backend:" + str(e))
            return config
    
    #GENERIC
    def write_config_file(self, file, config):
        print(f"PROPERT: Writing file {file}")
        with open(file, 'w') as configfile:
            config.write(configfile)
        return config
    
    