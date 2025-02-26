import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key

keyboard = Controller()

detector = HandDetector(detectionCon=0.7, maxHands=2)

cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

last_key = None

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]  
        cx, cy = hand["center"]  # Get hand center x-coordinate

        # Reassign hand labels based on x-position in the flipped image
        image_center_x = img.shape[1] // 2  # Midpoint of the screen
        if cx < image_center_x:
            hand_type = "Left"  # Appears on the left of flipped image, but is the right hand
        else:
            hand_type = "Right"  # Appears on the right of flipped image, but is the left hand

        if hand_type == "Left":  # Corrected logic
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)

            cv2.putText(img, f'Fingers: {totalFingers}', (50, 50), 
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2)

            # Key press logic remains the same
            if totalFingers == 5 and last_key != "right":
                keyboard.press(Key.right)
                keyboard.release(Key.left)
                last_key = "right"
            elif totalFingers == 0 and last_key != "left":
                keyboard.press(Key.left)
                keyboard.release(Key.right)
                last_key = "left"

    cv2.imshow('Camera Feed', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
