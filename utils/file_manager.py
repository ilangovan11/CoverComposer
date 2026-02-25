# utils/file_manager.py

import os
import uuid
import time
from pathlib import Path
from config.settings import OUTPUT_DIR
from config.logging_config import get_logger

logger = get_logger(__name__)

def ensure_output_dir():
    """
    Ensure the output directory exists.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"Ensured output directory exists: {OUTPUT_DIR}")

def generate_filename() -> str:
    """
    Generate a unique filename using UUID4.
    """
    return f"{uuid.uuid4()}.wav"

def cleanup_old_files(hours: int = 24):
    """
    Delete .wav files older than specified hours.
    No aggressive deletion; only targets .wav in OUTPUT_DIR.
    """
    if not os.path.exists(OUTPUT_DIR):
        return

    now = time.time()
    cutoff = now - (hours * 3600)
    
    deleted_count = 0
    for file_path in Path(OUTPUT_DIR).glob("*.wav"):
        if file_path.stat().st_mtime < cutoff:
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                logger.error(f"Failed to delete {file_path}: {e}")
                
    if deleted_count > 0:
        logger.info(f"Cleaned up {deleted_count} old audio files.")
