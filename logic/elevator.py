import json

from properties.properties import PropertiesManager
from time import sleep
import asyncio

from logic.Singleton import SingletonMeta
from logic.CapacityController import get_current_occupation, is_capacity_respected
from logic.VoiceAssistant import VoiceAssistant
from logic.VoiceRecognition import wait_voice_input, check_floor_and_ride
from logic.threading import threaded
from func import protocol as prot

class Elevator(metaclass=SingletonMeta):
    #Static
    code = None
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
    
    main_thread = None
    calls_thread = None
    ride_thread = None
    voice_recog_thread = None

    #INITIALIZATION
    def __init__(self, properties, lora):
        self.voice_assistant = VoiceAssistant(self)
        self.code = properties.ELEVATOR_CODE
        self.lora = lora

        print(f"ELEV: Initializing elevator {self.code}")
        #Get configuration from backend or file
        if self.activate():
            self.status = True
            print("ELEV: Status = successful.")
        else:
            self.status = False
            print("ELEV: Status = error.")   
        
        self.main_thread = self.check_threads()
        self.calls_thread = self.thread_check_calls()
    
    def activate(self):
        config = PropertiesManager().get_elevator_configuration()
        try:
            self.functionalities = json.loads(config['DEFAULT']['FUNCTIONALITIES'])
            self.floors = json.loads(config['DEFAULT']['FLOORS'])
            self.capacity = int(config['DEFAULT']['CAPACITY'])
            return True
        except Exception as e:
            print("ELEV: Could not set configuration. The configuration does not exist or is corrupt.")
            return False 

    @property
    def overall_status(self):
        return self.status and self.voice_assistant.status and self.main_thread.is_alive()

    @property
    def riding(self):
        return not self.ride_thread == None
    
    def clean_thread(self, t):
        if t != None and not t.is_alive():
            return None
        else:
            return t

    @threaded
    def check_threads(self):
        while True:
            sleep(1)
            #print(self.ride_thread, self.riding)
            #print(self.calls_thread, self.calls_pool)
            self.ride_thread = self.clean_thread(self.ride_thread)

    @threaded
    def thread_check_calls(self):
        while True:
            sleep(1)
            if not self.riding and len(self.calls_pool) > 0:
                #print(f"ELEV: {self.calls_pool}.")
                toFloor = self.calls_pool[0]
                if toFloor is not None:
                    self.ride(False, toFloor)
            """else:
                print(f"ELEV: There are not rides.")"""

    #BUSINESS LOGIC
    def call(self, where):
        if(self.valid_floor_selection(False, where)):
            print(f"ELEV: Elevator called in {where}")
            #self.voice_assistant.add_to_pool(f"Elevador llamado en el piso {where}")
            try:
                self.calls_pool.append(where)
            except Exception as e:
                self.status = False
        else:
            print(f"ELEV: Elevator called in inactive floor {where}")

    def kill_thread(self, thread):
        if thread:
            thread.kill()
            thread.join() 
        return None

    def onclick_physic_button(self, floor):
        self.voice_recog_thread = self.kill_thread(self.voice_recog_thread)
        self.ride(True, floor)

    def ask_for_floor_input(self):
        #Activamos el reconocimiento por voz
        self.kill_thread(self.voice_recog_thread)
        self.voice_recog_thread = self.thread_ask_for_floor_input()

        #Activamos el onclick
        print('VAS AL PISO:')
        x = input()
        self.onclick_physic_button(int(x))

    @threaded
    def thread_ask_for_floor_input(self):
        self.voice_assistant.add_to_pool('Pronuncie el piso al que desea ir o utilize los botones físicos.')
        asyncio.run(wait_voice_input(check_floor_and_ride))

    def ride(self, destination, floor):
        self.ride_thread = self.thread_ride(destination, floor)

    def add_pool_arrived_lora(self, floor):
        if floor not in self.arrived_pool:
            self.arrived_pool.append(floor)

    def send_arrived_lora(self, floor):
        try:
            for floorArrived in self.arrived_pool:
                encoded_data = prot.dump_data({
                    prot.ELEVATOR_ARRIVED: floor,
                })
                self.lora.write_string(encoded_data)
            return True
        except Exception as e:
            print())
            return False

    @threaded
    def thread_ride(self, destination, floorToGo):
        if (floorToGo == None):
            return
        
        if not is_capacity_respected(self.capacity):
            print(f"ELEV: The capacity is superior to maximum {self.capacity}.")

        elif not self.valid_floor_selection(False, floorToGo):
            print(f"ELEV: The floor {floorToGo} is disabled.")

        elif(self.where == floorToGo):
            print(f"ELEV: Elevator already on floor {floorToGo}.")
        
        else:
            print(f"ELEV: Capacity and floor validations succeeded.")
            diff = abs(self.where - floorToGo)
            self.close_doors()
            self.voice_assistant.add_to_pool(f"Elevador yendo a {floorToGo}.")
            for i in range(0, diff):
                sleep(2)
                #self.voice_assistant.add_to_pool(f"Elevador yendo a {floorToGo}. Ahora en {i}")
                print(f"ELEV: Riding to {floorToGo}. Now in {i}")

            self.where = floorToGo
            self.open_doors()
            
            if not destination:
                self.ask_for_floor_input()
            
        
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
        sleep(2)
        self.doors_open = True
    
    def close_doors(self):
        self.voice_assistant.add_to_pool("Cerrando cabina.")
        sleep(2)
        self.doors_open = False

    
        
        