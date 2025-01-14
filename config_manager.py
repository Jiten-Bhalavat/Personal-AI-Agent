import os
from dotenv import load_dotenv, find_dotenv

class ConfigManager:
    """Handles environment configuration and API key management."""
    
    def __init__(self):
        self.env_loaded = False
        self._load_environment()

    def _load_environment(self):
        """Loads environment variables from .env file."""
        if not self.env_loaded:
            load_dotenv(find_dotenv())
            self.env_loaded = True

    def get_api_key(self, key_name):
        """Retrieves the API key for a given key name."""
        api_key = os.getenv(key_name)
        if not api_key:
            raise ValueError(f"API key for {key_name} not found. Check your environment settings.")
        return api_key
