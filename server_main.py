import json
from time import sleep
from logic.threading import threaded

from properties.properties import PropertiesManager
from logic.Elevator import Elevator
from logic.CapacityController import CapacityController

from lora.lora import LoraEndpoint
from func import protocol as prot

properties = PropertiesManager()
elevator = Elevator(properties.ELEVATOR_CODE)
lora_sender = LoraEndpoint()
lora_listener = LoraEndpoint()

def ride_elevator(floor):
    data = {
        prot.ELEVATOR_RIDE: floor,
    }
    encoded_data = prot.dump_data(data)
    lora_sender.write_string(encoded_data)

@threaded
def thread_listen_to_floors():
    while elevator.overall_status:
        try:
            print("CABIN: Waiting to receive a message...")
            data = prot.clean_data(lora_listener.read())
            
            if prot.ELEVATOR_CALL in data:
                print("Received elevator call")
                calledFloor = int(data[prot.ELEVATOR_CALL])
                elevator.call(calledFloor)
            ride_elevator(2)
        
        except Exception as e:
            print(f"EXCEPTION IN thread_listen_to_floors {str(e)}")

        sleep(properties.REFRESH_TIME)

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    
    elevator.call(0)
    thread_listen_to_floors()
    CapacityController()
    



