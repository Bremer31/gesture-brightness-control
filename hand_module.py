import mediapipe as mp
import cv2
import time
cap = cv2.VideoCapture(0) #creating the webcam object
mphands = mp.solutions.hands # creating hands object
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils # defining drawing object
cap.set(cv2.CAP_PROP_FPS,60) #setting the fps of the video

class HandDetector():
    def __init__(self,MAX_HANDS = 2):
        self.MAX_HANDS = MAX_HANDS

        
        self.mphands = mp.solutions.hands # creating hands object
        self.hands = self.mphands.Hands(self.MAX_HANDS)
        self.mpDraw = mp.solutions.drawing_utils # defining drawing object


    def find_hands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #changing the color of the video
        self.results = self.hands.process(imgRGB) # results of the hand tracking
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img,handLms,self.mphands.HAND_CONNECTIONS) #drawing connections and utils for the hand
        return img
    def findPosition(self,img,hand_no = 0,draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]


            for id ,lm in enumerate(my_hand.landmark): #getting id and landmark from handlms landmark
                    
                    h,w,c = img.shape
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    lmlist.append([id,cx,cy])

                    if draw:
                       cv2.circle(img,(cx,cy),15,(255,0,255),3) 
        return lmlist


        

                    

               

        


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector  =HandDetector()
    while True:
        success,img = cap.read()
        img = detector.find_hands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[4]) #write what you want to search for

            
        cTime = time.time()#gives us current time
        fps = 1 /(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


        cv2.imshow("image",img) #showing the video
        cv2.waitKey(1)  


if __name__ == '__main__':
    main()
