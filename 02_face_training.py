import cv2
import numpy as np
from PIL import Image
import os
import tkinter
from tkinter import messagebox

root = tkinter.Tk()
root.withdraw()

path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids


print("\n Training faces. It will take a few seconds. Wait ...")
#messagebox.showinfo(None, "Starting Training")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# recognizer.save() worked on Mac, but not on Pi
recognizer.write('trainer/trainer.yml')


print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
messagebox.showinfo(None, "Traning Done.............!! \n ")
