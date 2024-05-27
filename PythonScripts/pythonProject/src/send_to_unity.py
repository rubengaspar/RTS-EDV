# send_to_unity.py
import cv2
import socket
import json
import argparse
from pose_detection import PoseDetector
from hand_detection import HandDetector


def send_to_unity(connection, data):
    message = json.dumps(data) + "\n"
    print("Sending JSON data to Unity:", message)
    connection.sendall(message.encode('utf-8'))


def main(send_to_unity_flag):
    pose_detector = PoseDetector()
    hand_detector = HandDetector()

    cap = cv2.VideoCapture(0)

    if send_to_unity_flag:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 65432)  # Ensure this matches the Unity client
        sock.bind(server_address)
        sock.listen(1)

        print("Waiting for a connection")
        connection, client_address = sock.accept()
        print("Connected to:", client_address)
    else:
        connection = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces, pose_results, pose_keypoints = pose_detector.process_frame(frame)
        hand_results, hand_keypoints = hand_detector.process_frame(frame)

        keypoints = {'pose': pose_keypoints, 'hands': hand_keypoints}

        if send_to_unity_flag:
            send_to_unity(connection, keypoints)

        frame = pose_detector.draw_keypoints(frame, faces, pose_results, pose_keypoints)
        frame = hand_detector.draw_keypoints(frame, hand_results)

        cv2.imshow('Face, Pose, and Hand Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if send_to_unity_flag:
        connection.close()
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pose and Hand Detection with optional sending to Unity.')
    parser.add_argument('--send_to_unity', action='store_true', help='Enable sending data to Unity')
    args = parser.parse_args()

    main(args.send_to_unity)
