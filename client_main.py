import os
import time
from lora.lora import LoraEndpoint
from func import protocol as prot
from logic.threading import threaded

THIS_FLOOR = 1
lora_sender = LoraEndpoint()
lora_listener = LoraEndpoint()

def call_elevator(floor):
    data = {
        prot.ELEVATOR_CALL: floor,
    }
    encoded_data = prot.dump_data(data)
    lora_sender.write_string(encoded_data)

@threaded
def thread_listen_to_cabin():
    while True:
        try:
            print("FLOOR: Waiting to receive a message...")
            data = prot.clean_data(lora_listener.read())
            
            if prot.ELEVATOR_RIDE in data:
                riding_to = int(data[prot.ELEVATOR_RIDE])
                print(f"Received elevator ride {riding_to}")
        
        except Exception as e:
            print(f"EXCEPTION IN Listen_to_cabin {str(e)}")

        sleep(1)

@threaded
def thread_main():
    while True:
        try:
            print('Llamas desde el piso:')
            x = input()
            call_elevator(int(x))
        except:
            print(f"EXCEPTION IN thread_main {str(e)}")

        time.sleep(3)

if __name__ == "__main__":
    print("Lora [OK]")
    thread_listen_to_cabin()
    thread_main()
    
