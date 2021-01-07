import json
from typing import Dict

ELEVATOR_CALL = "elevatorcall"

def dump_data(data: Dict) -> str:
    return json.dumps(data)

def load_data(data: str) -> Dict:
    return json.loads(data)
    
def decode_data(data: bytes) -> str:
    return data.decode()
