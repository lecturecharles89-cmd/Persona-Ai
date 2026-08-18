from __future__ import annotations
import re
CUES={'chuckle':'😄 chuckle','soft laugh':'😊 soft laugh','laugh':'😂 laugh','sigh':'😮‍💨 sigh','gasp':'😮 gasp','breath':'🌬 breath','inhale':'🌬 inhale','exhale':'🌬 exhale','short pause':'⏸ short pause','long pause':'⏸ long pause','pause':'⏸ pause','whisper':'🤫 whisper','softly':'🤍 softly','emphasis':'🔊 emphasis'}
PATTERN=re.compile(r'\[(.*?)\]|\((.*?)\)',re.I)
def parse_phonetic_cues(text):
    cues=[]
    for m in PATTERN.finditer(text):
        cue=(m.group(1) or m.group(2) or '').strip().lower()
        if cue in CUES: cues.append(CUES[cue])
    clean=PATTERN.sub(lambda m: '' if (m.group(1) or m.group(2) or '').strip().lower() in CUES else m.group(0),text)
    return re.sub(r'\s+',' ',clean).strip(),cues
