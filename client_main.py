import os
import time
from lora.lora import LoraEndpoint
from func import protocol as prot

SAMPLING_FREQUENCY = 3

if __name__ == "__main__":
    lora_endpoint = LoraEndpoint()
    print("Lora [OK]")
    
    while True:
        try:
            print("Getting data from sensors...")
            sensor_data = {
                prot.TEMPERATURE_FIELD: 50,
            }

            encoded_data = prot.dump_sensor_data(sensor_data)
            print(f"JSON data encoded: {encoded_data}")
            
            print(f"Sending data to Lora Endpoint...")
            lora_endpoint.write_string(encoded_data)
            print(f"Data sent [OK]")

            print(f"Sleeping {SAMPLING_FREQUENCY} seconds...")
            time.sleep(SAMPLING_FREQUENCY)
        except:
            pass
