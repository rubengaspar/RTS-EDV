import cv2
import socket
import json
from pose_detection import PoseDetector


def send_to_unity(connection, data):
    message = json.dumps(data)
    connection.sendall(message.encode('utf-8'))


def main():
    detector = PoseDetector()

    cap = cv2.VideoCapture(0)

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65432)  # Ensure this matches the Unity client
    sock.bind(server_address)
    sock.listen(1)

    print("Waiting for a connection")
    connection, client_address = sock.accept()
    print("Connected to:", client_address)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces, results, keypoints = detector.process_frame(frame)
        send_to_unity(connection, keypoints)
        frame = detector.draw_keypoints(frame, faces, results, keypoints)

        cv2.imshow('Face and Pose Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    connection.close()
    sock.close()

if __name__ == "__main__":
    main()
