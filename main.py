#!/usr/bin/python2.7

import cv2
import signal
import sys
import subprocess

def exit_handler(signal, frame):
    print("\nCtrl-c")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

color = (255, 255, 255)
signal.signal(signal.SIGINT, exit_handler)
angel = 0
protect_frame_count = 0
default_frame_count = 0
DEF_LIMIT = 5
PRO_LIMIT = 2

while(True):
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

    if faces == () and default_frame_count < DEF_LIMIT:
        default_frame_count += 1

    elif faces == () and DEF_LIMIT == default_frame_count and not angel == 0:
        subprocess.call(["echo 0=50% > /dev/servoblaster"], shell=True)
        default_frame_count = 0
        protect_frame_count = 0
        angel = 0

    elif not faces == () and protect_frame_count < PRO_LIMIT:
        protect_frame_count += 1

    elif not faces == () and PRO_LIMIT == protect_frame_count and not angel == -90:
        subprocess.call(["echo 0=99% > /dev/servoblaster"], shell=True)
        default_frame_count = 0
        protect_frame_count = 0
        angel = -90
    else:
        print("DEFAULT: {} PROTECT: {}".format(default_frame_count, protect_frame_count))