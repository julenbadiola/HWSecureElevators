import json

from properties.properties import PropertiesManager
import time
import asyncio

from logic.Singleton import SingletonMeta
from logic.CapacityController import get_current_occupation
from logic.VoiceAssistant import VoiceAssistant
from logic.VoiceRecognition import wait_voice_input, check_floor_and_ride
from logic.threading import threaded, kill_thread
from func import protocol as prot
from func.servercommunication import ServerCommunication, DISABLED_FLOOR, CAPACITY_OVER

class Elevator(metaclass=SingletonMeta):
    #Static
    code = None
    id = None
    config = None
    functionalities = []
    floors = []
    capacity = None

    #Dynamic
    status = False
    doors_open = False
    where = 0

    #Functionality
    calls_pool = []
    arrived_pool = []
    
    calls_thread = None
    ride_thread = None
    voice_recog_thread = None
    physic_button_thread = None

    #INITIALIZATION
    def __init__(self, properties, lora):
        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        config = properties.get_elevator_configuration()
        try:
            self.id = json.loads(config['DEFAULT']['ID'])
            self.functionalities = json.loads(config['DEFAULT']['FUNCTIONALITIES'])
            self.floors = json.loads(config['DEFAULT']['FLOORS'])
            self.capacity = int(config['DEFAULT']['CAPACITY'])

            self.calls_thread = self.thread_check_calls()
            self.voice_assistant = VoiceAssistant(self)
            self.code = properties.ELEVATOR_CODE
            self.lora = lora
            print("ELEV: Initialized successfully")

        except Exception as e:
            print(f"ELEV: Could not set configuration. The configuration does not exist or is corrupt. {str(e)}")

    @property
    def overall_status(self):
        try:
            return self.calls_thread.is_alive() and self.voice_assistant.status
        except Exception:
            return False

    @property
    def riding(self):
        try:
            return self.ride_thread.is_alive()
        except Exception:
            return False

    @threaded
    def thread_check_calls(self):
        #Checks calls pool and sends to ride if the elevator is not riding already
        while True:
            time.sleep(1)
            if not self.riding and len(self.calls_pool) > 0:
                #print(f"ELEV: {self.calls_pool}.")
                toFloor = self.calls_pool[0]
                if toFloor is not None:
                    self.ride(False, toFloor)

    #BUSINESS LOGIC
    def call(self, where):
        if(self.valid_floor_selection(False, where)):
            print(f"ELEV: Elevator called in {where}")
            #self.voice_assistant.add_to_pool(f"Elevador llamado en el piso {where}")
            ServerCommunication().send_call_data(where)
            self.calls_pool.append(where)
        else:
            print(f"ELEV: Elevator called in inactive floor {where}")

    def kill_floor_input_threads(self):
        self.voice_recog_thread = kill_thread(self.voice_recog_thread)
        self.physic_button_thread = kill_thread(self.physic_button_thread)

    def wait_for_floor_input(self):
        #Matamos los hilos input si existen
        self.kill_floor_input_threads()
        #Activamos el reconocimiento por voz
        self.voice_recog_thread = self.thread_voice_recognition_floor_input()
        #Activamos los botones (emulados por teclado)
        self.physic_button_thread = self.thread_physic_button_floor_input()

    @threaded
    def thread_physic_button_floor_input(self):
        print('VAS AL PISO:')
        x = input()
        self.ride(True, floor)

    @threaded
    def thread_voice_recognition_floor_input(self):
        try:
            self.voice_assistant.add_to_pool('Pronuncie el piso al que desea ir o utilice los botones físicos.')
            time.sleep(2)
            asyncio.run(wait_voice_input(check_floor_and_ride))
        except expression as identifier:
            self.voice_assistant.add_to_pool('No se ha podido iniciar el reconocimiento de voz. Utilice los botones físicos.')
        
    def ride(self, destination, floor):
        self.kill_floor_input_threads()
        self.ride_thread = self.thread_ride(destination, floor)

    @threaded
    def thread_ride(self, destination, floorToGo):
        start = time.time()
        if (floorToGo == None):
            return
        
        occupation = get_current_occupation()
        if self.capacity < occupation:
            print(f"ELEV: The capacity is higher than maximum {self.capacity}.")
            ServerCommunication().send_incidence_data(self.where, CAPACITY_OVER, f"{occupation}/{self.capacity}")

        elif not self.valid_floor_selection(False, floorToGo):
            print(f"ELEV: The floor {floorToGo} is disabled.")
            ServerCommunication().send_incidence_data(self.where, DISABLED_FLOOR, None)

        elif(self.where == floorToGo):
            print(f"ELEV: Elevator already on floor {floorToGo}.")
        
        else:
            print(f"ELEV: Capacity and floor validations succeeded.")
            diff = abs(self.where - floorToGo)
            self.close_doors()
            self.voice_assistant.add_to_pool(f"Elevador going to {floorToGo}.")
            for i in range(0, diff):
                time.sleep(2)
                #self.voice_assistant.add_to_pool(f"Elevador yendo a {floorToGo}. Ahora en {i}")
                print(f"ELEV: Riding to {floorToGo}. Now in {i}")

            self.where = floorToGo
            self.open_doors()
            ServerCommunication().send_ride_data(self.where, floorToGo, time.time() - start, occupation)
            if not destination:
                self.wait_for_floor_input()
            
        print(f"ELEV: Ride to {floorToGo} finished.")
        try:
            self.add_pool_arrived_lora(floorToGo)
            self.calls_pool.remove(floorToGo)
        except Exception as e:
            #Si tira error es porque no es un call, el ride se ha activado desde el recog o los botones
            pass
    
    ## OTHERS
    def valid_floor_selection(self, voice, floor):
        if floor > len(self.floors) - 1:
            return False

        if self.floors[floor] == True:
            return True
        else:
            if voice:
                self.voice_assistant.add_to_pool(f"El piso {floor} está inhabilitado.")
            return False

    def add_to_voice_assistant(self, tosay):
        self.voice_assistant.add_to_pool(tosay)

    def open_doors(self):
        self.voice_assistant.add_to_pool("Abriendo cabina.")
        time.sleep(2)
        self.doors_open = True
    
    def close_doors(self):
        self.voice_assistant.add_to_pool("Cerrando cabina.")
        time.sleep(2)
        self.doors_open = False

    #LORA COMMUNICATION
    def add_pool_arrived_lora(self, floor):
        if floor not in self.arrived_pool:
            self.arrived_pool.append(floor)

    def send_arrived_lora(self):
        try:
            for floorArrived in self.arrived_pool:
                encoded_data = prot.dump_data({
                    prot.ELEVATOR_ARRIVE: floorArrived,
                })
                self.lora.write_string(encoded_data)
            self.arrived_pool.clear()
            return True
        except Exception as e:
            print(str(e))
            return False

    
        
        