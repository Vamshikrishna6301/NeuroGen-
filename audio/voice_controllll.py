import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyautogui
import os
import threading
import time

# ================= AUTO MICROPHONE SELECTION =================
def get_microphone():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0 and "microphone" in d["name"].lower():
            return i, d
    raise RuntimeError("No microphone found")

MIC_INDEX, MIC_INFO = get_microphone()
SAMPLE_RATE = int(MIC_INFO["default_samplerate"])

print(f"🎧 Using microphone [{MIC_INDEX}]: {MIC_INFO['name']}")
print(f"🎚️ Sample rate: {SAMPLE_RATE}")

# ================= CONFIG =================
MODEL_NAME = "small"
DURATION = 3  # short window for responsiveness

# ================= LOAD WHISPER =================
print("🔄 Loading Whisper model...")
model = whisper.load_model(MODEL_NAME)

# ================= GLOBAL STATE =================
MODE = "COMMAND"   # COMMAND | DICTATION
move_x = 0
move_y = 0
running = True

# ================= CURSOR MOVEMENT THREAD =================
def cursor_loop():
    global move_x, move_y, running
    while running:
        if MODE == "COMMAND" and (move_x != 0 or move_y != 0):
            pyautogui.moveRel(move_x, move_y)
        time.sleep(0.05)

threading.Thread(target=cursor_loop, daemon=True).start()

# ================= LISTEN =================
def listen(prompt):
    print(f"\n🎙️ {prompt}")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.float32,
        device=MIC_INDEX
    )
    sd.wait()

    if np.abs(audio).max() < 0.01:
        return ""

    wav.write("temp.wav", SAMPLE_RATE, audio)

    result = model.transcribe(
        "temp.wav",
        language="en",
        temperature=0.0,
        condition_on_previous_text=False
    )

    text = result["text"].strip().lower()
    print("📝 You said:", text)
    return text

# ================= COMMAND MODE =================
def handle_command(text):
    global MODE, move_x, move_y, running

    # MODE SWITCH
    if "start typing" in text:
        MODE = "DICTATION"
        move_x = move_y = 0
        print("⌨️ Dictation mode ENABLED")
        return

    # EXIT
    if any(w in text for w in ["exit", "quit"]):
        print("👋 Exiting NeuroGen Voice Control")
        running = False
        exit()

    # CLICK
    if any(w in text for w in ["click", "select", "press"]):
        pyautogui.click()
        print("🖱️ Clicked")
        return

    # OPEN APPS
    if "open" in text or "launch" in text:
        if "chrome" in text or "browser" in text:
            os.system("start chrome")
            print("🚀 Opened Chrome")
            return
        if "notepad" in text:
            os.system("notepad")
            print("📝 Opened Notepad")
            return

    # SCROLL
    if "scroll down" in text:
        pyautogui.scroll(-400)
        return
    if "scroll up" in text:
        pyautogui.scroll(400)
        return

    # CURSOR MOVE
    if "move" in text or "go" in text:
        step = 10
        if "slow" in text:
            step = 5
        elif "fast" in text:
            step = 20

        if "left" in text:
            move_x, move_y = -step, 0
        elif "right" in text:
            move_x, move_y = step, 0
        elif "up" in text:
            move_x, move_y = 0, -step
        elif "down" in text:
            move_x, move_y = 0, step

        print("➡️ Cursor moving")
        return

    # STOP CURSOR
    if text.strip() == "stop":
        move_x = move_y = 0
        print("🛑 Cursor stopped")

# ================= DICTATION MODE =================
def handle_dictation(text):
    global MODE

    if "stop typing" in text:
        MODE = "COMMAND"
        print("🎙️ Command mode ENABLED")
        return

    # Type text
    pyautogui.write(text + " ")
    print("⌨️ Typed text")

# ================= MAIN LOOP =================
while True:
    if MODE == "COMMAND":
        spoken = listen("Speak a COMMAND (or say 'start typing')")
        if spoken:
            handle_command(spoken)

    elif MODE == "DICTATION":
        spoken = listen("Dictation mode (say 'stop typing')")
        if spoken:
            handle_dictation(spoken)
