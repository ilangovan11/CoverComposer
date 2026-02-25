# core/model_loader.py

import threading
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from services.device_manager import get_device
from services.config_manager import get_env
from config.settings import MODEL_NAME
from config.logging_config import get_logger

logger = get_logger(__name__)

class ModelLoadError(Exception):
    """Custom exception for model loading failures."""
    pass

_model = None
_processor = None
_generation_lock = threading.Lock()

def load_model():
    """
    Lazy-load the MusicGen model and processor once.
    Forces CPU execution and sets model to eval mode.
    """
    global _model, _processor
    
    with _generation_lock:
        if _model is not None and _processor is not None:
            return _model, _processor
        
        try:
            logger.info(f"Cold start: Loading model {MODEL_NAME}...")
            
            device = get_device()
            hf_token = get_env("HF_TOKEN")
            
            _processor = AutoProcessor.from_pretrained(MODEL_NAME, token=hf_token)
            _model = MusicgenForConditionalGeneration.from_pretrained(
                MODEL_NAME, 
                token=hf_token
            ).to(device)
            
            _model.eval()
            
            logger.info("Model and processor loaded successfully.")
            return _model, _processor
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise ModelLoadError(f"Critical error loading AI models: {e}")
