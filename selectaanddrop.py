import cv2
import numpy as np
import Handtrackinhmodule as hm
import time
import autopy
import mediapipe as mp


cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,600)
pTime=0
npHands = mp.solutions.hands
hands = npHands.Hands()
while True:
    sucess ,img = cap.read()

    im

    cv2.imshow("image",img)
    cv2.waitKey(1)