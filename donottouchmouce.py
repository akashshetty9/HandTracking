import cv2
import numpy as np
import Handtrackinhmodule as hm
import time
import autopy

cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,600)
pTime=0

detector = hm.Handdetector(maxHands=1)

while True:


    sucess,img = cap.read()
    ima = detector.findhands(img)
    landmarklist= detector.position(img)

    if len(landmarklist) !=0:
        x1,y1 = landmarklist[8][1:]
        x2, y2 = landmarklist[12][1:]
        print(x1,x2,y1,y2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)