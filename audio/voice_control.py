# audio/voice_control.py

import sounddevice as sd
import numpy as np
import webrtcvad
from faster_whisper import WhisperModel
import queue
import sys

# ================= CONFIG =================
SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

MAX_VOICED_FRAMES = 50
VAD_AGGRESSIVENESS = 1

# ================= VAD =================
vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
audio_queue = queue.Queue()

# ================= MODEL =================
print("🔄 Loading faster-whisper (GPU)...")
model = WhisperModel(
    "tiny",
    device="cuda",
    compute_type="float16"
)
print("✅ Model loaded")

# ================= AUDIO CALLBACK =================
def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

# ================= GENERATOR =================
def listen():
    """
    Generator that yields transcribed text.
    Owns microphone stream lifecycle.
    """

    stream = sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_SIZE,
        dtype="int16",
        channels=1,
        callback=audio_callback
    )

    stream.start()
    print("🎙️ Microphone stream started")

    try:
        while True:
            voiced_frames = []
            speech_active = False

            while True:
                frame = audio_queue.get()

                if vad.is_speech(frame, SAMPLE_RATE):
                    speech_active = True
                    voiced_frames.append(frame)

                    if len(voiced_frames) >= MAX_VOICED_FRAMES:
                        break

                elif speech_active:
                    break

            if not voiced_frames:
                continue

            audio = (
                np.frombuffer(b"".join(voiced_frames), dtype=np.int16)
                .astype(np.float32) / 32768.0
            )

            segments, _ = model.transcribe(
                audio,
                language="en",
                temperature=0.0,
                vad_filter=False
            )

            text = " ".join(seg.text for seg in segments).strip().lower()
            if text:
                yield text

    finally:
        stream.stop()
        stream.close()
        print("🛑 Microphone stream stopped")
