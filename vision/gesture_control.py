import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np

# ================= CONFIG =================
TARGET_FPS = 30
FRAME_TIME = 1 / TARGET_FPS
INFERENCE_SKIP = 2
CURSOR_UPDATE_RATE = 60
SHOW_FEED = True

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

INNER_AREA_PERCENT = 0.7

SCROLL_TRIGGER_PX = 10     # sensitivity
SCROLL_STEP = 160          # scroll speed

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 60)

screen_w, screen_h = pyautogui.size()

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=1
)
mp_draw = mp.solutions.drawing_utils

# ================= UTILS =================
def dist(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def map_to_screen(x, y, fw, fh):
    mw = fw * (1 - INNER_AREA_PERCENT) / 2
    mh = fh * (1 - INNER_AREA_PERCENT) / 2
    sx = np.interp(x, (mw, fw - mw), (0, screen_w))
    sy = np.interp(y, (mh, fh - mh), (0, screen_h))
    return sx, sy

# ================= STATE =================
prev_x, prev_y = screen_w // 2, screen_h // 2
last_frame_time = 0
last_cursor_update = 0
frame_count = 0

click_state = "OPEN"
scroll_mode = False
scroll_anchor_y = None
scroll_accum = 0

# ================= MAIN LOOP =================
while True:
    now = time.time()
    if now - last_frame_time < FRAME_TIME:
        continue
    last_frame_time = now

    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    fh, fw = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_count += 1
    if frame_count % INFERENCE_SKIP != 0:
        if SHOW_FEED:
            cv2.imshow("Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        continue

    result = hands.process(rgb)
    if not result.multi_hand_landmarks:
        scroll_mode = False
        scroll_anchor_y = None
        scroll_accum = 0
        if SHOW_FEED:
            cv2.imshow("Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        continue

    hand = result.multi_hand_landmarks[0]
    mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # ===== CURSOR (Ring MCP) =====
    anchor = hand.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    target_x, target_y = map_to_screen(anchor.x * fw, anchor.y * fh, fw, fh)

    dx = abs(target_x - prev_x)
    dy = abs(target_y - prev_y)
    alpha = 0.9 if dx + dy > 60 else 0.6

    curr_x = prev_x + (target_x - prev_x) * alpha
    curr_y = prev_y + (target_y - prev_y) * alpha

    if now - last_cursor_update > 1 / CURSOR_UPDATE_RATE:
        pyautogui.moveTo(curr_x, curr_y)
        last_cursor_update = now
        prev_x, prev_y = curr_x, curr_y

    # ===== LANDMARKS =====
    index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]

    # ===== CLICK (Thumb + Index) =====
    pinch_index = dist(index_tip, thumb_tip)
    wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
    hand_size = dist(wrist, middle_tip)

    click_enter = 0.30 * hand_size
    click_exit  = 0.45 * hand_size

    if click_state == "OPEN" and pinch_index < click_enter:
        pyautogui.click()
        click_state = "COOLDOWN"
    elif click_state == "COOLDOWN" and pinch_index > click_exit:
        click_state = "OPEN"

    # ===== SCROLL MODE (Index + Middle UP) =====
    index_up = index_tip.y < hand.landmark[6].y
    middle_up = middle_tip.y < hand.landmark[10].y

    if index_up and middle_up:
        if not scroll_mode:
            scroll_mode = True
            scroll_anchor_y = middle_tip.y
            scroll_accum = 0
    else:
        scroll_mode = False
        scroll_anchor_y = None
        scroll_accum = 0

    # ===== SCROLL ACTION =====
    if scroll_mode and scroll_anchor_y is not None:
        dy = (middle_tip.y - scroll_anchor_y) * screen_h
        scroll_accum += dy
        scroll_anchor_y = middle_tip.y

        if abs(scroll_accum) >= SCROLL_TRIGGER_PX:
            direction = 1 if scroll_accum > 0 else -1
            pyautogui.scroll(direction * SCROLL_STEP)
            scroll_accum = 0

    # ===== DISPLAY =====
    if SHOW_FEED:
        cv2.putText(frame, f"Scroll: {scroll_mode}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)
        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
