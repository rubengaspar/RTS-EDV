# pose_detection.py
import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self):
        # Initialize face detection (Haar Cascade)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Initialize MediaPipe pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def extract_keypoints(self, results):
        keypoints = {}
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            selected_keypoints = {
                'nose': landmarks[self.mp_pose.PoseLandmark.NOSE],
                'left_eye': landmarks[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER],
                'right_eye': landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER],
                'left_ear': landmarks[self.mp_pose.PoseLandmark.LEFT_EAR],
                'right_ear': landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR],
                'left_shoulder': landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER],
                'right_shoulder': landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER],
                'left_elbow': landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW],
                'right_elbow': landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW],
                'left_wrist': landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST],
                'right_wrist': landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST],
                'left_hip': landmarks[self.mp_pose.PoseLandmark.LEFT_HIP],
                'right_hip': landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP],
                'left_knee': landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE],
                'right_knee': landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE],
                'left_ankle': landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE],
                'right_ankle': landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE],
            }
            keypoints = {k: {'x': v.x, 'y': v.y, 'z': v.z, 'visible': v.visibility > 0.5} for k, v in selected_keypoints.items()}
        return keypoints

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        keypoints = self.extract_keypoints(results)

        return faces, results, keypoints

    def draw_keypoints(self, frame, faces, results, keypoints):
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Draw pose landmarks and key points
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            for key, point in keypoints.items():
                if point['visible']:
                    cv2.circle(frame, (int(point['x'] * frame.shape[1]), int(point['y'] * frame.shape[0])), 10, (0, 255, 0), -1)

        return frame
