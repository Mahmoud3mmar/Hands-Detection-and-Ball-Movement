# import mediapipe as mp
# import cv2
# import socket

# # Create a VideoCapture object (cap) to access the webcam.
# cap = cv2.VideoCapture(0)
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mpDraw = mp.solutions.drawing_utils


# # Create a socket to connect to the C# server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('127.0.0.1', 12345)  # Change the IP and port as needed
# client_socket.connect(server_address)


# while True:
#     # Read a frame from the webcam using cap.read()
#     success, image = cap.read()
#     # Convert the BGR image to RGB format because MediaPipe expects RGB input.
#     imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     results = hands.process(imageRGB)
#     # Initialize a list to store the coordinates
#     coordinates = []
#     # Checking whether a hand is detected
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:  # Working with each hand
#             # For each landmark (lm) in the hand, extract its coordinates and calculate the center (cx, cy).
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = image.shape
#                 # 
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 # Print the (x, y) coordinates of the landmark
#                 print(f"Landmark {id}: ({cx}, {cy})")
#                 # Use mpDraw.draw_landmarks to draw landmarks and connections on the image.
#                 mpDraw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

#     cv2.imshow("Output", image)

#     # Check for a key press. If 'x' is pressed, exit the loop.
#     key = cv2.waitKey(1)
#     if key == ord('x'):
#         break

# # Release the camera and close the OpenCV window
# cap.release()
# cv2.destroyAllWindows()
# # Close the socket connection
# client_socket.close()



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
    # Initialize a list to store the coordinates
    coordinates = []

    # Checking whether a hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:  # Working with each hand
            # For each landmark (lm) in the hand, extract its coordinates and calculate the center (cx, cy).
            for lm in hand_landmarks.landmark:
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Append the (x, y) coordinates to the list
                coordinates.extend([cx, cy])

            # Use mpDraw.draw_landmarks to draw landmarks and connections on the image.
            mpDraw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Convert the list of coordinates to a comma-separated string
    coordinates_str = ','.join(map(str, coordinates))

    # Send the coordinates to the connected C# client
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