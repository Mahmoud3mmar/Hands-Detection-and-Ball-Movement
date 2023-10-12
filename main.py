import mediapipe as mp
import cv2
import socket

# Create a VideoCapture object (cap) to access the webcam.
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8000)  # Listen on all available network interfaces
server_socket.bind(server_address)
server_socket.listen(1)

print("Waiting for a connection...")
connection, client_address = server_socket.accept()
print("Connected to:", client_address)

while True:
    # Read a frame from the webcam using cap.read()
    success, image = cap.read()
    # Convert the BGR image to RGB format because MediaPipe expects RGB input.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(imageRGB)
    
    left_hand_landmarks = None
    right_hand_landmarks = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if hand_landmarks.landmark[0].x < hand_landmarks.landmark[9].x:
                left_hand_landmarks = hand_landmarks
            else:
                right_hand_landmarks = hand_landmarks

    if left_hand_landmarks:
        # Print landmarks for the left hand
        left_hand_coordinates = []
        for lm in left_hand_landmarks.landmark:
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            left_hand_coordinates.extend([cx, cy])

        # Draw landmarks for the left hand
        mpDraw.draw_landmarks(image, left_hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(image, 'Right Hand', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Print the left hand landmarks
        print("Left Hand Landmarks:", left_hand_coordinates)

        # Draw text over the left hand
        cv2.putText(image, 'Right Hand', (left_hand_coordinates[0], left_hand_coordinates[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if right_hand_landmarks:
        # Print landmarks for the right hand
        right_hand_coordinates = []
        for lm in right_hand_landmarks.landmark:
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            right_hand_coordinates.extend([cx, cy])

        # Draw landmarks for the right hand
        mpDraw.draw_landmarks(image, right_hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(image, 'Left Hand', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Print the right hand landmarks
        print("Right Hand Landmarks:", right_hand_coordinates)

        # Draw text over the right hand
        cv2.putText(image, 'Left Hand', (right_hand_coordinates[0], right_hand_coordinates[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Send the coordinates to the connected C# client
    if left_hand_landmarks and right_hand_landmarks:
        coordinates_str = ','.join(map(str, left_hand_coordinates)) + '\n' + ','.join(map(str, right_hand_coordinates))
        connection.send(coordinates_str.encode())

    cv2.imshow("Output", image)

    # Check for a key press. If 'x' is pressed, exit the loop.
    key = cv2.waitKey(1)
    if key == ord('x'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Close the socket connection
connection.close()
server_socket.close()
