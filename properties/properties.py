import json
import requests 
import configparser
from func.Singleton import SingletonMeta
from logic.ServerCommunication import ServerCommunication
from cached_property import cached_property

class PropertiesManager(metaclass=SingletonMeta):
    MAIN_CONFIGURATION_FILE = "properties/main.properties"
    ELEVATOR_CONFIGURATION_FILE = "properties/elevator.properties"
    SERVER_COMMUNICATION = None

    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(self.MAIN_CONFIGURATION_FILE)
        self.elevatorConfig = configparser.RawConfigParser()
        self.SERVER_COMMUNICATION = ServerCommunication(self)

    #CLIENT PROPERTIES
    @cached_property
    def THIS_FLOOR(self):
        return str(self.config.get('CLIENT', 'THIS_FLOOR'))

    @cached_property
    def LED_PIN(self):
        return int(self.config.get('CLIENT', 'LED_PIN'))

    @cached_property
    def PROXIMITY_PIN(self):
        return int(self.config.get('CLIENT', 'PROXIMITY_PIN'))
    
    @cached_property
    def BUTTON_PIN(self):
        return int(self.config.get('CLIENT', 'PROXIMITY_PIN'))

    #SERVER PROPERTIES
    @cached_property
    def BACKEND_URL(self):
        return str(self.config.get('SERVER', 'SERVER_URL'))
    
    @cached_property
    def POST_CALL_URL(self):
        return self.BACKEND_URL + str(self.config.get('SERVER', 'CALL_PATH'))
    
    @cached_property
    def POST_RIDE_URL(self):
        return self.BACKEND_URL + str(self.config.get('SERVER', 'RIDE_PATH'))
    
    @cached_property
    def POST_INCIDENCE_URL(self):
        return self.BACKEND_URL + str(self.config.get('SERVER', 'INCIDENCE_PATH'))

    #SPEECH PROPERTIES
    @cached_property
    def NUMBER_OF_TRIES_SPEECH(self):
        return int(self.config.get('SPEECH', 'NUMBER_OF_TRIES'))
    
    @cached_property
    def SPEECH_KEYWORD(self):
        return str(self.config.get('SPEECH', 'KEYWORD'))
    
    @cached_property
    def SPEECH_LANGUAGE(self):
        return int(self.config.get('SPEECH', 'LANGUAGE'))
    
    @cached_property
    def MIC_INDEX(self):
        return int(self.config.get('SPEECH', 'MIC_INDEX'))
    
    #ELEVATOR PROPERTIES
    @cached_property
    def ELEVATOR_CODE(self):
        return str(self.config.get('MAIN', 'CODE'))

    @cached_property
    def REFRESH_TIME(self):
        return int(self.config.get('MAIN', 'REFRESH_TIME'))

    #ELEVATOR SPECIFIC CONFIG (elevator.properties)
    @cached_property
    def ELEVATOR_ID(self):
        return str(self.elevatorConfig.get('DEFAULT', 'ID')).replace('"', '')

    def get_elevator_configuration(self):
        self.elevatorConfig.read(self.ELEVATOR_CONFIGURATION_FILE)
        try:
            data = self.SERVER_COMMUNICATION.get_from_backend(self.BACKEND_URL + self.ELEVATOR_CODE)
            if data:
                self.elevatorConfig['DEFAULT']['ID'] = json.dumps(data['_id'])
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
    
    