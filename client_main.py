import os
import time
from lora.lora import LoraEndpoint
from func import protocol as prot

THIS_FLOOR = 1
lora_endpoint = LoraEndpoint()


def call_elevator(floor):
    data = {
        prot.ELEVATOR_CALL: 50,
    }
    encoded_data = prot.dump_data(data)
    lora_endpoint.write_string(encoded_data)


if __name__ == "__main__":
    print("Lora [OK]")

    while True:
        try:
            print('Llamas desde el piso:')
            x = input()
            call_elevator(int(x))
        except:
            raise

        time.sleep(3)
