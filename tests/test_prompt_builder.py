# tests/test_prompt_builder.py

import pytest
from core.prompt_builder import build_prompt

def test_build_prompt_contains_data():
    """
    Verify prompt contains mood, genre, tempo and is non-empty.
    """
    mood = "Happy"
    genre = "Pop"
    tempo = 120
    style = "Lo-fi"
    
    prompt = build_prompt(mood, genre, tempo, style)
    
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "cheerful" in prompt.lower() or mood.lower() in prompt.lower()
    assert "pop" in prompt.lower()
    assert "120" in prompt
    assert "lo-fi" in prompt.lower()

def test_build_prompt_with_extra():
    """
    Verify extra prompt is included.
    """
    extra = "with a heavy bassline"
    prompt = build_prompt("Dark", "Electronic", 90, "Cinematic", extra)
    
    assert extra in prompt
