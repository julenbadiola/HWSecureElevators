import os
import time
from lora.lora import LoraEndpoint
from func import protocol as prot

THIS_FLOOR = 1

def call_elevator():
    """
    #LEER DATOS DE LOS SENSORES

    #IF EL DE PROXIMIDAD:
    # data = {
    # prot.ELEVATOR_CALL: 50,
    # }
    # encoded_data = prot.dump_data(data)
    # lora_endpoint.write_string(encoded_data)
    
    """
if __name__ == "__main__":
    lora_endpoint = LoraEndpoint()
    print("Lora [OK]")
    
    while True:
        try:
            """
            #LEER DATOS DE LOS SENSORES

            #IF EL DE PROXIMIDAD:
            call_elevator()

            CALL
            """
            time.sleep(3)
        except:
            pass
