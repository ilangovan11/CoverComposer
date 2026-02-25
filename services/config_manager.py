# services/config_manager.py

import os
from dotenv import load_dotenv

# Note: Using github.dotenv based on common requirements.txt patterns if applicable, 
# but usually it's just 'dotenv'. The prompt mentioned python-dotenv.
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default=None):
    """
    Retrieve environment variables.
    """
    return os.getenv(key, default)
