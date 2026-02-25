# utils/audio_utils.py

import soundfile as sf
import numpy as np
from config.logging_config import get_logger

logger = get_logger(__name__)

class AudioSaveError(Exception):
    """Custom exception for audio saving failures."""
    pass

def save_audio(audio_array, sample_rate, file_path):
    """
    Save audio array to a WAV file.
    
    Requirements:
    - Convert to float32
    - Guard zero-division normalization
    - Transpose shape from (channels, samples) -> (samples, channels)
    - Use soundfile.write
    """
    try:
        # Convert to float32
        audio_array = audio_array.astype(np.float32)
        
        # Guard zero-division normalization
        max_val = np.max(np.abs(audio_array))
        if max_val > 0:
            audio_array = audio_array / max_val
        
        # Transpose shape from (channels, samples) -> (samples, channels)
        # Note: If input is (1, samples), it becomes (samples, 1)
        if len(audio_array.shape) == 2:
            audio_array = audio_array.T
            
        sf.write(file_path, audio_array, sample_rate)
        logger.info(f"Successfully saved audio to {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to save audio to {file_path}: {e}")
        raise AudioSaveError(f"Failed to save audio: {e}")
