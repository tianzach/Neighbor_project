"""
Application settings and configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings
    """
    # API Configuration
    app_name: str = "Multi-Vehicle Search API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Data Configuration
    listings_file_path: str = "listings.json"
    
    # Business Rules
    max_vehicles_per_request: int = 5
    vehicle_width: int = 10  # Fixed width in feet
    max_response_time_ms: int = 300
    
    # Performance
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Override with environment variables if they exist
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.port = int(os.getenv("PORT", self.port))


# Global settings instance
settings = Settings()