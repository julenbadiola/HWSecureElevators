import speech_recognition as sr
from func.numparser import Text2Int
from logic.VoiceAssistant import VoiceAssistant
import asyncio

r = sr.Recognizer()
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

def cleanText(text):
    res = []
    for s in text.split():
        r = Text2Int(s)
        if r is not None:
            #print(f'VOICEREC: Añadido {r}.')
            res.append(r)
    return res


async def wait_voice_input(elevator):
    done = False
    with sr.Microphone() as source:
        elevator.add_to_voice_assistant('Pronuncie el piso al que desea ir.')
        while not done: 
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="es-ES")
                #print(text.lower())
                
                if keyWord.lower() in text.lower():
                    try:
                        floors = cleanText(text)
                        if len(floors) == 1:
                            #print(f'VOICEREC: {floors} detected in the speech.')
                            floor = floors[0]
                            if elevator.valid_floor_selection(floor):
                                confirmation = await wait_for_confirmation(f"ir al piso {floor}")
                                if confirmation:
                                    elevator.ride(floor)
                                    done = True
                                
                    except Exception as e:
                        print(e)

            except Exception as e:
                elevator.add_to_voice_assistant('No he entendido. Vuelva a pronunciarlo.')
        