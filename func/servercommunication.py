import json
import requests 

#Incidence event types
DISABLED_FLOOR = "disabledfloor"
CAPACITY_OVER = "capacityover"

class ServerCommunication(metaclass=SingletonMeta):
    PROPERTIES = None

    def __init__(self, properties):
        self.PROPERTIES = properties

    def post_to_backend(self, path, json):
        url = str(path)
        print(f"BACKEND: Posting {json} to backend")
        r = requests.post(url, json={path})
        try:
            response = r.json()
            print(response)
            return True
        except Exception as e:
            print(f"BACKEND: Error while posting data to {path} = " + str(e))
            return None

    def get_from_backend(self, path):
        url = str(path)
        r = requests.get(url = url) 
        try:
            response = r.json()
            print(f"BACKEND: Got data from {path}")
            return response
        
        except Exception as e:
            print(f"BACKEND: Error while getting data from {path} = " + str(e))
            return None

    #Specific
    def send_call_data(self, inFloor):
        url =  self.PROPERTIES.POST_CALL_URL
        json = {
            "elevator":  self.PROPERTIES.ELEVATOR_ID,
            "floor": int(inFloor)
        }
        self.post_to_backend(url, json)

    def send_ride_data(self, fromFloor, toFloor, time, numPassengers):
        url =  self.PROPERTIES.POST_RIDE_URL
        json = {
            "elevator":  self.PROPERTIES.ELEVATOR_ID,
            "from": int(fromFloor),
            "toFloor": int(toFloor),
            "time": int(time),
            "numPassengers": int(numPassengers)
        }
        self.post_to_backend(url, json)

    def send_incidence_data(self, where, reason, data):
        url =  self.PROPERTIES.POST_INCIDENCE_URL
        json = {
            "elevator":  self.PROPERTIES.ELEVATOR_ID,
            "where": int(where),
            "reason": str(reason),
            "numPassengers": int(numPassengers)
        }
        if data:
            json["data"] = str(data),
        
        self.post_to_backend(url, json)