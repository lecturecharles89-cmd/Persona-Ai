from __future__ import annotations
from pathlib import Path

def synthesize_text(text, voice_settings, root:Path):
    """Optional TTS adapter. Returns bytes when a supported local backend is installed, otherwise None."""
    try:
        import pyttsx3
        engine=pyttsx3.init()
        engine.setProperty('rate', max(80,min(250,int(180/float(voice_settings.get('speed',1.0)) ))))
        output=root/'output'/'response.wav'
        output.parent.mkdir(parents=True,exist_ok=True)
        engine.save_to_file(text,str(output)); engine.runAndWait()
        return output.read_bytes() if output.exists() else None
    except Exception:
        return None
