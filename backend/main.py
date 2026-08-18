from __future__ import annotations

import json, os, re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai

ROOT = Path(__file__).resolve().parents[1]
PERSONA_DIR = ROOT / "persona"
PERSONA_DIR.mkdir(exist_ok=True)

DEFAULT = {
    "id":"aria","name":"Aria","description":"A warm, intelligent and playful AI companion.",
    "traits":["warm","intelligent","playful","empathetic"],
    "personality":{"warmth":88,"confidence":76,"humor":70,"empathy":92,"playfulness":78,"energy":68,"curiosity":90,"patience":84,"formality":25},
    "speaking_style":{"tone":"natural","sentence_length":"medium","vocabulary":"natural"},
    "current_mood":{"emotion":"calm","intensity":50},"memory":[]
}

app = FastAPI(title="AI Persona API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    persona_id: str = "aria"
    history: list[dict[str, Any]] = Field(default_factory=list)

class PersonaRequest(BaseModel):
    name: str
    description: str = ""
    personality: dict[str, int] = Field(default_factory=dict)
    speaking_style: dict[str, str] = Field(default_factory=lambda:{"tone":"natural"})
    traits: list[str] = Field(default_factory=list)
    current_mood: dict[str, Any] = Field(default_factory=lambda:{"emotion":"calm","intensity":50})


def path_for(pid: str) -> Path: return PERSONA_DIR / f"{pid}.json"

def load_persona(pid: str) -> dict:
    p = path_for(pid)
    if p.exists(): return json.loads(p.read_text(encoding="utf-8"))
    if pid == "aria": return DEFAULT.copy()
    raise HTTPException(404, "Persona not found")

def save_persona(p: dict) -> None: path_for(p["id"]).write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")

def emotion(text: str, persona: dict) -> dict:
    t=text.lower()
    groups={"happy":(["happy","love","great","awesome","amazing","thank you"],82),"sad":(["sad","cry","sorry","hurt","lonely"],72),"playful":(["lol","haha","funny","joke","😂"],86),"angry":(["angry","hate","mad","furious"],90),"surprised":(["wow","really","seriously","no way"],78),"curious":(["why","how","what if"],65)}
    for e,(words,score) in groups.items():
        if any(w in t for w in words): return {"emotion":e,"intensity":score}
    return persona.get("current_mood",{"emotion":"calm","intensity":50})

def memory_extract(text: str) -> list[dict]:
    out=[]
    patterns=[(r"\bmy name is ([A-Za-z][A-Za-z '-]{1,40})", "user_name"),(r"\bi like ([^.!,?]{2,80})", "likes"),(r"\bi love ([^.!,?]{2,80})", "loves")]
    for pattern,key in patterns:
        m=re.search(pattern,text,re.I)
        if m: out.append({"key":key,"value":m.group(1).strip()})
    return out

def system_prompt(p: dict) -> str:
    mem="\n".join(f"- {m.get('key')}: {m.get('value')}" for m in p.get("memory",[])[-12:]) or "No saved memories."
    return f"""You are {p['name']}, an AI persona. {p.get('description','')}
Personality: {json.dumps(p.get('personality',{}))}
Traits: {', '.join(p.get('traits',[]))}
Speaking style: {json.dumps(p.get('speaking_style',{}))}
Memories: {mem}
Current mood: {json.dumps(p.get('current_mood',{}))}
Stay consistent with this persona. Be natural, concise and emotionally expressive. You may use occasional vocal micro-cues such as [chuckle], [sigh], [pause], [gasp] when genuinely appropriate. Never overuse cues. Never claim to be human or a real person."""

@app.get('/api/health')
def health(): return {"ok":True,"service":"ai-persona-api"}

@app.get('/api/personas')
def personas():
    result=[]
    for f in PERSONA_DIR.glob('*.json'):
        try:
            p=json.loads(f.read_text(encoding='utf-8')); result.append({k:p.get(k) for k in ['id','name','description','traits','current_mood']})
        except Exception: pass
    if not any(x.get('id')=='aria' for x in result): result.insert(0,{k:DEFAULT.get(k) for k in ['id','name','description','traits','current_mood']})
    return result

@app.post('/api/personas')
def create_persona(req: PersonaRequest):
    pid=re.sub(r'[^a-z0-9]+','-',req.name.lower()).strip('-') or 'persona'
    p={**DEFAULT,**req.model_dump(),"id":pid,"memory":[]}
    save_persona(p); return p

@app.post('/api/chat')
def chat(req: ChatRequest):
    p=load_persona(req.persona_id)
    for m in memory_extract(req.message):
        p.setdefault('memory',[]).append(m)
    p['memory']=p['memory'][-50:]
    mood=emotion(req.message,p); p['current_mood']=mood
    key=os.getenv('GEMINI_API_KEY')
    if not key: return {"text":"Your persona is ready. Add GEMINI_API_KEY to the backend environment to activate the AI brain.","emotion":mood}
    try:
        client=genai.Client(api_key=key)
        contents=[{"role":"user" if x.get('role')=='user' else 'model','parts":[{"text":x.get('content','')}]} for x in req.history[-16:]]
        contents.append({"role":"user","parts":[{"text":req.message}]})
        response=client.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-3.6-flash'),contents=contents,config={"system_instruction":system_prompt(p)})
        text=response.text or "I’m here. Tell me more."
    except Exception as exc:
        raise HTTPException(502,f"Gemini request failed: {exc}")
    save_persona(p)
    return {"text":text,"emotion":emotion(text,p),"memory":p['memory'][-3:]}
