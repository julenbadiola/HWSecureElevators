from lora.lora import LoraEndpoint
import os
import json

if __name__ == "__main__":
    print("==================== SERVER SECURE ELEVATORS ===================== \n")
    lora = LoraEndpoint()
    while True:
        try:
            print("Waiting to receive a message...")
            encoded_data = lora.read()
            print(f"Encoded data received: {encoded_data}")
            decoded_data = decode_data(encoded_data)
            print(f"Decoded data: {decoded_data}")
            time.sleep(10)
        except:
            pass

def decode_data(data: bytes) -> str:
    return data.decode()