import json
import requests 

def post_to_backend(data):
    print(f"BACKEND: Posting {data} to backend")
    pass

def get_from_backend(path):
    url = str(path)
    r = requests.get(url = url) 
    try:
        data = r.json()
        print(f"BACKEND: Got data from {path}")
        return data
    
    except Exception as e:
        print(f"BACKEND: Error while getting data from {path} = " + str(e))
        return None
    