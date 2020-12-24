from lora.lora import LoraEndpoint
from logic.elevator import Elevator
from func.properties import Properties
import os
import json
from time import sleep
import random

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #lora = LoraEndpoint()
    properties = Properties()
    elevator = Elevator(properties.elevator_code)

    while elevator.status:
        try:
            print("Waiting to receive a message...")
            """
            encoded_data = lora.read()
            print(f"Encoded data received: {encoded_data}")
            decoded_data = decode_data(encoded_data)
            print(f"Decoded data: {decoded_data}")
            
            """
            print(elevator.floors)
            elevator.call(random.randint(0,len(elevator.floors)))
            elevator.ride()
        except:
            pass

        sleep(3)

def decode_data(data: bytes) -> str:
    return data.decode()