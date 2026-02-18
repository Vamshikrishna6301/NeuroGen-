# audio/voice_main.py

from voice_control import listen
from voice_state_machine import VoiceStateMachine
from intent_router import route_intent
from command_executor import execute_intent
from dictation_mode import type_text

print("🎧 NeuroGen++ Voice System Ready")
print("Say: start typing / stop typing / exit")
print("Try: open chrome, open camera\n")

state = VoiceStateMachine()

def main():
    try:
        for text in listen():
            print(f"[VOICE] {text}")

            intent = route_intent(text)
            if not intent:
                continue

            # MODE SWITCH
            if intent["type"] == "MODE":
                if intent["value"] == "DICTATION":
                    state.set_dictation_mode()
                else:
                    state.set_command_mode()
                continue

            if state.is_disabled():
                continue

            if state.is_command_mode():
                execute_intent(intent)

            elif state.is_dictation_mode():
                if intent["type"] == "TEXT":
                    type_text(intent["content"])

    except KeyboardInterrupt:
        print("\n👋 Voice stopped by user")
    except SystemExit:
        print("\n👋 Exit command received")

if __name__ == "__main__":
    main()
