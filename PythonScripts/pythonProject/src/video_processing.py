import cv2
import pandas as pd

# Initialize video capture
cap = cv2.VideoCapture('../downloads/blabla.mp4')

# DataFrame to store tracking downloads
tracking_data = []

# Function to detect players and ball (simplified for example)
def detect_objects(frame):
    # Dummy function - replace with actual object detection logic
    players = [{'id': 1, 'x': 50, 'y': 50}, {'id': 2, 'x': 100, 'y': 100}]
    ball = {'x': 75, 'y': 75}
    return players, ball

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    players, ball = detect_objects(frame)

    for player in players:
        tracking_data.append({
            'timestamp': cap.get(cv2.CAP_PROP_POS_MSEC),
            'player_id': player['id'],
            'player_position_x': player['x'],
            'player_position_y': player['y'],
            'ball_position_x': ball['x'],
            'ball_position_y': ball['y']
        })

    # Display frame (for debugging)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save tracking downloads
df = pd.DataFrame(tracking_data)
df.to_csv('tracking_data.csv', index=False)