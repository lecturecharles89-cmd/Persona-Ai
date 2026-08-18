from __future__ import annotations

def load_memories(persona):
    return list(persona.get('memory',[]))

def add_memory(persona,key,value):
    item={'key':key,'value':value}
    persona.setdefault('memory',[]).append(item)
    return item

def search_memories(memories,query):
    q=query.lower()
    return [m for m in memories if q in str(m).lower()]

def clear_memories(persona):
    persona['memory']=[]
