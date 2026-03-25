"""
System Actions Module for Jarvis AI Assistant
Handles system-level operations (open apps, close windows, etc.)
"""

import subprocess
import platform
import os
import time
import psutil
from typing import Optional, Tuple
from config.settings import config

class SystemActions:
    """Handles system-level operations"""
    
    def __init__(self):
        self.os_name = platform.system()
        
        # Application paths for Windows
        self.app_paths = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'paint': 'mspaint.exe',
            'taskmgr': 'taskmgr.exe',
            'task manager': 'taskmgr.exe',
            'settings': 'start ms-settings:',
            'control panel': 'control.exe',
            'control': 'control.exe',
            'vscode': 'code',
            'visual studio code': 'code',
            'word': 'start winword',
            'excel': 'start excel',
            'powerpoint': 'start powerpnt',
            'spotify': 'start spotify:',
            'discord': 'start discord:',
            'telegram': 'start telegram:',
            'whatsapp': 'start whatsapp:',
            'snipping tool': 'SnippingTool.exe',
            'edge': 'start msedge',
            'firefox': 'start firefox',
            'brave': 'start brave',
        }
        
        if config.DEBUG_MODE:
            print(f"✓ System Actions initialized (OS: {self.os_name})")
    
    def open_application(self, app_name: str) -> Tuple[bool, str]:
        """
        Open an application
        
        Args:
            app_name: Name of the application
            
        Returns:
            Tuple of (success, message)
        """
        try:
            app_name = app_name.lower()
            
            if self.os_name == "Windows":
                return self._open_app_windows(app_name)
            elif self.os_name == "Linux":
                return self._open_app_linux(app_name)
            elif self.os_name == "Darwin":  # macOS
                return self._open_app_macos(app_name)
            else:
                return False, f"Unsupported operating system: {self.os_name}"
                
        except Exception as e:
            return False, f"Error opening application: {e}"
    
    def _open_app_windows(self, app_name: str) -> Tuple[bool, str]:
        """Open application on Windows"""
        try:
            # Try direct paths first
            if app_name in self.app_paths:
                subprocess.Popen(self.app_paths[app_name])
                return True, f"Opening {app_name}"
            
            # Try using 'start' command
            subprocess.Popen(['start', app_name], shell=True)
            return True, f"Opening {app_name}"
            
        except Exception as e:
            return False, f"Could not open {app_name}: {e}"
    
    def _open_app_linux(self, app_name: str) -> Tuple[bool, str]:
        """Open application on Linux"""
        try:
            subprocess.Popen([app_name])
            return True, f"Opening {app_name}"
        except Exception as e:
            return False, f"Could not open {app_name}: {e}"
    
    def _open_app_macos(self, app_name: str) -> Tuple[bool, str]:
        """Open application on macOS"""
        try:
            subprocess.Popen(['open', '-a', app_name])
            return True, f"Opening {app_name}"
        except Exception as e:
            return False, f"Could not open {app_name}: {e}"
    
    def close_window(self) -> Tuple[bool, str]:
        """Close the active window"""
        try:
            if self.os_name == "Windows":
                # Use Alt+F4 to close active window
                import pyautogui
                pyautogui.hotkey('alt', 'f4')
                return True, "Closing active window"
            elif self.os_name == "Linux":
                os.system("xdotool key alt+F4")
                return True, "Closing active window"
            elif self.os_name == "Darwin":
                os.system("osascript -e 'tell application \"System Events\" to keystroke \"w\" using {command down}'")
                return True, "Closing active window"
            else:
                return False, "Unsupported operating system"
                
        except Exception as e:
            return False, f"Error closing window: {e}"
    
    def close_application(self, app_name: str) -> Tuple[bool, str]:
        """
        Close a specific application by name
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            Tuple of (success, message)
        """
        try:
            closed = False
            for proc in psutil.process_iter(['name']):
                try:
                    process_name = proc.info['name'].lower()
                    if app_name.lower() in process_name:
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                return True, f"Closed {app_name}"
            else:
                return False, f"{app_name} is not running"
                
        except Exception as e:
            return False, f"Error closing {app_name}: {e}"
    
    def get_system_info(self) -> dict:
        """Get basic system information"""
        try:
            return {
                'os': self.os_name,
                'os_version': platform.version(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent if self.os_name != "Windows" else psutil.disk_usage('C:').percent
            }
        except Exception as e:
            return {'error': str(e)}
    
    def lock_screen(self) -> Tuple[bool, str]:
        """Lock the computer screen"""
        try:
            if self.os_name == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return True, "Locking screen"
            elif self.os_name == "Linux":
                os.system("gnome-screensaver-command -l")
                return True, "Locking screen"
            elif self.os_name == "Darwin":
                os.system("pmset displaysleepnow")
                return True, "Locking screen"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Error locking screen: {e}"
    
    def shutdown_system(self) -> Tuple[bool, str]:
        """Shutdown the computer"""
        try:
            if self.os_name == "Windows":
                os.system("shutdown /s /t 60")
                return True, "System will shutdown in 60 seconds"
            elif self.os_name == "Linux":
                os.system("shutdown -h +1")
                return True, "System will shutdown in 1 minute"
            elif self.os_name == "Darwin":
                os.system("sudo shutdown -h +1")
                return True, "System will shutdown in 1 minute"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Error shutting down: {e}"
    
    def restart_system(self) -> Tuple[bool, str]:
        """Restart the computer"""
        try:
            if self.os_name == "Windows":
                os.system("shutdown /r /t 60")
                return True, "System will restart in 60 seconds"
            elif self.os_name == "Linux":
                os.system("shutdown -r +1")
                return True, "System will restart in 1 minute"
            elif self.os_name == "Darwin":
                os.system("sudo shutdown -r +1")
                return True, "System will restart in 1 minute"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Error restarting: {e}"
    
    def sleep_system(self) -> Tuple[bool, str]:
        """Put computer to sleep"""
        try:
            if self.os_name == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return True, "Putting system to sleep"
            elif self.os_name == "Linux":
                os.system("systemctl suspend")
                return True, "Putting system to sleep"
            elif self.os_name == "Darwin":
                os.system("pmset sleepnow")
                return True, "Putting system to sleep"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Error sleeping system: {e}"
    
    def take_screenshot(self) -> Tuple[bool, str]:
        """Take a screenshot"""
        try:
            import pyautogui
            from datetime import datetime
            
            # Create screenshots directory
            screenshots_dir = config.BASE_DIR / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"screenshot_{timestamp}.png"
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            return True, f"Screenshot saved as {filename.name}"
            
        except Exception as e:
            return False, f"Error taking screenshot: {e}"

# Global system actions instance
system_actions = SystemActions()
