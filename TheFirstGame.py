import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

detector = HandDetector(detectionCon=0.7, maxHands=2)

cap = cv2.VideoCapture(0)
cap.set (3, 600)
cap.set (4,400)

last_key = None

while True:
    sucess, img = cap.read()
    img = cv2.flip (img, 1)
    hand, img = detector.findHands(img)
    if hand and hand[0]["type"] == "Left":
        fingers = detector.fingersUp(hand[0])
        totalFingers = fingers.count(1)
        cv2.putText (img, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2)
    cv2.imshow ('Camera Feed', img)
    cv2.waitKey(1)
