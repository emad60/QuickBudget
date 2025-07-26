"""
Settings management for application configuration.
"""

from typing import Dict, Any, Optional, Tuple
import json
import os


class SettingsManager:
    """Manages application settings and configuration."""
    
    def __init__(self):
        self.default_settings = {
            'sales_collection_current': 0.6,
            'sales_collection_next': 0.4,
            'purchases_payment_current': 0.5,
            'purchases_payment_next': 0.5,
            'ending_inventory_pct': 0.2,
            'external_financing_ratio': 0.3,
            'working_capital_turnover': 2.0,
            'beginning_cash': 100000
        }
        self.settings = self.default_settings.copy()
    
    def get_setting(self, key: str) -> float:
        """Get a setting value."""
        return self.settings.get(key, self.default_settings.get(key, 0.0))
    
    def set_setting(self, key: str, value: float) -> bool:
        """Set a setting value."""
        try:
            if key in self.default_settings:
                self.settings[key] = float(value)
                return True
            return False
        except (ValueError, TypeError):
            return False
    
    def get_all_settings(self) -> Dict[str, float]:
        """Get all current settings."""
        return self.settings.copy()
    
    def update_settings(self, new_settings: Dict[str, float]) -> bool:
        """Update multiple settings at once."""
        try:
            for key, value in new_settings.items():
                if key in self.default_settings:
                    self.settings[key] = float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self.default_settings.copy()
    
    def validate_settings(self) -> Tuple[bool, str]:
        """Validate current settings."""
        try:
            for key, value in self.settings.items():
                if not isinstance(value, (int, float)):
                    return False, f"Setting '{key}' must be a number"
                if value < 0:
                    return False, f"Setting '{key}' must be non-negative"
            
            # Validate percentage settings
            percentage_settings = [
                'sales_collection_current', 'sales_collection_next',
                'purchases_payment_current', 'purchases_payment_next',
                'ending_inventory_pct', 'external_financing_ratio'
            ]
            
            for setting in percentage_settings:
                if self.settings[setting] > 1.0:
                    return False, f"Setting '{setting}' must be between 0 and 1"
            
            return True, "Settings validation passed"
            
        except Exception as e:
            return False, f"Settings validation error: {str(e)}"
    
    def save_to_file(self, filename: str = "settings.json") -> bool:
        """Save settings to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_from_file(self, filename: str = "settings.json") -> bool:
        """Load settings from JSON file."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Validate loaded settings
                for key, value in loaded_settings.items():
                    if key in self.default_settings:
                        self.settings[key] = float(value)
                return True
            return False
        except Exception:
            return False
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings."""
        return {
            'total_settings': len(self.settings),
            'settings': self.settings.copy(),
            'has_custom_values': self.settings != self.default_settings
        } 