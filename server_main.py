from lora.lora import LoraEndpoint
from logic.elevator import Elevator
import os
import json
from time import sleep
import configparser
from properties import STATIC_CONFIGURATION_FILE

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #lora = LoraEndpoint()

    config = configparser.RawConfigParser()
    config.read(STATIC_CONFIGURATION_FILE)
    code = config.get('ElevatorSection', 'elevator.code')
    elevator = Elevator(code)

    while elevator.status:
        try:
            print("Waiting to receive a message...")
            """
            encoded_data = lora.read()
            print(f"Encoded data received: {encoded_data}")
            decoded_data = decode_data(encoded_data)
            print(f"Decoded data: {decoded_data}")
            
            """
            
        except:
            pass

        sleep(10)

def decode_data(data: bytes) -> str:
    return data.decode()