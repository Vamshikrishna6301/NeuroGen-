# audio/test_state_machine.py
from voice_state_machine import VoiceStateMachine

state = VoiceStateMachine()

tests = [
    "hello",
    "start typing",
    "this is dictation",
    "stop typing",
    "disable voice",
    "enable voice"
]

for t in tests:
    print("\nTEXT:", t)
    switched = state.handle_mode_switch(t)
    print("Switched:", switched)
    print("Current state:", state.get_state())
