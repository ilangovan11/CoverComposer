# app.py

import streamlit as st
import os
from core.generator import generate_music
from utils.file_manager import ensure_output_dir
from config.logging_config import get_logger

logger = get_logger(__name__)

# Page Config
st.set_page_config(
    page_title="CoverComposer",
    page_icon="🎵",
    layout="centered"
)

def main():
    st.title("🎵 CoverComposer")
    st.markdown("Generate custom AI music tracks (CPU-Only Production Demo)")
    
    # Sidebar/Input Layout
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            mood = st.selectbox(
                "Select Mood",
                ["Happy", "Sad", "Energetic", "Calm", "Dark"]
            )
            genre = st.selectbox(
                "Select Genre",
                ["Pop", "Rock", "Jazz", "Electronic", "Classical"]
            )
            
        with col2:
            style = st.selectbox(
                "Select Style",
                ["Lo-fi", "Cinematic", "Acoustic", "8-bit"]
            )
            tempo = st.slider("Tempo (BPM)", min_value=60, max_value=180, value=120)
            
        extra_prompt = st.text_area(
            "Extra Prompt (Optional)",
            placeholder="e.g., with a heavy bassline, flute melody...",
            help="Additional instructions for the AI model."
        )

    # Generation Trigger
    if st.button("Generate Music", type="primary", use_container_width=True):
        try:
            with st.spinner("🎸 Composing your track... This can take 1-2 minutes on CPU."):
                # Orchestrate generation
                output_path = generate_music(
                    mood=mood,
                    genre=genre,
                    tempo=tempo,
                    style=style,
                    extra_prompt=extra_prompt
                )
                
                if output_path and os.path.exists(output_path):
                    st.success("✨ Track generated successfully!")
                    
                    # Audio Playback
                    with open(output_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/wav")
                        
                        # Download Button
                        st.download_button(
                            label="Download Track",
                            data=audio_bytes,
                            file_name=os.path.basename(output_path),
                            mime="audio/wav"
                        )
                else:
                    st.error("Failed to locate generated audio file.")
                    
        except Exception as e:
            logger.error(f"UI Error: {e}")
            st.error(f"Generation failed: {str(e)}")

if __name__ == "__main__":
    ensure_output_dir()
    main()
