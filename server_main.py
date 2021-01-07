import json
from time import sleep

from logic.Elevator import Elevator
from properties.properties import PropertiesManager
from lora.lora import LoraEndpoint

from logic.Capacity.CapacityController import initialize as InitCapacityController
from logic.threading import threaded
"""
self.
self.capacity_controller.detect()
"""

properties = PropertiesManager()
elevator = Elevator(properties.elevator_code)
#lora = LoraEndpoint()

@threaded
def initialization():
    elevator.call(0)
    while elevator.overall_status:
        try:
            if not elevator.riding:
                print('Llamas desde el piso:')
                x = input()
                if not elevator.riding:
                    elevator.call(int(x))
        except:
            raise

        sleep(3)

@threaded
def checkLoraMessages():
    while elevator.overall_status:
        try:
            #print("Waiting to receive a message...")
            """
                encoded_data = lora.read()
                print(f"Encoded data received: {encoded_data}")
                decoded_data = decode_data(encoded_data)
                print(f"Decoded data: {decoded_data}")
            """
                
        except:
            raise

        sleep(3)

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    
    initialization()
    InitCapacityController()
    

def decode_data(data: bytes) -> str:
    return data.decode()

