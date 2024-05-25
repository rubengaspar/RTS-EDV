import cv2
from pose_detection import PoseDetector

def main():
    detector = PoseDetector()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces, results, keypoints = detector.process_frame(frame)
        frame = detector.draw_keypoints(frame, faces, results, keypoints)

        cv2.imshow('Face and Pose Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
