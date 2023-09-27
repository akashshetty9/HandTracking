import math
import cv2
import time
import numpy
import numpy as np

import Handtrackinhmodule as ht
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
vol=0
volba=400
volper=0


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumerange = volume.GetVolumeRange()

min = volumerange[0]
max = volumerange[1]

cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,800)
ptime=0

detector = ht.Handdetector(detectionCon=0.8)
while True:
    sucess,img = cap.read()

    img = detector.findhands(img)
    landmark = detector.position(img,draw=False)
    if (len(landmark) != 0):
       # print(landmark[4],landmark[8])


        x1,y1 = landmark[4][1],landmark[4][2]
        x2, y2 = landmark[8][1], landmark[8][2]
        xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
        cv2.circle(img, (xc, yc), 15, (255, 0, 0), cv2.FILLED)

        length = math.hypot((x2-x1),y2-y1)
        #print(length)

        vol = np.interp(length,[50,300],[min,max])
        volba= np.interp(length,[50,300],[480,150])
        volper = np.interp(length,[50,300],[0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)



        if length < 50:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)


    cv2.rectangle(img, (58, int(volba)), (85, 400), (0, 255, 0), 3, cv2.FILLED)
    cv2.putText(img,f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime =ctime
    cv2.putText(img,f'FPS : {int(fps)}',(50,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    cv2.imshow("image",img)
    cv2.waitKey(1)