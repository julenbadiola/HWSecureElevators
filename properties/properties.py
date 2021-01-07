import json
import requests 
import configparser
from logic.Singleton import SingletonMeta
from func.servercommunication import get_from_backend, post_to_backend
import functools

class PropertiesManager(metaclass=SingletonMeta):
    MAIN_CONFIGURATION_FILE = "properties/main.properties"
    ELEVATOR_CONFIGURATION_FILE = "properties/elevator.properties"

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(self.MAIN_CONFIGURATION_FILE)
        self.elevatorConfig = configparser.RawConfigParser()

    #SERVER PROPERTIES
    @functools.cached_property
    def BACKEND_URL(self):
        return str(self.config.get('SERVER', 'SERVER_URL'))
    
    #SPEECH PROPERTIES
    @functools.cached_property
    def NUMBER_OF_TRIES_SPEECH(self):
        return int(self.config.get('SPEECH', 'NUMBER_OF_TRIES'))
    
    @functools.cached_property
    def SPEECH_KEYWORD(self):
        return str(self.config.get('SPEECH', 'KEYWORD'))
    
    @functools.cached_property
    def SPEECH_LANGUAGE(self):
        return int(self.config.get('SPEECH', 'LANGUAGE'))
    
    @functools.cached_property
    def MIC_INDEX(self):
        return int(self.config.get('SPEECH', 'MIC_INDEX'))
    
    #ELEVATOR PROPERTIES
    @functools.cached_property
    def ELEVATOR_CODE(self):
        return str(self.config.get('MAIN', 'CODE'))

    @functools.cached_property
    def REFRESH_TIME(self):
        return int(self.config.get('MAIN', 'REFRESH_TIME'))

    #ELEVATOR SPECIFIC CONFIG (elevator.properties)
    def get_elevator_configuration(self):
        self.elevatorConfig.read(self.ELEVATOR_CONFIGURATION_FILE)
        try:
            data = get_from_backend(self.BACKEND_URL + self.ELEVATOR_CODE)
            if data:
                self.elevatorConfig['DEFAULT']['FUNCTIONALITIES'] = json.dumps(data['activeFunctionalities'])
                self.elevatorConfig['DEFAULT']['FLOORS'] = json.dumps(data['activeFloors'])
                self.elevatorConfig['DEFAULT']['CAPACITY'] = str(data['capacity'])
                return self.write_config_file(self.ELEVATOR_CONFIGURATION_FILE, self.elevatorConfig)

        except Exception as e:
            print(f"PROPERT: Error while trying to get configuration from backend:" + str(e))
            return self.elevatorConfig
    
    #GENERIC
    def write_config_file(self, file, config):
        print(f"PROPERT: Writing into file {file}")
        with open(file, 'w') as configfile:
            config.write(configfile)
        return config
    
    