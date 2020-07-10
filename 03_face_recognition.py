import cv2
import sys
import numpy as np
import pyautogui
import ctypes
import os
import datetime
import time
import tkinter
from tkinter import messagebox
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

counter_correct = 0  # counter variable to count number of times loop runs
counter_wrong = 0

now = datetime.datetime.now()  # extract current time
now = now.second
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0
name = sys.argv[1]
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', name]

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img = cam.read()
    # img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for(x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if(confidence > 80):  # confidence usually comes greater than 80 for strangers
            counter_wrong += 1
            print("Wrong")
            Id = "Unknown + {0:.2f}%".format(round(100 - confidence, 2))
            print(confidence)
            print("counter_wrong - " + str(counter_wrong))
            cv2.rectangle(img, (x-22, y-90), (x+w+22, y-22), (0, 0, 255), -1)
            cv2.putText(img, str(Id), (x, y-40), font, 1, (0, 0, 0), 2)
        else:  # confidence usually comes less than 80 for correct user(s)
            Id = names[1] + "{0:.2f}%".format(round(100 - confidence, 2))
            print("Verified")
            print(confidence)
            counter_correct += 1
            print("counter_correct - " + str(counter_correct))
            cv2.rectangle(img, (x-22, y-90), (x+w+22, y-22),
                          (255, 255, 255), -1)
            cv2.putText(img, str(Id), (x, y-40), font, 1, (0, 0, 0), 2)

        if(counter_wrong == 3):
            pyautogui.moveTo(48, 748)
            pyautogui.click(48, 748)
            pyautogui.typewrite("Hello Stranger!!! Whats Up.")
            cam.release()
            cv2.destroyAllWindows()
            ctypes.windll.user32.LockWorkStation()
            sys.exit()

        # if counter = 6 then program will terminate as it has recognized correct user for 6 times.
        if(counter_correct == 6):
            messagebox.showinfo(None, "Welcome dude ......!")
            cam.release()
            cv2.destroyAllWindows()
            sys.exit()

    cv2.imshow('Camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
