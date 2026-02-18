# audio/command_executor.py
import pyautogui
import time

# ================= CONFIG =================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0

SCROLL_AMOUNT = 300

MOVE_SPEED = {
    "SLOW": 10,
    "NORMAL": 25,
    "FAST": 50
}

# ================= EXECUTOR =================
def execute_intent(intent: dict):
    """
    Executes a validated intent.
    Intent must be a dict produced by intent_router.
    """

    if not intent or "type" not in intent:
        return

    intent_type = intent["type"]

    # ---------- SYSTEM ----------
    if intent_type == "SYSTEM_EXIT":
        print("[EXECUTOR] Exit requested")
        raise SystemExit

    # ---------- MOUSE ----------
    if intent_type == "MOUSE_CLICK":
        pyautogui.click()
        print("[EXECUTOR] Mouse click")
        return

    # ---------- SCROLL ----------
    if intent_type == "SCROLL":
        direction = intent.get("direction")
        amount = -SCROLL_AMOUNT if direction == "DOWN" else SCROLL_AMOUNT
        pyautogui.scroll(amount)
        print(f"[EXECUTOR] Scroll {direction}")
        return

    # ---------- CURSOR MOVE ----------
    if intent_type == "MOVE_CURSOR":
        direction = intent.get("direction")
        speed_label = intent.get("speed", "NORMAL")
        step = MOVE_SPEED.get(speed_label, MOVE_SPEED["NORMAL"])

        dx, dy = 0, 0
        if direction == "left":
            dx = -step
        elif direction == "right":
            dx = step
        elif direction == "up":
            dy = -step
        elif direction == "down":
            dy = step

        pyautogui.moveRel(dx, dy)
        print(f"[EXECUTOR] Move {direction} ({speed_label})")
        return
