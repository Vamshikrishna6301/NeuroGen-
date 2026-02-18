# audio/voice_state_machine.py

class VoiceStateMachine:
    """
    Voice interaction state controller.
    This file has NO side effects.
    """

    COMMAND = "COMMAND"
    DICTATION = "DICTATION"
    DISABLED = "DISABLED"

    def __init__(self):
        self._state = self.COMMAND

    # ---------- STATE GETTERS ----------

    def get_state(self):
        return self._state

    def is_command_mode(self):
        return self._state == self.COMMAND

    def is_dictation_mode(self):
        return self._state == self.DICTATION

    def is_disabled(self):
        return self._state == self.DISABLED

    # ---------- STATE SETTERS ----------

    def set_command_mode(self):
        self._state = self.COMMAND
        print("[STATE] → COMMAND")

    def set_dictation_mode(self):
        self._state = self.DICTATION
        print("[STATE] → DICTATION")

    def disable(self):
        self._state = self.DISABLED
        print("[STATE] → DISABLED")

    # ---------- TEXT-BASED TRANSITIONS ----------

    def handle_mode_switch(self, text: str) -> bool:
        """
        Detects and applies mode switch commands.
        Returns True if a mode switch occurred.
        """

        if not text:
            return False

        text = text.lower()

        if "start typing" in text:
            self.set_dictation_mode()
            return True

        if "stop typing" in text:
            self.set_command_mode()
            return True

        if "disable voice" in text:
            self.disable()
            return True

        if "enable voice" in text:
            self.set_command_mode()
            return True

        return False
