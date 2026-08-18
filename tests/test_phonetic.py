from voice.phonetic import parse_phonetic_cues

def test_bracket_cue():
    text,cues=parse_phonetic_cues('Hello [chuckle] world [sigh].')
    assert 'chuckle' in cues[0]
    assert 'sigh' in cues[1]
    assert '[chuckle]' not in text

def test_parenthetical_cue():
    text,cues=parse_phonetic_cues('Hello (soft laugh) there.')
    assert cues
    assert '(soft laugh)' not in text
