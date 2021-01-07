import json
from time import sleep
from logic.threading import threaded

from properties.properties import PropertiesManager
from logic.Elevator import Elevator
from logic.CapacityController import CapacityController

from lora.lora import LoraEndpoint
from func import protocol as prot

properties = PropertiesManager()
elevator = Elevator(properties.elevator_code)
lora = LoraEndpoint()

"""
@threaded
def thread_initialization():
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
"""

@threaded
def thread_checkLoraMessages():
    while elevator.overall_status:
        try:
            print("Waiting to receive a message...")
            encoded_data = lora.read()
            print(f"Encoded data received: {encoded_data}")
            decoded_data = decode_data(encoded_data)
            print(f"Decoded data: {decoded_data}")
            
            if prot.ELEVATOR_CALL in decoded_data:
                print("Received elevator call")
                elevator.call(decoded_data[prot.ELEVATOR_CALL])
        except:
            raise

        sleep(3)

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    
    elevator.call(0)
    thread_checkLoraMessages()
    CapacityController()
    

def decode_data(data: bytes) -> str:
    return data.decode()

