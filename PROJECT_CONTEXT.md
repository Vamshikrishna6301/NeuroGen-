NeuroGen++ – Brain-Inspired Multimodal AI Assistant

🎯 Core Vision (Why this project exists)

NeuroGen++ is a real-time, multimodal intelligent personal assistant designed accessibility-first for differently-abled users:

Visually impaired

Motor impaired

Speech impaired

Cognitively challenged

Unlike traditional assistants (Alexa, Siri, Google Assistant) that rely almost entirely on voice, NeuroGen++ is brain-inspired and multimodal.

It can:

👁️ See → camera, scene understanding, OCR

🎙️ Listen → speech recognition

✋ Observe movement → gesture, gaze

😊 Sense emotion → facial expressions

🧠 Learn → reinforcement learning

🧩 Remember → contextual memory

🔄 Adapt → interaction style per user

Core idea:

Every user interacts using their strongest available senses.

🧩 High-Level Architecture

NeuroGen++ follows a layered modular architecture.

┌──────────────────────────────────────────────┐
│        Frontend / Interaction Layer          │
│  (voice-only / minimal UI / visual UI)       │
└──────────────────────────────────────────────┘
                        ▲
                        │
┌──────────────────────────────────────────────┐
│            NeuroGen++ Core Brain              │
│  Fusion Engine | Decision Engine | RL Layer   │
│  Context Memory | User Profiles               │
└──────────────────────────────────────────────┘
                        ▲
                        │
┌──────────────────────────────────────────────┐
│          Input / Output Modules               │
│ Gesture | Voice | Vision | Gaze | Emotion     │
└──────────────────────────────────────────────┘

🔑 Key Architectural Principle

Build each modality in isolation → integrate later via a central brain

This avoids fragile systems and enables clean research-grade integration.

👥 Accessibility Philosophy (CRITICAL)

NeuroGen++ does NOT use one UI for everyone.

Instead, it uses User Interaction Profiles:

UserProfile = {
  "inputs": ["gesture", "voice", "gaze"],
  "outputs": ["speech", "text", "visual"],
  "priority": "hands_free"
}

Examples

Visually impaired

Input: Voice

Output: Speech

Features: Scene narration, OCR

Motor impaired

Input: Eye tracking + voice

Output: Minimal UI

Features: Gaze-based selection

Speech impaired

Input: Gesture + gaze

Output: Text

Features: No speech dependency

➡️ Same intelligence, different interaction paths.

🛠️ Development Strategy (How the project is built)
✅ Correct approach (used)

Build each modality independently

Ensure assistive-grade stability

Optimize UX smoothness (latency, jitter, accuracy)

Integrate later using:

Multimodal Fusion Engine

Decision Engine

Context Memory

RL personalization

❌ Explicitly avoided

One giant main.py

Early UI integration

Blind GitHub cloning

Monolithic logic

📁 Project Folder Structure
NeuroGen++/
│
├── vision/
│   ├── camera_test.py
│   ├── hand_detection.py
│   ├── pinch_test.py
│   ├── gesture_control.py        ✅ DONE
│   ├── scene_understanding.py    ⏳ Phase 6
│   └── emotion_detection.py      ⏳ Phase 7
│
├── audio/
│   └── voice_control.py          ⏳ Phase 5 (IN PROGRESS – NOT FINAL)
│
├── gaze/
│   └── eye_tracking.py           ⏳ Phase 8
│
├── core/
│   ├── fusion_engine.py          ⏳ Phase 9
│   ├── decision_engine.py        ⏳ Phase 9
│   └── context_memory.py         ⏳ Phase 11
│
├── rl/
│   └── habit_learning.py         ⏳ Phase 10
│
├── llm/
│   └── assistant.py              ⏳ Phase 5B / Phase 9+
│
├── security/
│   ├── voice_auth.py             ⏳ Phase 12
│   └── face_auth.py              ⏳ Phase 12
│
└── main.py                       ⏳ Phase 13 (final integration)

✅ COMPLETED WORK (DO NOT MODIFY)
✋ Phase 1–4: Gesture Control Module — DONE

File
vision/gesture_control.py

Features implemented

Index-finger cursor movement

Thumb + index pinch → accurate single click

Index + middle finger → smooth scrolling

Cursor smoothing (low-pass filter)

Cursor lock during click (prevents jumps)

Corrected scroll direction (human-natural)

Deadzone & clamping for scroll stability

Tech

MediaPipe Hands

OpenCV

PyAutoGUI

Status

✅ Assistive-grade
✅ Stable
✅ UX-optimized
✅ Ready for multimodal integration

🔜 PLANNED PHASES (AUTHORITATIVE ROADMAP)
Phase 5: 🎙️ Voice Command System (IN PROGRESS)

Owner: Project Lead
File: audio/voice_control.py

Phase 5A – Deterministic Voice Control

Whisper STT

Commands:

enable gesture

disable gesture

click

scroll up / down

move cursor (direction + speed)

Works standalone

Phase 5B – Dictation Mode

Mode-based system:

COMMAND mode

DICTATION mode

Voice typing into any textbox

Safe switching (start typing, stop typing)

Phase 5C – GenAI Intent Router (advanced)

LLM decides:

command vs dictation vs reasoning

Structured JSON output

Execution remains deterministic

⚠️ Phase 5 is intentionally unfinished in repo
(Project Lead will complete it.)

Phase 6: 👁️ Scene Understanding

File: vision/scene_understanding.py

YOLOv8 object detection

OCR for text reading

Scene narration for visually impaired

Output: structured scene description

End state:

“What is in front of me?”

“Read the text on screen”

Phase 7: 😊 Emotion Detection

File: vision/emotion_detection.py

Facial expression recognition

Detect:

confusion

frustration

fatigue

Output emotion state

Used later by:

Fusion engine

RL personalization

Phase 8: 👁️‍🗨️ Eye Tracking

File: gaze/eye_tracking.py

Gaze-based cursor positioning

Blink-based click

For severe motor impairment

Standalone + fusion-ready.

Phase 9: 🔄 Multimodal Fusion Engine

File: core/fusion_engine.py

Inputs:

gesture

voice

gaze

emotion

Architecture:

Transformer / GRU

Output:

final intent

confidence score

This is the core research contribution.

Phase 10: 🧠 Reinforcement Learning Layer

File: rl/habit_learning.py

DQN-based personalization

Learns:

preferred modality

speed

sensitivity

Updates user profile dynamically

Phase 11: 🧩 Context Memory

File: core/context_memory.py

Short-term memory

Long-term memory

Enables:

follow-up commands

conversational continuity

Phase 12: 🔐 Secure Access

Folder: security/

Voiceprint authentication

Face authentication

Gesture-based login

Passwordless accessibility

Phase 13: 📦 Integration & Frontend

File: main.py

Minimal UI (Tkinter or Web)

Multiple accessibility modes

System demo

Final evaluation & report