import json
from time import sleep
from lora.lora import LoraEndpoint
from grove.gpio import GPIO

from properties.properties import PropertiesManager
from logic.Elevator import Elevator
from logic.CapacityController import initialize as initialize_capacity_controller
from func.threading import threaded
from func import protocol

properties = PropertiesManager()
lora = LoraEndpoint()
elevator = Elevator(properties, lora)

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

def exit():
    print("CLEANING GPIOs")
    GPIO.cleanup()
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    try:
        #Initializing
        elevator.call(0)
        thread_listen_to_floors()
        if elevator.capacity_control_active:
            print("FUNC: Capacity control functionality is active.")
            initialize_capacity_controller()
        else:
            print("FUNC: Capacity control functionality is INACTIVE.")

    except Exception as e:
        exit()
    except KeyboardInterrupt:
        exit()
