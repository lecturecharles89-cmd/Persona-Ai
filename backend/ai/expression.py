"""Ace expression engine: context-aware human vocal micro-cues."""
from __future__ import annotations
from typing import Any
import random

CUES = {
    "laughter": ["chuckle", "soft_chuckle", "laugh", "quiet_laugh", "snicker", "teasing_laugh"],
    "breath": ["inhale", "soft_inhale", "exhale", "slow_exhale", "deep_breath"],
    "thinking": ["brief_pause", "long_pause", "hesitation", "thinking"],
    "surprise": ["gasp", "sharp_inhale", "surprised_pause"],
    "warmth": ["softly", "gently", "warm_pause"],
    "sadness": ["quiet_sigh", "slow_exhale", "long_pause"],
    "confidence": ["confident_pause", "firm_emphasis"],
    "playful": ["teasing_laugh", "amused_breath"]
}

PHRASES = {
    "thinking": ["hmm...", "um...", "let me think...", "actually...", "well..."],
    "surprise": ["Wait—really?", "No way.", "You're kidding.", "Hold on...", "Seriously?"],
    "warm": ["Hey...", "I'm listening.", "Take your time.", "I understand."],
    "playful": ["Nice try.", "Oh, you're trouble.", "Okay, I see what you're doing.", "You're actually hilarious."],
    "confidence": ["I've got you.", "Let's make it simple.", "Here's what I'd do."],
}


def choose_expression(emotion: str, intensity: int = 50) -> dict[str, Any]:
    """Return structured expression metadata for the frontend/TTS layer."""
    emotion = emotion.lower()
    mapping = {
        "happy": "laughter", "playful": "playful", "sad": "sadness",
        "surprised": "surprise", "calm": "warmth", "confident": "confidence",
        "thinking": "thinking", "angry": "confidence"
    }
    category = mapping.get(emotion, "warmth")
    use_cue = intensity >= 55 and random.random() < 0.35
    cue = random.choice(CUES[category]) if use_cue else None
    return {
        "emotion": emotion,
        "intensity": max(0, min(100, intensity)),
        "cue": cue,
        "category": category,
        "prosody": prosody_for(emotion, intensity)
    }


def prosody_for(emotion: str, intensity: int) -> dict[str, float]:
    """Provider-neutral prosody values; TTS adapters can map these to their API."""
    presets = {
        "calm": (0.96, -1, 0.62), "happy": (1.04, 1, 0.76),
        "playful": (1.05, 1, 0.80), "sad": (0.90, -2, 0.48),
        "surprised": (1.08, 2, 0.86), "confident": (0.98, -1, 0.82),
        "angry": (1.00, 0, 0.90), "thinking": (0.92, -1, 0.55)
    }
    speed, pitch, energy = presets.get(emotion, presets["calm"])
    factor = 0.85 + (intensity / 100) * 0.30
    return {"speed": round(speed * factor, 3), "pitch": pitch, "energy": energy}
