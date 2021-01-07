import json
from time import sleep
from logic.threading import threaded

from properties.properties import PropertiesManager
from logic.Elevator import Elevator
from logic.CapacityController import initialize_capacity_controller

from lora.lora import LoraEndpoint
from func import protocol as prot

properties = PropertiesManager()
lora = LoraEndpoint()
elevator = Elevator(properties, lora)

@threaded
def thread_listen_to_floors(protocol):
    while elevator.overall_status:
        try:
            print("CABIN: Waiting to receive a message...")
            data = protocol.clean_data(lora.read())
            
            if protocol.ELEVATOR_CALL in data:
                print("Received elevator call")
                calledFloor = int(data[protocol.ELEVATOR_CALL])
                elevator.call(calledFloor)
        
        except Exception as e:
            print(f"EXCEPTION IN thread_listen_to_floors {str(e)}")

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    
    #Initializing
    elevator.call(0)
    thread_listen_to_floors(prot)
    initialize_capacity_controller()
    



