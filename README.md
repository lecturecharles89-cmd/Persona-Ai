# ✨ AI Persona

A persona-first AI character app for creating fictional personalities, chatting with them, remembering useful details, detecting emotion, and optionally speaking responses.

## Features

- Create and customize AI personas
- Personality traits and sliders
- Gemini-powered character conversations when `GOOGLE_API_KEY` is configured
- Graceful offline fallback
- Conversation history
- Lightweight persona memory
- Emotion detection
- Phonetic micro-cue parsing
- Optional local TTS
- Mobile-friendly Streamlit interface

## Run locally

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Windows activation: `.venv\\Scripts\\activate`

macOS/Linux: `source .venv/bin/activate`

## Gemini

Set `GOOGLE_API_KEY` in your environment to enable AI responses. Never commit API keys.

## Voice assets

Optional WAV micro-cues can be placed in `sounds/`. An ONNX voice model can be placed in `voices/voice.onnx`; the repository does not include a fake model because the exact inference interface depends on the supplied model.

## Safety

Use only fictional personas or voice/likeness assets you have permission to use. Do not use the application to impersonate real people without authorization.
