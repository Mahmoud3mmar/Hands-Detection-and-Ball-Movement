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



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8000)  # Change IP and port as needed
server_socket.bind(server_address)
server_socket.listen(1)

print("Waiting for a connection...")
connection, client_address = server_socket.accept()
print("Connected to:", client_address)

while True:
    try:
        # Send the data to the C# program
        connection.send(data.encode())  # Encode the data as bytes before sending
        print("Data sent successfully")  # Add this line

        # Break the loop after sending data
        break

    except Exception as e:
        print("Error:", e)
        break

# Clean up
connection.close()
server_socket.close()