"""Logging configuration for the Codacy coding standard generator."""
import logging
import os
from datetime import datetime
from pathlib import Path
from rich.logging import RichHandler
from src.config.settings import settings

def setup_logger(output_path: str = None, verbose: bool = False) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        output_path: Optional custom path for the log file.
        verbose: Whether to enable debug logging.
        
    Returns:
        Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger("codacy_standard")
    logger.setLevel(logging.DEBUG if verbose else getattr(logging, settings.log_level))

    # Create formatters
    console_formatter = logging.Formatter("%(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler with rich formatting
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if verbose else getattr(logging, settings.log_level))
    logger.addHandler(console_handler)

    # File handler
    if not output_path:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        output_path = log_dir / f"codacy_standard_{datetime.now().strftime('%Y-%m-%d')}.log"

    file_handler = logging.FileHandler(output_path)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)  # Always log everything to file
    logger.addHandler(file_handler)

    return logger

def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    
    Returns:
        Logger instance.
    """
    return logging.getLogger("codacy_standard")
