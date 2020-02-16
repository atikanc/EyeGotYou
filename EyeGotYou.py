import cv2 as cv
import sys
import datetime as dt
from time import sleep
import os
from pynput.keyboard import Key, Controller

faceCas = cv.CascadeClassifier("haarcascades/haarcascade_eye.xml")
cam = cv.VideoCapture(0)
last_detection = dt.datetime.now()
threshold = dt.timedelta(seconds=10)
recent_lock = bool(0)
keyboard = Controller()

while (True):
    sleep(0.2)
    if not cam.isOpened():
        print("Could not open Camera")
        break

    ret, frame = cam.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = faceCas.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        last_detection = dt.datetime.now()
        if recent_lock:
            print("[", dt.datetime.now(), "] =>", "Eyes Detected Again")
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            print("[ Accessibility ] => Media Playback Triggered (Play)")
            recent_lock = bool(0)

    if((dt.datetime.now() - last_detection) > threshold):
        print("[", dt.datetime.now(), "] =>", "No eyes for", dt.datetime.now() - last_detection)
        if not recent_lock:
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            print("[ Accessibility ] => Media Playback Triggered (Pause)")
            os.system('rundll32.exe user32.dll,LockWorkStation')
            sleep(5)
            recent_lock = bool(1)

    cv.imshow('Webcam', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
