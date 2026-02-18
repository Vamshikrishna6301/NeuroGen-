# audio/command_executor.py
import pyautogui
import os

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

SCROLL_AMOUNT = 300

MOVE_SPEED = {
    "SLOW": 10,
    "NORMAL": 25,
    "FAST": 50
}

def execute_intent(intent: dict):
    if not intent or "type" not in intent:
        return

    t = intent["type"]

    if t == "SYSTEM_EXIT":
        raise SystemExit

    if t == "OPEN_APP":
        os.system(intent["command"])
        return

    if t == "MOUSE_CLICK":
        pyautogui.click()
        return

    if t == "SCROLL":
        amt = -SCROLL_AMOUNT if intent["direction"] == "DOWN" else SCROLL_AMOUNT
        pyautogui.scroll(amt)
        return

    if t == "MOVE_CURSOR":
        step = MOVE_SPEED.get(intent["speed"], 25)
        dx, dy = 0, 0

        if intent["direction"] == "left":
            dx = -step
        elif intent["direction"] == "right":
            dx = step
        elif intent["direction"] == "up":
            dy = -step
        elif intent["direction"] == "down":
            dy = step

        pyautogui.moveRel(dx, dy)
