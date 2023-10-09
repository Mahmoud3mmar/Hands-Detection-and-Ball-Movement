import mediapipe as mp
import cv2
import socket



path="istockphoto-157179536-612x612.jpg"
image = cv2.imread(path)
mp_hands = mp.solutions.hands














data=""

with mp_hands.Hands(static_image_mode=True,
                    max_num_hands=2,
                    min_detection_confidence=0.7) as hands:
    rgb= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    flippedimage=cv2.flip(rgb,1)
    results= hands.process(flippedimage)
    image_height,image_width,_=image.shape
    for hand_landmarks in results.multi_hand_landmarks :
        for point in range(21):
            data+=str(hand_landmarks.landmark[point].x*image_width)+","+str(hand_landmarks.landmark[point].y*image_height)+","

print(data)