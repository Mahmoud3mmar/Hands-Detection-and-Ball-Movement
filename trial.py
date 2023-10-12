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
    # Initialize lists to store the coordinates for both hands
    left_hand_coordinates = []
    right_hand_coordinates = []

    # Checking whether hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Check if it's a left or right hand based on the x-coordinate of the landmarks
            is_left_hand = hand_landmarks.landmark[0].x < hand_landmarks.landmark[9].x

            # For each landmark (lm) in the hand, extract its coordinates and calculate the center (cx, cy).
            for lm in hand_landmarks.landmark:
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # Append the (x, y) coordinates to the corresponding hand list
                if is_left_hand:
                    left_hand_coordinates.append(f"{cx}.{cy}")
                else:
                    right_hand_coordinates.append(f"{cx}.{cy}")

            # Use mpDraw.draw_landmarks to draw landmarks and connections on the image.
            if is_left_hand:
                mpDraw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                cv2.putText(image, 'Left Hand', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                mpDraw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=mpDraw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
                cv2.putText(image, 'Right Hand', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

     # Print the landmarks for both hands in x.y format
    print("Left Hand Landmarks:", ', '.join(left_hand_coordinates))
    print("Right Hand Landmarks:", ', '.join(right_hand_coordinates))
    # Convert the lists of coordinates to comma-separated strings for both hands
    left_coordinates_str = ','.join(left_hand_coordinates)
    right_coordinates_str = ','.join(right_hand_coordinates)

    # Send the coordinates for both hands to the connected C# client
    connection.send(( 'Left Hand Landmarks: '+left_coordinates_str  + '\n' + 'Right Hand Landmarks:' +right_coordinates_str).encode())

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
