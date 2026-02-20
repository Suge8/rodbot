"""Configuration module for rodbot."""

from rodbot.config.loader import load_config, get_config_path
from rodbot.config.schema import Config

__all__ = ["Config", "load_config", "get_config_path"]
