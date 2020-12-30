import os
import json
from time import sleep
import random
import threading

from logic.elevator import Elevator
from properties.properties import PropertiesManager
from lora.lora import LoraEndpoint


def elevator_calls_worker(elevator):
    while True:
        sleep(1)
        elevator.check_calls()

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    #lora = LoraEndpoint()
    
    properties = PropertiesManager()
    elevator = Elevator(properties.elevator_code)

    threads = []
    if elevator.status:
        t = threading.Thread(target=elevator_calls_worker, args=(elevator,))
        threads.append(t)   
        t.start()

        while elevator.status:
            try:
                print("Waiting to receive a message...")
                """
                encoded_data = lora.read()
                print(f"Encoded data received: {encoded_data}")
                decoded_data = decode_data(encoded_data)
                print(f"Decoded data: {decoded_data}")
                
                """
                elevator.call(random.randint(0,len(elevator.floors) - 1))
            except:
                raise

            sleep(13)

def decode_data(data: bytes) -> str:
    return data.decode()

