# services/device_manager.py

import torch
from config.settings import CPU_THREAD_LIMIT
from config.logging_config import get_logger

logger = get_logger(__name__)

def get_device():
    """
    Force torch to use CPU and set thread limits.
    Logs CUDA availability if detected but ignored.
    """
    if torch.cuda.is_available():
        logger.info("CUDA detected but ignored as per CPU-only production policy.")
    
    device = torch.device("cpu")
    
    # Set CPU thread limits for stable production execution
    torch.set_num_threads(CPU_THREAD_LIMIT)
    logger.info(f"Device set to CPU with thread limit: {CPU_THREAD_LIMIT}")
    
    return device
