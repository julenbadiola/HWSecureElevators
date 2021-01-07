import os
import time
from lora.lora import LoraEndpoint
from func import protocol as prot
from logic.threading import threaded

THIS_FLOOR = 1
lora_endpoint = LoraEndpoint()

def call_elevator(floor):
    data = {
        prot.ELEVATOR_CALL: floor,
    }
    encoded_data = prot.dump_data(data)
    lora_endpoint.write_string(encoded_data)
    listen_to_cabin()

def listen_to_cabin():
    while True:
        try:
            print("FLOOR: Waiting to receive arrived message from elevator...")
            data = prot.clean_data(lora_endpoint.read())
                
            if prot.ELEVATOR_ARRIVE in data:
                arrived_to = int(data[prot.ELEVATOR_ARRIVE])
                print(f"Received elevator arrived {arrived_to}")
                break
            
        except Exception as e:
            print(f"EXCEPTION IN Listen_to_cabin {str(e)}")
    
@threaded
def thread_main():
    while True:
        try:
            print(f'Llamas desde el {THIS_FLOOR}:')
            x = input()
            call_elevator(THIS_FLOOR)
        except Exception as e:
            print(f"EXCEPTION IN thread_main {str(e)}")

        time.sleep(3)

if __name__ == "__main__":
    print("Lora [OK]")
    #thread_listen_to_cabin()
    thread_main()
    
