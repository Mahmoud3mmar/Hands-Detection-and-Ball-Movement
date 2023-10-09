import mediapipe as mp
import cv2
import socket



# path="istockphoto-157179536-612x612.jpg"
# image = cv2.imread(path)
# mp_hands = mp.solutions.hands



cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 20:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
                
    cv2.imshow("Output", image)
    cv2.waitKey(1)



                










# data=""

# with mp_hands.Hands(static_image_mode=True,
#                     max_num_hands=2,
#                     min_detection_confidence=0.7) as hands:
#     rgb= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#     flippedimage=cv2.flip(rgb,1)
#     results= hands.process(flippedimage)
#     image_height,image_width,_=image.shape
#     for hand_landmarks in results.multi_hand_landmarks :
#         for point in range(21):
#             data+=str(hand_landmarks.landmark[point].x*image_width)+","+str(hand_landmarks.landmark[point].y*image_height)+","

# print(data)