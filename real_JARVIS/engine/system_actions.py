"""
JARVIS PRIME - System Actions
OS-level execution logic for the intelligence engine.
"""
import os
import subprocess
import time

class SystemActions:
    def open_application(self, app_name: str):
        """Attempts to open an application by name."""
        try:
            if os.name == 'nt':
                subprocess.Popen(f'start {app_name}', shell=True)
            else:
                subprocess.Popen(['open', '-a', app_name])
            return True, f"Initiated execution sequence for {app_name}."
        except Exception as e:
            return False, f"Failed to open {app_name}: {e}"

    def system_status(self):
        """Returns a high-level system status."""
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            return f"System operational. CPU at {cpu}%, Memory at {mem.percent}%."
        except ImportError:
            return "System operational. Extended metrics unavailable (psutil missing)."

system_actions = SystemActions()
