import os
import time
import signal
from lora.lora import LoraEndpoint
from func import protocol as prot
from func.threading import threaded
from func.sensors import LED, GroveUltrasonicRanger, Button
from properties.properties import PropertiesManager

properties = PropertiesManager()
lora_endpoint = LoraEndpoint()
#SENSORS
led = LED(properties.LED_PIN)
but = Button(properties.BUTTON_PIN)
prox = GroveUltrasonicRanger(properties.PROXIMITY_PIN)

def timeout_handler(signum, frame):
    raise Exception("timeout reached")

def call_elevator(t=None):
    data = {
        prot.ELEVATOR_CALL: properties.THIS_FLOOR,
    }
    encoded_data = prot.dump_data(data)
    lora_endpoint.write_string(encoded_data)
    # Enceder led parpadeante que significa que he llamado al ascensor
    led.blink()

    # Listen to cabin for 40 seconds, if the elevator has not arrived, stop listening
    # This is because cannot call the elevator while listen_to_cabin is running, since lora module is busy
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(40)
    try:
        listen_to_cabin()

    except Exception as e:
        print(f"listen_to_cabin {str(e)}")


def listen_to_cabin():
    # Listen to cabin ELEVATOR_ARRIVE events
    start = time.time()
    while True:
        try:
            print("FLOOR: Waiting to receive arrived message from elevator...")
            data = prot.clean_data(lora_endpoint.read())

            if prot.ELEVATOR_ARRIVE in data:
                arrived_to = int(data[prot.ELEVATOR_ARRIVE])
                print(
                    f"Received elevator arrived to {arrived_to}. This floor {arrived_to == properties.THIS_FLOOR}")

                if arrived_to == properties.THIS_FLOOR:
                    led.stop_blink()
                    break

        except Exception as e:
            print(f"EXCEPTION IN Listen_to_cabin {str(e)}")

if __name__ == "__main__":
    print("Lora [OK]")
    try:
        while True:
            try:
                # Emulador botón físico
                # TODO: if sensor proximidad detecta algo o el boton es presionado => call_elevator
                dist = prox.get_distance()
                print(f"DISTANCE: {dist}")
                if but.pressed or dist < 2:
                    call_elevator()

            except Exception as e:
                print(f"EXCEPTION IN thread_main {str(e)}")

            time.sleep(1)

    except Exception as e:
        print("CLEANING GPIOs")
        GPIO.cleanup()
