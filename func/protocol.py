import json
from typing import Dict

ELEVATOR_CALL = "elevatorcall"
ELEVATOR_RIDE = "elevatorride"
ELEVATOR_INCIDENCE = "elevatorincidence"
ELEVATOR_ARRIVE = "elevatorarrived"

def dump_data(data: Dict) -> str:
    return json.dumps(data)

def decode_data(data: bytes) -> str:
    return data.decode()

def load_data(data: str) -> Dict:
    return json.loads(data)
    
def clean_data(lora_data: bytes) -> Dict:
    decoded_data = decode_data(lora_data)
    return load_data(decoded_data)