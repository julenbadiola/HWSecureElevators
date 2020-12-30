import json
from time import sleep

from logic.Elevator import Elevator
from logic.VoiceAssistant import VoiceAssistant
from properties.properties import PropertiesManager
from lora.lora import LoraEndpoint

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    #Initializing
    #lora = LoraEndpoint()
    
    properties = PropertiesManager()
    elevator = Elevator(properties.elevator_code)
    voice = VoiceAssistant()
    sleep(2)
    elevator.call(0)

    if elevator.status:
        while elevator.status and voice.status:
            try:
                print("Waiting to receive a message...")
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

