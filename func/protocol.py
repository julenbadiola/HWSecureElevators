import json
from typing import Dict

TEMPERATURE_FIELD = "temperature"


def dump_sensor_data(sensor_data: Dict) -> str:
    return json.dumps(sensor_data)


def load_data_sensor(data: bytes) -> str:
    return data.decode()
