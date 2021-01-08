import os
import time
import signal
from lora.lora import LoraEndpoint
from func import protocol as prot
from logic.threading import threaded

THIS_FLOOR = 1
lora_endpoint = LoraEndpoint()

def timeout_handler(signum, frame):
    raise Exception("timeout reached")

def call_elevator(floor):
    data = {
        prot.ELEVATOR_CALL: floor,
    }
    encoded_data = prot.dump_data(data)
    lora_endpoint.write_string(encoded_data)

    #Listen to cabin por 10 seconds, if the elevator has not arrived, stop listening
    #This is because cannot call the elevator while listen_to_cabin is running, since lora module is busy
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)
    try:
        listen_to_cabin()
    except Exception as e:
        print(f"listen_to_cabin {str(e)}")

def listen_to_cabin():
    #Listen to cabin ELEVATOR_ARRIVE events
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

if __name__ == "__main__":
    print("Lora [OK]")
    while True:
        try:
            #Emulador botón físico
            print(f'Llamas desde el {THIS_FLOOR}:')
            x = input()
            call_elevator(THIS_FLOOR)
        except Exception as e:
            print(f"EXCEPTION IN thread_main {str(e)}")

        time.sleep(3)
    
