import speech_recognition as sr
import asyncio

from func.numparser import Text2Int
from logic.VoiceAssistant import VoiceAssistant
from properties.properties import PropertiesManager as PM

r = sr.Recognizer()

async def wait_for_confirmation(reason):
    va = VoiceAssistant()
    va.add_to_pool(f'Esperando confirmación para {reason}')
    with sr.Microphone(device_index=2) as source:
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="es-ES")
                #print(text.lower())
                
                if "si" in text.lower():
                    return True

            except Exception as e:
                return False

def tries_advice(tries_left):
    tosay = "Vuelva a pronunciarlo. "
    if tries_left > 1:
        tosay += f"Quedan {tries_left} intentos"
    elif tries_left == 1:
        tosay += f"Queda un intento"
    else:
        tosay = f"No he entendido por {PM().NUMBER_OF_TRIES_SPEECH} veces. Utilice los botones físicos"
    return tosay

def cleanTextForNumbers(text):
    res = []
    for s in text.split():
        r = Text2Int(s)
        if r is not None:
            #print(f'VOICEREC: Añadido {r}.')
            res.append(r)
    return res

async def check_floor_and_ride(text):
    print(f"Recognizing {text}")
    elevator = VoiceAssistant().elevator
    floors = cleanTextForNumbers(text)
    if len(floors) == 1:
        #print(f'VOICEREC: {floors} detected in the speech.')
        floor = floors[0]
        
        if elevator.valid_floor_selection(True, floor):
            """confirmation = await wait_for_confirmation(f"ir al piso {floor}")
            if confirmation:
                elevator.ride(True, floor)
                return True"""
            elevator.ride(True, floor)
            return True
    return False

async def wait_voice_input(_callback = None):
    try:
        with sr.Microphone(device_index=2) as source:
            while True: 
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio, language="es-ES")
                    print(text.lower())
                    
                    if PM().SPEECH_KEYWORD.lower() in text.lower():
                        if _callback:
                            if await _callback(text):
                                break

                except Exception as e:
                    print(e)

            #print("VOICE RECOGNITION STOPPED")
            return
        print("VOICEREC: Stopped")
    except Exception:
        raise Exception("VOICEREC: Could not initialize")
    
