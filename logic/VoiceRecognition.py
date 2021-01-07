import speech_recognition as sr
from func.numparser import Text2Int
from logic.VoiceAssistant import VoiceAssistant
import asyncio

r = sr.Recognizer()
NUM_TRIES = 3
keyWord = 'piso'
"""
Quiero ir al piso 1
Me gustaría ir al piso 1
Llévame al piso 1
Piso 1
"""

async def wait_for_confirmation(reason):
    va = VoiceAssistant()
    va.add_to_pool(f'Esperando confirmación para {reason}')
    with sr.Microphone() as source:
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
        tosay = f"No he entendido por {NUM_TRIES} veces. Utilice los botones físicos"
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
    va = VoiceAssistant()
    with sr.Microphone() as source:
        tries_left = NUM_TRIES
        while tries_left > 0: 
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio, language="es-ES")
                print(text.lower())
                
                if keyWord.lower() in text.lower():
                    if _callback:
                        if await _callback(text):
                            break
                        else:
                            tries_left -= 1

            except Exception as e:
                print(e)
                tries_left -= 1

            va.add_to_pool(tries_advice(tries_left))

        #print("VOICE RECOGNITION STOPPED")
        return
    #print("VOICE RECOGNITION STOPPED")
