# audio/dictation_mode.py
import pyautogui
import time

# ================= CONFIG =================
pyautogui.FAILSAFE = True   # move mouse to corner to emergency-stop
pyautogui.PAUSE = 0.0       # no artificial delay

MIN_TEXT_LENGTH = 1         # ignore empty / noise

# ================= DICTATION =================
def type_text(text: str):
    """
    Types given text into the active application.
    Assumes focus is already on a text field.
    """

    if not text:
        return

    text = text.strip()

    if len(text) < MIN_TEXT_LENGTH:
        return

    # Small safety delay (prevents accidental focus issues)
    time.sleep(0.05)

    # Type text followed by space (natural dictation feel)
    pyautogui.write(text + " ")
