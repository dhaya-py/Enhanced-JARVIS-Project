"""
JARVIS PRIME - UI Launcher
Opens the Glass UI in a borderless/app Chrome window for a native desktop feel.
"""
import os
import subprocess
import webbrowser
from pathlib import Path

def launch():
    ui_path = Path(__file__).parent / "jarvis_ui" / "index.html"
    if not ui_path.exists():
        print("[PRIME:Error] UI files not found.")
        return

    # Try to use Chrome in app mode for a native feel
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    launched = False
    for path in chrome_paths:
        if os.path.exists(path):
            try:
                subprocess.Popen([path, f"--app=file:///{ui_path.resolve()}"])
                launched = True
                break
            except Exception:
                pass
                
    if not launched:
        print("[PRIME] Chrome not found. Falling back to default browser.")
        webbrowser.open(f"file:///{ui_path.resolve()}")

if __name__ == "__main__":
    launch()
