import json
from time import sleep

from logic.Elevator import Elevator
from properties.properties import PropertiesManager
from lora.lora import LoraEndpoint

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    #lora = LoraEndpoint()
    
    properties = PropertiesManager()
    elevator = Elevator(properties.elevator_code)    
    elevator.call(0)

    sleep(1)
    while elevator.overall_status:
        try:
            #print("Waiting to receive a message...")
            """
                encoded_data = lora.read()
                print(f"Encoded data received: {encoded_data}")
                decoded_data = decode_data(encoded_data)
                print(f"Decoded data: {decoded_data}")
            """
            if not elevator.riding:
                print('Llamas desde el piso:')
                x = input()
                elevator.call(int(x))
        except:
            raise

        sleep(3)

def decode_data(data: bytes) -> str:
    return data.decode()

