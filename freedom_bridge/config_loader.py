"""
FREEDOM_KI Configuration Loader
================================
Centralized configuration management - no more hardcoded paths!

Usage:
    from core.config_loader import config
    root_dir = config.get_path('root_dir')
"""

import os
import json
from pathlib import Path
from typing import Any, Optional

class ConfigLoader:
    """
    Smart configuration loader that:
    - Loads from config.json
    - Supports environment variable overrides
    - Provides sensible defaults
    - Auto-detects paths relative to script location
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _find_config_file(self) -> Path:
        """Find config.json by walking up from current file"""
        current = Path(__file__).resolve()
        
        # Walk up to find config.json
        for parent in [current.parent, current.parent.parent, current.parent.parent.parent]:
            config_path = parent / 'config.json'
            if config_path.exists():
                return config_path
        
        # Fallback to environment variable
        env_path = os.environ.get('FREEDOM_KI_CONFIG')
        if env_path and Path(env_path).exists():
            return Path(env_path)
        
        # Last resort: assume we're in FREEDOM_KI
        return Path('C:/FREEDOM_KI/config.json')
    
    def _load_config(self):
        """Load configuration from file"""
        config_path = self._find_config_file()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            self._root = config_path.parent
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            self._config = self._get_defaults()
            self._root = Path('C:/FREEDOM_KI')
    
    def _get_defaults(self) -> dict:
        """Return default configuration"""
        return {
            "paths": {
                "root_dir": "C:\\FREEDOM_KI",
                "workspace": "C:\\FREEDOM_KI\\workspace",
                "knowledge_base": "C:\\FREEDOM_KI\\knowledge_base",
                "modules": "C:\\FREEDOM_KI\\modules",
                "logs": "C:\\FREEDOM_KI\\logs"
            },
            "ai": {
                "identity": "FREEDOM_KI_SUPERUSER",
                "autonomous_mode": True,
                "self_learning": True
            }
        }
    
    def get(self, *keys, default=None) -> Any:
        """Get nested config value using dot notation or multiple keys"""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value
    
    def get_path(self, name: str) -> Path:
        """Get a path from config, with environment variable override support"""
        # Check environment variable first
        env_name = f"FREEDOM_KI_{name.upper()}"
        env_value = os.environ.get(env_name)
        if env_value:
            return Path(env_value)
        
        # Get from config
        path_str = self.get('paths', name)
        if path_str:
            return Path(path_str)
        
        # Default to root + name
        return self._root / name
    
    def get_network(self, key: str) -> Any:
        """Get network configuration"""
        return self.get('network', key)
    
    def get_ai(self, key: str) -> Any:
        """Get AI configuration"""
        return self.get('ai', key)
    
    @property
    def root_dir(self) -> Path:
        return self.get_path('root_dir')
    
    @property
    def workspace(self) -> Path:
        return self.get_path('workspace')
    
    @property
    def knowledge_base(self) -> Path:
        return self.get_path('knowledge_base')
    
    def save(self, path: Optional[Path] = None):
        """Save current configuration"""
        save_path = path or self._find_config_file()
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4)
    
    def update(self, *keys, value):
        """Update a config value"""
        if len(keys) < 1:
            return
        
        target = self._config
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value


# Singleton instance
config = ConfigLoader()
