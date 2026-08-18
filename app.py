from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import streamlit as st

from persona.persona_manager import DEFAULT_PERSONA, load_persona, save_persona, presets, persona_from_preset
from ai.chat import generate_persona_response
from ai.memory import add_memory, load_memories, clear_memories
from ai.emotion import infer_emotion
from voice.phonetic import parse_phonetic_cues
from voice.tts import synthesize_text
from chat.history import load_history, save_message

ROOT = Path(__file__).resolve().parent
PERSONA_PATH = ROOT / "persona" / "persona.json"

st.set_page_config(page_title="AI Persona", page_icon="✨", layout="wide")


def init_state() -> None:
    if "persona" not in st.session_state:
        st.session_state.persona = load_persona(PERSONA_PATH)
    if "messages" not in st.session_state:
        st.session_state.messages = load_history(ROOT / "chat" / "conversations.json")
    if "memories" not in st.session_state:
        st.session_state.memories = load_memories(st.session_state.persona)
    if "voice_audio" not in st.session_state:
        st.session_state.voice_audio = None


def apply_css() -> None:
    st.markdown("""
    <style>
    .stApp { background: #09090b; color: #f4f4f5; }
    .hero { padding: 1.8rem 0 1rem; }
    .hero h1 { font-size: 3.1rem; margin: 0; letter-spacing: -0.05em; }
    .hero p { color: #a1a1aa; font-size: 1.05rem; }
    .persona-card { padding: 1.2rem; border: 1px solid #27272a; border-radius: 20px; background: linear-gradient(145deg,#18181b,#101012); }
    .pill { display:inline-block; padding:.3rem .65rem; border:1px solid #3f3f46; border-radius:999px; margin:.15rem; color:#d4d4d8; font-size:.82rem; }
    .online { color:#86efac; }
    .stButton > button { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)


init_state()
apply_css()
p = st.session_state.persona

with st.sidebar:
    st.markdown("## ✨ AI PERSONA")
    page = st.radio("Navigate", ["Home", "Chat", "Create Persona", "Memory", "Voice"], label_visibility="collapsed")
    st.divider()
    st.markdown(f"### {p['name']}")
    st.caption(p.get("description", "Your AI character"))
    st.markdown('<span class="online">● Online</span>', unsafe_allow_html=True)

if page == "Home":
    st.markdown('<div class="hero"><h1>AI Persona</h1><p>Create characters. Start conversations. Bring personalities to life.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<div class='persona-card'><h2>{p['name']}</h2><p>{p.get('description','')}</p><p class='online'>● Online</p></div>", unsafe_allow_html=True)
        if st.button("💬 Start Chat", type="primary", use_container_width=True):
            st.session_state.page_jump = "Chat"
            st.rerun()
    with c2:
        st.metric("Memories", len(st.session_state.memories))
        st.metric("Messages", len(st.session_state.messages))
    st.markdown("### Personality")
    tags = p.get("traits", [])
    st.markdown(" ".join(f'<span class="pill">{x}</span>' for x in tags), unsafe_allow_html=True)

elif page == "Chat":
    st.title(f"💬 {p['name']}")
    st.caption(f"{p.get('description','')} · {p.get('relationship',{}).get('type','companion').title()}")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="✨" if msg["role"] == "assistant" else "🙂"):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("emotion"):
                st.caption(f"{msg['emotion'].title()} · {msg.get('timestamp','')}")
    prompt = st.chat_input(f"Message {p['name']}...")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt,"timestamp":datetime.now().isoformat(timespec="seconds")})
        with st.chat_message("user", avatar="🙂"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner(f"{p['name']} is thinking..."):
                result = generate_persona_response(prompt, p, st.session_state.messages, st.session_state.memories)
                emotion = infer_emotion(result, p)
                st.markdown(result)
                st.caption(f"{emotion['emotion'].title()} · {emotion['intensity']}%")
                clean_text, cues = parse_phonetic_cues(result)
                if cues:
                    st.caption(" · ".join(cues))
                if st.button("🔊 Play response", key=f"play_{len(st.session_state.messages)}"):
                    audio = synthesize_text(clean_text, p.get("voice", {}), ROOT)
                    if audio:
                        st.audio(audio, format="audio/wav")
        item = {"role":"assistant","content":result,"emotion":emotion["emotion"],"timestamp":datetime.now().isoformat(timespec="seconds")}
        st.session_state.messages.append(item)
        save_message(ROOT / "chat" / "conversations.json", item)

elif page == "Create Persona":
    st.title("✨ Create Persona")
    with st.form("persona_form"):
        name = st.text_input("Name", p.get("name", "Aria"))
        description = st.text_area("Description", p.get("description", ""))
        role = st.text_input("Role", p.get("role", "AI companion"))
        st.markdown("### Personality")
        personality = p.get("personality", {})
        cols = st.columns(3)
        values = {}
        for i, key in enumerate(["warmth","confidence","humor","empathy","playfulness","energy","curiosity","patience","formality"]):
            with cols[i % 3]:
                values[key] = st.slider(key.title(), 0, 100, int(personality.get(key, 70)))
        traits = st.text_input("Traits (comma separated)", ", ".join(p.get("traits", [])))
        st.markdown("### Background")
        interests = st.text_input("Interests", ", ".join(p.get("background", {}).get("interests", [])))
        hobbies = st.text_input("Hobbies", ", ".join(p.get("background", {}).get("hobbies", [])))
        tone = st.selectbox("Speaking style", ["natural","casual","professional","poetic","playful","mysterious","friendly"], index=["natural","casual","professional","poetic","playful","mysterious","friendly"].index(p.get("speaking_style",{}).get("tone","natural")))
        relationship = st.selectbox("Relationship", ["friend","assistant","mentor","companion","story character","creative partner"], index=0)
        submitted = st.form_submit_button("Save Persona", type="primary")
        if submitted:
            p["name"] = name.strip() or "Aria"
            p["description"] = description
            p["role"] = role
            p["personality"] = values
            p["traits"] = [x.strip() for x in traits.split(",") if x.strip()]
            p["background"]["interests"] = [x.strip() for x in interests.split(",") if x.strip()]
            p["background"]["hobbies"] = [x.strip() for x in hobbies.split(",") if x.strip()]
            p["speaking_style"]["tone"] = tone
            p["relationship"]["type"] = relationship
            save_persona(PERSONA_PATH, p)
            st.session_state.memories = load_memories(p)
            st.success("Persona saved.")
    st.markdown("### Presets")
    for key, preset in presets().items():
        if st.button(f"Use {preset['name']} — {preset['description']}", key=f"preset_{key}"):
            st.session_state.persona = persona_from_preset(key)
            save_persona(PERSONA_PATH, st.session_state.persona)
            st.rerun()

elif page == "Memory":
    st.title("🧠 Memory")
    st.caption(f"What {p['name']} remembers about your conversations.")
    if not st.session_state.memories:
        st.info("No memories yet. Share useful details during a conversation.")
    for i, memory in enumerate(st.session_state.memories):
        st.markdown(f"**{memory.get('key','Memory')}** — {memory.get('value','')}")
    if st.button("Forget everything"):
        clear_memories(p)
        st.session_state.memories = []
        st.success("Memory cleared.")

elif page == "Voice":
    st.title("🎙️ Voice")
    voice = p.setdefault("voice", {})
    voice["speed"] = st.slider("Speed", 0.5, 2.0, float(voice.get("speed", 1.0)), 0.05)
    voice["pitch"] = st.slider("Pitch", -12, 12, int(voice.get("pitch", 0)))
    voice["warmth"] = st.slider("Warmth", 0, 100, int(voice.get("warmth", 80)))
    voice["expression"] = st.slider("Expression", 0, 100, int(voice.get("expression", 80)))
    voice["breathiness"] = st.slider("Breathiness", 0, 100, int(voice.get("breathiness", 30)))
    st.info("Voice files and ONNX models are optional. Text chat remains available without them.")
    if st.button("Save voice settings"):
        save_persona(PERSONA_PATH, p)
        st.success("Voice settings saved.")
