from __future__ import annotations
import os

def build_persona_context(persona, memories):
    return f"""You are {persona['name']}, a fictional AI persona.\nRole: {persona.get('role','AI companion')}\nDescription: {persona.get('description','')}\nTraits: {', '.join(persona.get('traits',[]))}\nPersonality: {persona.get('personality',{})}\nBackground: {persona.get('background',{})}\nSpeaking style: {persona.get('speaking_style',{})}\nRelationship: {persona.get('relationship',{})}\nRelevant memories: {memories}\nStay in character. Be natural and conversational. Do not claim to be human."""

def _fallback(message, persona):
    name=persona.get('name','Aria')
    return f"I'm here with you. Tell me more about that. — {name}"

def generate_persona_response(message, persona, history, memories):
    key=os.getenv('GOOGLE_API_KEY')
    if not key:
        return _fallback(message,persona)
    try:
        from google import genai
        client=genai.Client(api_key=key)
        context=build_persona_context(persona,memories)
        transcript='\n'.join(f"{m.get('role')}: {m.get('content')}" for m in history[-12:])
        prompt=f"{context}\nConversation:\n{transcript}\nUser: {message}\nRespond only as the persona. Use occasional bracketed vocal cues such as [chuckle] or [sigh] only when genuinely appropriate."
        response=client.models.generate_content(model='gemini-2.5-flash',contents=prompt)
        return (response.text or '').strip() or _fallback(message,persona)
    except Exception:
        return _fallback(message,persona)
