# core/generator.py

import torch
import os
from core.model_loader import load_model, _generation_lock, ModelLoadError
from core.prompt_builder import build_prompt
from utils.file_manager import ensure_output_dir, generate_filename, cleanup_old_files
from utils.audio_utils import save_audio, AudioSaveError
from config.settings import OUTPUT_DIR, MAX_DURATION
from config.logging_config import get_logger

logger = get_logger(__name__)

class DurationConfigError(Exception):
    """Custom exception for duration configuration errors."""
    pass

class GenerationError(Exception):
    """Custom exception for general generation failures."""
    pass

def generate_music(mood, genre, tempo, style, extra_prompt=None) -> str:
    """
    Generate music based on user inputs and return the path to the saved WAV file.
    
    Performance/Memory Requirements:
    - CPU-only execution
    - Memory safe (del tensors)
    - Thread-safe inference
    - Optimized for Streamlit-safe consumption
    """
    try:
        # Maintenance and Setup
        ensure_output_dir()
        cleanup_old_files()
        
        # Load Model and Build Prompt
        model, processor = load_model()
        prompt = build_prompt(mood, genre, tempo, style, extra_prompt)
        
        # Prepare Inputs
        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        
        # Resolve frame_rate safely
        frame_rate = None
        if hasattr(model.config, 'audio_encoder') and hasattr(model.config.audio_encoder, 'frame_rate'):
            frame_rate = model.config.audio_encoder.frame_rate
        elif hasattr(model.config, 'audio_encoder'):
            sr = getattr(model.config.audio_encoder, 'sampling_rate', None)
            hop = getattr(model.config.audio_encoder, 'hop_length', None)
            if sr and hop:
                frame_rate = sr / hop
        
        if frame_rate is None:
            logger.error("Could not resolve frame_rate for duration calculation.")
            raise DurationConfigError("Failed to resolve frame_rate from model config.")
            
        max_new_tokens = int(frame_rate * MAX_DURATION)
        
        # Inference with Lock
        with _generation_lock:
            logger.info(f"Starting generation for prompt: {prompt}")
            with torch.no_grad():
                audio_values = model.generate(
                    **inputs.to(model.device),
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    guidance_scale=3.0
                )
            logger.info("Generation complete.")
            
        # Post-processing
        # Audio values shape is (batch, channels, samples)
        # Move to CPU and convert to numpy
        audio_array = audio_values[0].cpu().numpy()
        sample_rate = model.config.audio_encoder.sampling_rate
        
        filename = generate_filename()
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        # Save Audio
        save_audio(audio_array, sample_rate, file_path)
        
        # Memory cleanup
        del audio_values
        del inputs
        
        return file_path
        
    except ModelLoadError:
        raise
    except AudioSaveError:
        raise
    except Exception as e:
        logger.error(f"Generation pipeline failed: {e}")
        raise GenerationError(f"Unexpected error during generation: {e}")
