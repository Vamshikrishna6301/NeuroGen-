# audio/test_executor.py
from command_executor import execute_intent
import time

print("You have 3 seconds to prepare...")
time.sleep(3)

execute_intent({"type": "MOUSE_CLICK"})
time.sleep(1)

execute_intent({"type": "SCROLL", "direction": "DOWN"})
time.sleep(1)

execute_intent({"type": "MOVE_CURSOR", "direction": "right", "speed": "FAST"})
time.sleep(1)

execute_intent({"type": "MOVE_CURSOR", "direction": "down", "speed": "SLOW"})
