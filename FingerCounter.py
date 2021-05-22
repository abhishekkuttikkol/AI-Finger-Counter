import cv2
import time
import os
import HandTrackingModule as htm

##############################
wCam, hCam = 640, 480
##############################

cap = cv2.VideoCapture(0)
# cap.open('http://192.168.1.199:8080/video') 
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.85)
tipId = [ 4, 8, 12, 16, 20]

# folderPath = "Finger Counter\\FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []

# for imPath in myList:
#     img = cv2.imread(f'{folderPath}/{imPath}')
#     overlayList.append(img)


while cap.isOpened():
    success, image = cap.read()
    # image[0:200, 0:200] = overlayList[0]
    image = detector.findhands(image, draw=False)
    lmList = detector.findPosition(image, draw=False)
    # print(lmList)
    fingers = []
    if len(lmList) !=0:
        if lmList[tipId[0]][2] < lmList[tipId[0]-1][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipId[id]][2] < lmList[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
        totalFingers = fingers.count(1)
        print(totalFingers)
        cv2.rectangle(image ,(20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, f'{int(totalFingers)}', (50, 375), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 5, (255, 0, 255), 25)
            

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    cv2.putText(image, f'{int(fps)}', (500, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 0, 255), 3)
    cv2.imshow("image", image)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
cap.release()  