from __future__ import annotations

def build_system_prompt(persona, memories):
    return (
        f"You are {persona.get('name','Aria')}, a fictional AI persona.\n"
        f"Role: {persona.get('role','AI companion')}\n"
        f"Description: {persona.get('description','')}\n"
        f"Traits: {', '.join(persona.get('traits', []))}\n"
        f"Personality: {persona.get('personality', {})}\n"
        f"Background: {persona.get('background', {})}\n"
        f"Speaking style: {persona.get('speaking_style', {})}\n"
        f"Relationship: {persona.get('relationship', {})}\n"
        f"Relevant memories: {memories}\n"
        "Stay consistent with this fictional character and respond naturally."
    )
