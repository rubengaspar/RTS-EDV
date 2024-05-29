# send_to_unity.py
import time

import cv2
import socket
import json
from pose_detection import PoseDetector
from hand_detection import HandDetector
from src.hand_object import HandPointEncoder


def send_to_unity(connection, data):
    # Convert the data to JSON
    message = json.dumps(data, cls=HandPointEncoder) + "\n"
    # print("Sending JSON data to Unity:", message)
    # Send the JSON data to Unity
    connection.sendall(message.encode('utf-8'))


def establish_connection():
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 65432)
        sock.bind(server_address)
        sock.listen(1)
        print("Waiting for a connection")
        # sock.settimeout(10)
        connection, client_address = sock.accept()
        print("Connected to:", client_address)
        # Return the connection, socket and status
        return connection, sock, True
    except Exception as e:
        print("Could not establish a connection:", str(e))
        # Return None, None and status
        return None, None, False


def main():
    # pose_detector = PoseDetector()
    hand_detector = HandDetector()
    cap = cv2.VideoCapture(0)

    connection, sock, status = establish_connection()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # faces, pose_results, pose_keypoints = pose_detector.process_frame(frame)
        hand_results, hand_keypoints = hand_detector.process_frame(frame)

        if status:
            send_to_unity(connection, hand_keypoints)
            time.sleep(0.1)

        # frame = pose_detector.draw_keypoints(frame, faces, pose_results, pose_keypoints)
        frame = hand_detector.draw_keypoints(frame, hand_results)

        cv2.imshow('Hand Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if status:
        connection.close()
        sock.close()


if __name__ == "__main__":
    main()
