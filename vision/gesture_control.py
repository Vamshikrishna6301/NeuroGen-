import cv2
import mediapipe as mp
import pyautogui
import math
import time

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# ================= CURSOR SMOOTHING =================
prev_x, prev_y = 0, 0
SMOOTHING = 0.7   # 0.6–0.8 (higher = smoother)

# ================= CLICK CONFIG =================
PINCH_ENTER = 0.13
CLICK_COOLDOWN = 0.6
CLICK_LOCK_TIME = 0.15

last_click_time = 0
cursor_locked_until = 0

# ================= SCROLL CONFIG =================
prev_scroll_y = None
SCROLL_DEADZONE = 0.004
SCROLL_SPEED = 2.5
MAX_SCROLL = 120

# ================= UTILS =================
def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_time = time.time()

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        thumb = hand.landmark[4]
        index = hand.landmark[8]
        middle = hand.landmark[12]

        pinch_dist = distance(thumb, index)

        # ========== CURSOR ==========
        if current_time > cursor_locked_until:
            target_x = index.x * screen_w
            target_y = index.y * screen_h

            curr_x = prev_x + (target_x - prev_x) * SMOOTHING
            curr_y = prev_y + (target_y - prev_y) * SMOOTHING

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

        # ========== CLICK ==========
        if pinch_dist < PINCH_ENTER:
            if current_time - last_click_time > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = current_time
                cursor_locked_until = current_time + CLICK_LOCK_TIME

                cv2.putText(frame, "CLICK", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3)

        # ========== SCROLL ==========
        index_up = index.y < hand.landmark[6].y
        middle_up = middle.y < hand.landmark[10].y

        if index_up and middle_up:
            if prev_scroll_y is None:
                prev_scroll_y = index.y
            else:
                delta = prev_scroll_y - index.y

                if abs(delta) > SCROLL_DEADZONE:
                    scroll_amount = -int(delta * screen_h * SCROLL_SPEED)
                    scroll_amount = max(-MAX_SCROLL, min(MAX_SCROLL, scroll_amount))
                    pyautogui.scroll(scroll_amount)

                prev_scroll_y = index.y

            cv2.putText(frame, "SCROLL", (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
        else:
            prev_scroll_y = None

        # ========== DEBUG ==========
        cv2.putText(frame, f"Pinch: {pinch_dist:.2f}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("NeuroGen++ Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
