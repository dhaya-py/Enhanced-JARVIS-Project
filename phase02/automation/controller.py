"""
Phase 02 - Automation Module
Brightness control, volume control, window management
"""

import platform
from typing import Tuple

class AutomationController:
    """Advanced automation features"""
    
    def __init__(self):
        self.os_name = platform.system()
        self.brightness_available = False
        self.volume_available = False
        
        self._check_availability()
    
    def _check_availability(self):
        """Check which features are available"""
        try:
            if self.os_name == "Windows":
                import screen_brightness_control as sbc
                self.brightness_available = True
        except ImportError:
            print("⚠ Brightness control not available (install screen-brightness-control)")
        
        try:
            if self.os_name == "Windows":
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                self.volume_available = True
        except ImportError:
            print("⚠ Volume control not available (install pycaw)")
    
    def set_brightness(self, level: int) -> Tuple[bool, str]:
        """
        Set screen brightness
        
        Args:
            level: Brightness level (0-100)
            
        Returns:
            Tuple of (success, message)
        """
        if not self.brightness_available:
            return False, "Brightness control not available"
        
        try:
            import screen_brightness_control as sbc
            
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return True, f"Brightness set to {level}%"
            
        except Exception as e:
            return False, f"Error setting brightness: {e}"
    
    def get_brightness(self) -> Tuple[bool, str]:
        """Get current brightness level"""
        if not self.brightness_available:
            return False, "Brightness control not available"
        
        try:
            import screen_brightness_control as sbc
            
            level = sbc.get_brightness()
            return True, f"Current brightness: {level}%"
            
        except Exception as e:
            return False, f"Error getting brightness: {e}"
    
    def set_volume(self, level: int) -> Tuple[bool, str]:
        """
        Set system volume
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Tuple of (success, message)
        """
        if not self.volume_available or self.os_name != "Windows":
            return False, "Volume control not available"
        
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            # Convert 0-100 to 0.0-1.0
            level = max(0, min(100, level)) / 100
            volume.SetMasterVolumeLevelScalar(level, None)
            
            return True, f"Volume set to {int(level * 100)}%"
            
        except Exception as e:
            return False, f"Error setting volume: {e}"
    
    def get_volume(self) -> Tuple[bool, str]:
        """Get current volume level"""
        if not self.volume_available or self.os_name != "Windows":
            return False, "Volume control not available"
        
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            current = volume.GetMasterVolumeLevelScalar()
            return True, f"Current volume: {int(current * 100)}%"
            
        except Exception as e:
            return False, f"Error getting volume: {e}"
    
    def mute_volume(self) -> Tuple[bool, str]:
        """Mute system volume"""
        if not self.volume_available or self.os_name != "Windows":
            return False, "Volume control not available"
        
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            volume.SetMute(1, None)
            return True, "Volume muted"
            
        except Exception as e:
            return False, f"Error muting volume: {e}"
    
    def unmute_volume(self) -> Tuple[bool, str]:
        """Unmute system volume"""
        if not self.volume_available or self.os_name != "Windows":
            return False, "Volume control not available"
        
        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            
            volume.SetMute(0, None)
            return True, "Volume unmuted"
            
        except Exception as e:
            return False, f"Error unmuting volume: {e}"

# Global automation controller instance
automation = AutomationController()
