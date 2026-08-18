"""Human-like vocal phrase and micro-cue library for Ace.

Cues are metadata, not instructions to impersonate a real person. The voice provider
is responsible for rendering supported effects naturally.
"""
MICRO_CUES = {
    "laughter": ["chuckle", "soft_chuckle", "small_laugh", "laugh", "quiet_laugh", "snicker", "teasing_laugh"],
    "breathing": ["inhale", "soft_inhale", "exhale", "slow_exhale", "deep_breath", "breath_out"],
    "hesitation": ["brief_pause", "long_pause", "hesitation", "thinking_pause", "searching_for_words"],
    "surprise": ["gasp", "soft_gasp", "sharp_inhale", "surprised_pause"],
    "emotion": ["soft_sigh", "quiet_sigh", "warm_pause", "voice_softens", "amused_breath"],
    "speech": ["emphasis", "lower_intensity", "gentle_start", "firm_finish"]
}

NATURAL_PHRASES = {
    "thinking": ["hmm...", "um...", "let me think...", "actually...", "well...", "I mean..."],
    "surprise": ["Wait—really?", "No way.", "You're kidding.", "Hold on...", "Seriously?", "Wow..."],
    "warm": ["Hey...", "I'm listening.", "Take your time.", "I understand.", "That's really sweet."],
    "playful": ["Nice try.", "Oh, you're trouble.", "Okay, I see what you're doing.", "You're actually hilarious."],
    "confidence": ["I've got you.", "Let's make it simple.", "Here's what I'd do.", "Trust me on this."],
    "comfort": ["Yeah... I get it.", "That's hard.", "You didn't deserve that.", "Take a breath."],
    "frustration": ["Okay... let's slow this down.", "That's frustrating.", "Let's figure it out."]
}

PAUSE_MS = {
    "brief": 180,
    "natural": 320,
    "dramatic": 650,
    "long": 900
}
