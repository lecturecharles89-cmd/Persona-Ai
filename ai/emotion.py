from __future__ import annotations

def infer_emotion(text, persona):
    t=text.lower()
    rules=[('excited',['!','amazing','wow','yay']),('sad',['sorry','sad','miss','hurt']),('playful',['haha','chuckle','funny','😉']),('empathetic',['understand','feel','difficult']),('angry',['angry','furious','hate']),('curious',['why','how','really?'])]
    for emotion,terms in rules:
        if any(x in t for x in terms):
            return {'emotion':emotion,'intensity':min(95,55+len(t)//80)}
    return {'emotion':'calm','intensity':45}
