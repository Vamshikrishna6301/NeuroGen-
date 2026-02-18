# audio/intent_router.py

def normalize(text: str) -> str:
    text = text.lower().strip()
    for ch in [".", ",", "?", "!", "'"]:
        text = text.replace(ch, "")
    return text


# ---- ALIASES ----
EXIT_ALIASES = ["exit", "quit", "close voice", "stop voice", "shutdown"]
START_TYPING = ["start typing", "begin typing", "dictation mode"]
STOP_TYPING = ["stop typing", "end typing", "command mode"]

APP_REGISTRY = {
    "chrome": "start chrome",
    "browser": "start chrome",
    "notepad": "notepad",
    "camera": "start microsoft.windows.camera:"
}


def route_intent(text: str):
    if not text:
        return None

    text = normalize(text)

    # ---- SYSTEM ----
    if any(cmd in text for cmd in EXIT_ALIASES):
        return {"type": "SYSTEM_EXIT"}

    if any(cmd in text for cmd in START_TYPING):
        return {"type": "MODE", "value": "DICTATION"}

    if any(cmd in text for cmd in STOP_TYPING):
        return {"type": "MODE", "value": "COMMAND"}

    # ---- OPEN APPS ----
    if "open" in text or "launch" in text:
        for app, command in APP_REGISTRY.items():
            if app in text:
                return {"type": "OPEN_APP", "command": command}

    # ---- MOUSE ----
    if "click" in text:
        return {"type": "MOUSE_CLICK"}

    if "scroll down" in text:
        return {"type": "SCROLL", "direction": "DOWN"}

    if "scroll up" in text:
        return {"type": "SCROLL", "direction": "UP"}

    # ---- CURSOR MOVE ----
    if "move" in text or "go" in text:
        speed = "NORMAL"
        if "slow" in text:
            speed = "SLOW"
        elif "fast" in text:
            speed = "FAST"

        for direction in ["left", "right", "up", "down"]:
            if direction in text:
                return {
                    "type": "MOVE_CURSOR",
                    "direction": direction,
                    "speed": speed
                }

    # ---- DICTATION TEXT ----
    return {"type": "TEXT", "content": text}
