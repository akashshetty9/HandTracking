import cv2
import mediapipe
import os
import time
import Handtrackinhmodule as hm

cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,800)
pTime=0

foldername = "folder_image"
mylist = os.listdir(foldername)
print(mylist)
overlaylist =[]
for imagepath in mylist:
    image = cv2.imread(f'{foldername}/{imagepath}')
    print(f'{foldername}/{imagepath}')
    overlaylist.append(image)

#print(len(overlaylist))

detector = hm.Handdetector(detectionCon=0.8)

tipid = [4,8,12,16,20]
while True:
    sucess ,img = cap.read()
    img = detector.findhands(img)
    #print(img)
    landmarklist = detector.position(img,draw=False)
    #print(landmarklist)
    if len(landmarklist) != 0:
        finfers=[]

        if landmarklist[tipid[0]][1] < landmarklist[tipid[0] - 1][1]:
            finfers.append(0)
        else:
            finfers.append(1)

        for id in range(1,5):
            if landmarklist[tipid[id]][2] < landmarklist[tipid[id]-1][2]:
                finfers.append(1)
            else:
                finfers.append(0)
        #print(finfers)
        totalfinger = finfers.count(1)
        h, w, c = overlaylist[totalfinger].shape
        img[0:h, 0:w] = overlaylist[totalfinger]
        cv2.putText(img, f'{int(totalfinger)}', (500, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,f'{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("image",img)
    cv2.waitKey(1)