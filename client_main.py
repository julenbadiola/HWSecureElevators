import os
import time
from ebikes.lora import lora

if __name__ == "__main__":
    lora_endpoint = lora.LoraEndpoint()
    print("Lora [OK]")
    
    while True:
        try:
            print("Getting data from sensors...")
            humidity, temperature = weather_sensor.value
            print(f"Humidty: {humidity}")
            print(f"Temperature: {temperature}")
            gas = sensors.calculate_gas_ratio(gas_sensor.value)
            print(f"Gas: {gas}")
            loudness = loudness_sensor.value
            print(f"Loudness: {loudness}")

            latitude, longitude = gps_sensor.value
            print(f"GPS: {(latitude, longitude)}")
            print("All data got from sensors [OK]")
            sensor_data = {
                prot.HUMIDITY_FIELD: humidity,
                prot.TEMPERATURE_FIELD: temperature,
                prot.GAS_FIELD: gas,
                prot.LOUDNESS_FIELD: loudness,
                prot.LATITUDE_FIELD: latitude,
                prot.LONGITUDE_FIELD: longitude
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
