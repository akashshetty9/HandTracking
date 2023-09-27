import cv2
import mediapipe as mpi
import time


class Handdetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC=modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.myhand = mpi.solutions.hands
        self.hands = self.myhand.Hands(self.mode, self.maxHands,self.modelC, self.detectionCon,
                                  self.trackCon)  # right click it will show the class if you want to pass the perameters
        self.mpiDraw = mpi.solutions.drawing_utils

    def findhands(self, img, draw=True):
        imgRgb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        self.results = self.hands.process(imgRgb)  # we will be getting all the information hear
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for hand0 in self.results.multi_hand_landmarks:
                if draw:
                    self.mpiDraw.draw_landmarks(img, hand0,
                                                self.myhand.HAND_CONNECTIONS)
        return img

    def position(self, img, handnum=0, draw=True):
        landmarklist= []
        if self.results.multi_hand_landmarks:
            hand0 = self.results.multi_hand_landmarks[handnum]

            for id, landm in enumerate(hand0.landmark):
               # print(id,landm)
                height, width, chanel = img.shape
                cx, cy = int(landm.x * width), int(landm.y * height)
                #print(id, cx, cy)
                landmarklist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return landmarklist

def main():
    pTime = 0
    cTime = 0
    capture = cv2.VideoCapture(0)
    detector = Handdetector()
    while True:
        sucess, img = capture.read()
        img = detector.findhands(img)
        value = detector.position(img)
        #if len(value) != 0:
           # print(value[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
