import json
import requests 
import time
from func.Singleton import SingletonMeta
from func.threading import threaded, kill_thread

#Incidence event types
DISABLED_FLOOR = "disabledfloor"
CAPACITY_OVER = "capacityover"
EXCEPTION = "exception"

class ServerCommunication(metaclass=SingletonMeta):
    PROPERTIES = None
    main_thread = None
    pool = []
    active = True

    def __init__(self, properties):
        self.PROPERTIES = properties
        self.main_thread = self.thread_check_pool()
        print("BACKEND: Initialized")
    
    def set_active(self, active):
        self.active = active

    def add_to_pool(self, url, data):
        obj = {
            "url": url,
            "data": data
        }
        self.pool.append(obj)
    
    @property
    def status():
        if self.main_thread and self.main_thread.is_alive():
            return True
        return False

    @threaded
    def thread_check_pool(self):
        while True:
            time.sleep(10)
            if self.active:
                for dataToSend in self.pool:
                    try:
                        r = self.post_to_backend(dataToSend['url'], dataToSend['data'])
                        if r and r.status_code == 200:
                            print(f"BACKEND: Response for {dataToSend['url']}: {r.json()}")
                            self.pool.remove(dataToSend)
                    except Exception as e:
                        print(str(e))
                else:
                    #TODO Guardar datos en logs
                    pass

    def post_to_backend(self, path, data):
        print(f"BACKEND: Posting {data} to backend")
        try:
            url = str(path)
            r = requests.post(url, json=data)
            return r
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
    def send_call_data(self, inFloor, delayedTime=None):
        url =  self.PROPERTIES.POST_CALL_URL
        data = {
            "elevator": self.PROPERTIES.ELEVATOR_ID,
            "floor": int(inFloor)
        }
        if delayedTime:
            data["delayedTime"] = delayedTime
        self.add_to_pool(url, data)

    def send_ride_data(self, fromFloor, toFloor, time, numPassengers):
        url =  self.PROPERTIES.POST_RIDE_URL
        data = {
            "elevator":  self.PROPERTIES.ELEVATOR_ID,
            "from": int(fromFloor),
            "to": int(toFloor),
            "time": int(time),
            "numPassengers": int(numPassengers)
        }
        self.add_to_pool(url, data)

    def send_incidence_data(self, reason, moredata=""):
        url =  self.PROPERTIES.POST_INCIDENCE_URL
        data = {
            "elevator":  self.PROPERTIES.ELEVATOR_ID,
            "reason": str(reason),
            "data": str(moredata)
        }
        self.add_to_pool(url, data)