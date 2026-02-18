import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        pinch_dist = distance(thumb, index)

        cv2.putText(frame, f"Pinch distance: {pinch_dist:.3f}",
                    (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        if pinch_dist < 0.12:
            cv2.putText(frame, "PINCH DETECTED",
                        (30, 120), cv2.FONT_HERSHEY_SIMPLEX,
                        1.3, (0, 0, 255), 3)

    cv2.imshow("Pinch Test", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
