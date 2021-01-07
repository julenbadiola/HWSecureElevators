import cv2
import imutils
import numpy as np
import argparse
from logic.Singleton import SingletonMeta

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
occupation = 0

def get_current_occupation():
    return occupation

def is_capacity_respected(maximumCapacity):
    if occupation <= maximumCapacity:
        return True
    return False

class CapacityController(metaclass=SingletonMeta):
    def __init__(self):
        self.detectByCamera()
        #self.detectByVideo()

    def detect(self, frame):
        bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
        
        person = 1
        for x,y,w,h in bounding_box_cordinates:
            #v2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            #cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            person += 1
        
        occupation = person - 1
        #print("occupation", self.occupation)

        #Salida por pantalla
        #cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
        #cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
        #cv2.imshow('output', frame)

        return frame

    def detectByCamera(self):        
        print('CAPAC: Initializing capacity controller.')
        camera = cv2.VideoCapture(0)

        firstFrame = None

        # loop over the frames of the video
        while True:
            # grab the current frame and initialize the occupied/unoccupied
            # text
            (grabbed, frame) = camera.read()
            
            text = "Unoccupied"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if not grabbed:
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=800)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue
            
            frame = self.detect(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

    def detectByVideo(self):
        video = cv2.VideoCapture("logic/Capacity/test2.mp4")
        check, frame = video.read()
        if check == False:
            print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
            return

        print('Detecting people...')
        while video.isOpened():
            #check is True if reading was successful 
            check, frame =  video.read()

            if check:
                frame = imutils.resize(frame , width=min(800,frame.shape[1]))
                frame = self.detect(frame)
                
                key = cv2.waitKey(1)
                if key== ord('q'):
                    break
            else:
                break
        video.release()
        cv2.destroyAllWindows()
    