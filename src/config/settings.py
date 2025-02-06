"""Configuration settings for the Codacy coding standard generator."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        self.api_token: str = self._get_required_env("CODACY_API_TOKEN")
        self.org_name: str = self._get_required_env("CODACY_ORG_NAME")
        self.provider: str = self._get_required_env("CODACY_PROVIDER")
        self.api_url: str = self._get_optional_env(
            "CODACY_API_URL", 
            "https://app.codacy.com"
        )
        self.log_level: str = self._get_optional_env("LOG_LEVEL", "INFO")

    @staticmethod
    def _get_required_env(key: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            key: The environment variable key.
            
        Returns:
            The environment variable value.
            
        Raises:
            ValueError: If the environment variable is not set.
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value

    @staticmethod
    def _get_optional_env(key: str, default: str) -> str:
        """
        Get an optional environment variable with a default value.
        
        Args:
            key: The environment variable key.
            default: The default value if the environment variable is not set.
            
        Returns:
            The environment variable value or the default value.
        """
        return os.getenv(key, default)

# Create a global settings instance
settings = Settings()
