import cv2
import mediapipe as mpi
import time

capture = cv2.VideoCapture(0)

myhand = mpi.solutions.hands
hands = myhand.Hands()  # right click it will show the class if you want to pass the perameters
mpiDraw = mpi.solutions.drawing_utils

pTime  = 0
cTime =  0
while True:
    sucess, img = capture.read()

    imgRgb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    results = hands.process(imgRgb)  # we will be getting all the information hear
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for hand0 in results.multi_hand_landmarks:
            for id,landm in enumerate(hand0.landmark):
                # print(id,landm)
                hight,width,chanel = img.shape

                cx ,cy = int(landm.x*width) , int(landm.y*hight)
                print(id ,cx, cy)
                #if id ==0:
                cv2.circle(img,(cx,cy),10,(255,0,255), cv2.FILLED)
            mpiDraw.draw_landmarks(img, hand0,myhand.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)  # if we put 0 it will have its image only
