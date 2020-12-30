import speech_recognition as sr
import pyttsx3
from .numparser import Text2Int

def init_speech():
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.9)
    r = sr.Recognizer()
    speech = sr.Microphone(device_index=0)

    with speech as source:
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_google(audio, language = 'es-ES')
        
        floor = Text2Int(recog)

        print("Yendo al piso " + str(floor))
        engine.say("Entendido. Te mando al piso " + str(floor))
        engine.runAndWait()

    except sr.UnknownValueError:
        engine.say("No he entendido. Por favor repite.")
        engine.runAndWait()

    except sr.RequestError as e:
        engine.say("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.runAndWait()