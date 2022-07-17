import cv2
from cv2 import VideoCapture
import mediapipe as mp
import numpy as np
import time
import hand_module as htm
import math

import screen_brightness_control as sbc




detector = htm.HandDetector()

pTime = 0
cTime = 0   
wCam,hCam =640,480#weidth and height

cap = VideoCapture(0)
cap.set(3,wCam) #setting width
cap.set(4,hCam)#setting height
while True:
    
    success,img = cap.read()
    img = detector.find_hands(img)
    lmlist = detector.findPosition(img,draw = False)
    if len(lmlist) != 0:
        
        x4,y4 = lmlist[4][1],lmlist[4][2]
        x8,y8 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x4 + x8) // 2,(y4 + y8)// 2
    
        cv2.circle(img,(x4,y4),15,(255,0,255),3,cv2.FILLED)
        cv2.circle(img,(x8,y8),15,(255,0,255),3,cv2.FILLED)
        cv2.circle(img,(cx,cy),3,(255,0,0),1,cv2.FILLED)
        cv2.line(img,(x4,y4),(x8,y8),(255,255,0),15)
        length = math.hypot(x8 - x4,y8-y4)
        bright = np.interp(length,[50,225],[0,100])


        print(int(length),bright)
        sbc.set_brightness(bright,display=0)
        if length < 50:
            cv2.circle(img,(cx,cy),15,(255,255,255),1,cv2.FILLED)
            
        


    cTime = time.time()#gives us current time   
    fps = 1 /(cTime-pTime)  
    pTime = cTime
    
    cv2.putText(img,f" FPS: {str(int(fps))}",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Volume control",img)
    cv2.waitKey(1)
