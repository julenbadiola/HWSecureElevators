import cv2
import imutils
import numpy as np
from logic.Singleton import SingletonMeta

width = 800
occupation = 0

def get_current_occupation():
    return occupation


def is_capacity_respected(maximumCapacity):
    if occupation <= maximumCapacity:
        return True
    return False


def initialize():
    #camera = cv2.VideoCapture("logic/CapacityTestVideos/test2.mp4")
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
            # break
            camera = cv2.VideoCapture("logic/CapacityTestVideos/test2.mp4")
            continue

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # loop over the contours

        people = 0
        for c in cnts:
            # print(c)
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 12000:
                continue

            people += 1

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        occupation = people
        cv2.putText(frame, "Occupation: {}".format(str(occupation)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Security Feed", frame)

    video.release()
    cv2.destroyAllWindows()
