import pyautogui

class MusicController:
    """Controls local media playback using system media keys."""
    
    def __init__(self):
        # We can adjust these based on OS, but pyautogui works cross-platform for standard media keys
        pass
        
    def play_pause(self) -> str:
        """Toggles play/pause for the active media player."""
        try:
            pyautogui.press('playpause')
            return "⏯️ Toggled media playback."
        except Exception as e:
            return f"❌ Failed to toggle media: {str(e)}"
            
    def next_track(self) -> str:
        """Skips to the next track."""
        try:
            pyautogui.press('nexttrack')
            return "⏭️ Skipping to next track."
        except Exception as e:
            return f"❌ Failed to skip track: {str(e)}"
            
    def previous_track(self) -> str:
        """Goes to the previous track."""
        try:
            pyautogui.press('prevtrack')
            return "⏮️ Playing previous track."
        except Exception as e:
            return f"❌ Failed to go to previous track: {str(e)}"

music_controller = MusicController()
