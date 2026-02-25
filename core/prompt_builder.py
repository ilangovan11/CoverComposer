# core/prompt_builder.py

def build_prompt(mood, genre, tempo, style, extra_prompt=None) -> str:
    """
    Construct a layered prompt for MusicGen based on structured inputs.
    """
    
    MOOD_MAP = {
        "Happy": "cheerful, upbeat, positive",
        "Sad": "melancholic, somber, emotional",
        "Energetic": "high-energy, driving, intense",
        "Calm": "peaceful, relaxed, ambient",
        "Dark": "mysterious, tense, atmospheric"
    }
    
    GENRE_MAP = {
        "Pop": "modern pop, catchy melody",
        "Rock": "rock, electric guitars, drums",
        "Jazz": "jazz, saxophone, swing rhythm",
        "Electronic": "electronic, synth-heavy, electronic beats",
        "Classical": "classical, orchestral, symphonic"
    }
    
    STYLE_MAP = {
        "Lo-fi": "lo-fi, chill, dusty beats",
        "Cinematic": "cinematic, epic, film score",
        "Acoustic": "acoustic, unplugged, natural",
        "8-bit": "8-bit, chiptune, retro game"
    }
    
    mood_desc = MOOD_MAP.get(mood, mood)
    genre_desc = GENRE_MAP.get(genre, genre)
    style_desc = STYLE_MAP.get(style, style)
    
    prompt_parts = [
        f"{mood_desc}",
        f"{genre_desc}",
        f"{style_desc}",
        f"at {tempo} BPM"
    ]
    
    if extra_prompt:
        prompt_parts.append(extra_prompt.strip())
        
    layered_prompt = ", ".join(prompt_parts) + "."
    
    return layered_prompt
