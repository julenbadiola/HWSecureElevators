import json
import requests 
import configparser
from logic.singleton import SingletonMeta

class Properties(metaclass=SingletonMeta):
    constant_config = None
    STATIC_CONFIGURATION_FILE = "constant.properties"

    #INITIALIZATION
    def __init__(self):
        self.constant_config = configparser.RawConfigParser()
        self.constant_config.read(self.STATIC_CONFIGURATION_FILE)

    #PROPERTIES
    @property
    def elevator_code(self):
        return self.constant_config.get('ELEVATORSECTION', 'ELEVATOR.CODE')
    @property
    def active_conf_file(self):
        return self.constant_config.get('SETTINGS', 'ACTIVE_CONFIGURATION_FILE')
    @property
    def backend_url(self):
        return self.constant_config.get('SETTINGS', 'BACKEND_URL')

    #ELEVATOR CONFIGURATION STUFF
    @property
    def configuration_url(self):
        return self.backend_url + str(self.elevator_code)

    def get_elevator_configuration_from_backend(self):
        print(f"PROPERT: Getting configuration from backend")
        r = requests.get(url = self.configuration_url) 
        try:
            data = r.json()
            config = configparser.ConfigParser()
            config['DEFAULT']['FUNCTIONALITIES'] = json.dumps(data['activeFunctionalities'])
            config['DEFAULT']['FLOORS'] = json.dumps(data['activeFloors'])
            config['DEFAULT']['CAPACITY'] = str(data['capacity'])
            return self.write_config_file(self.active_conf_file, config)
        except Exception as e:
            raise e
            return None

    def get_elevator_configuration_from_file(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.active_conf_file)
            return config
        except Exception as e:
            raise e
            return None
    
    def write_config_file(self, file, config):
        with open(file, 'w') as configfile:
            config.write(configfile)
        return config
    
    