import json
import requests 

def post_to_backend(data):
    print(f"BACKEND: Posting {data} to backend")
    pass

def get_from_backend(path):
    print(f"BACKEND: Getting {path} from backend")

    url = str(path)
    r = requests.get(url = url) 
    try:
        data = r.json()
        return data
    
    except Exception as e:
        raise e
    return None
    