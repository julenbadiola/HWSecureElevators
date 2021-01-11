import json
from time import sleep
from lora.lora import LoraEndpoint

from properties.properties import PropertiesManager
from logic.Elevator import Elevator
from logic.CapacityController import initialize as initialize_capacity_controller
from func.threading import threaded
from func import protocol
from func.sensors import GroveButton

properties = PropertiesManager()
lora = LoraEndpoint()
buttonsEmulator = GroveButton(properties.BUTTON_PIN)
elevator = Elevator(properties, lora, buttonsEmulator)

@threaded
def thread_listen_to_floors():
    while elevator.overall_status:
        try:
            print("MAIN: Waiting to receive a LORA message...")
            data = protocol.clean_data(lora.read())
            
            if protocol.ELEVATOR_CALL in data:
                print("Received elevator call")
                calledFloor = int(data[protocol.ELEVATOR_CALL])
                elevator.call(calledFloor)
            elevator.send_arrived_lora()
        
        except Exception as e:
            pass

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    
    #Initializing
    elevator.call(0)
    thread_listen_to_floors()
    if elevator.capacity_control_active:
        print("FUNC: Capacity control functionality is active.")
        initialize_capacity_controller()
    else:
        print("FUNC: Capacity control functionality is INACTIVE.")



