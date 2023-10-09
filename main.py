import mediapipe as mp
import cv2
import socket



# path="istockphoto-157179536-612x612.jpg"
# image = cv2.imread(path)
# mp_hands = mp.solutions.hands


#Create a VideoCapture object (cap) to access the webcam.
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    # Read a frame from the webcam using cap.read()
    success, image = cap.read()
    # Convert the BGR image to RGB format because MediaPipe expects RGB input.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(imageRGB)
    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            # For each landmark (lm) in the hand, extract its coordinates and calculate the center (cx, cy).
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                # 
                cx, cy = int(lm.x * w), int(lm.y * h)
                # if the landmark ID is 20 (usually a fingertip), draw a filled circle at that location.
                # if id == 20:
                #     cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                # Use mpDraw.draw_landmarks to draw landmarks and connections on the image.
                mpDraw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
                
    cv2.imshow("Output", image)

    # Check for a key press. If 'x' is pressed, exit the loop.
    key = cv2.waitKey(1)
    if key == ord('x'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()



                










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