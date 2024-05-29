# hand_detection.py
import cv2
import mediapipe as mp

from src.hand_object import HandPoint


class HandDetector:
    def __init__(self):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def extract_keypoints(self, results):
        keypoints = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                for id, point in enumerate(hand_landmarks.landmark):

                    hand_point = HandPoint(id, point.x, point.y, point.z)

                    keypoints.append(hand_point)

        return keypoints

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        keypoints = self.extract_keypoints(results)
        return results, keypoints

    def draw_keypoints(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame
