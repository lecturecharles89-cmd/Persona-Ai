from __future__ import annotations
import json
from pathlib import Path

def load_history(path:Path):
    try:
        if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    except Exception: pass
    return []

def save_message(path:Path,message):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=load_history(path); data.append(message)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
