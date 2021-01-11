import speech_recognition as sr
import asyncio
import time

from func.numparser import Text2Int
from logic.VoiceAssistant import VoiceAssistant
from properties.properties import PropertiesManager as PM
from func.threading import threaded

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

def cleanTextForNumbers(text):
    res = []
    for s in text.split():
        r = Text2Int(s)
        if r is not None:
            #print(f'VOICEREC: Añadido {r}.')
            res.append(r)
    return res

async def check_floor_and_ride(elevator, text):
    print(f"Recognizing {text}")
    floors = cleanTextForNumbers(text)
    print(f"Floors {text}")
    if len(floors) > 1:
        #print(f'VOICEREC: {floors} detected in the speech.')
        floor = floors[0]
        
        print(f"Recognized {floor}")
        if elevator.valid_floor_selection(True, floor):
            """confirmation = await wait_for_confirmation(f"ir al piso {floor}")
            if confirmation:"""
            print(f"Valid {floor}")
            return floor
    return None

async def loop_voice_input(elevator):
    try:
        with sr.Microphone(device_index=2) as source:
            while True: 
                if elevator.waitingForInput:
                    try:
                        print("VOICEREC: recognizing...")
                        audio = r.listen(source)
                        text = r.recognize_google(audio, language="es-ES")
                        print(text.lower())
                        
                        if PM().SPEECH_KEYWORD.lower() in text.lower() or "pisos" in text.lower():
                            floor = await check_floor_and_ride(elevator, text)
                            if elevator.waitingForInput and floor != None:
                                elevator.ride(True, floor)

                    except Exception as e:
                        print("VOICEREC controlled exception: ", str(e))
                time.sleep(1)
            #print("VOICE RECOGNITION STOPPED")
        print("VOICEREC: Stopped")
    except Exception as e:
        print(f"VOICEREC: Exception {str(e)}")

@threaded
def VoiceRecognizer(elevator):
    print("VOICEREC: Initializing")
    fails = 0
    while fails < 3:
        asyncio.run(loop_voice_input(elevator))
        print("VOICEREC: Restarting after fail")
        fails += 1