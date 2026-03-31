"""
JARVIS System Actions — OS-level control (cross-platform)
"""
import os
import sys
import subprocess
import platform
import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemActions:
    def __init__(self):
        self.os_name = platform.system()  # Windows / Linux / Darwin

    def open_application(self, app_name: str):
        """Open an application by name"""
        app_map = {
            "notepad": {"Windows": "notepad.exe", "Linux": "gedit", "Darwin": "textedit"},
            "chrome": {"Windows": "chrome", "Linux": "google-chrome", "Darwin": "Google Chrome"},
            "calculator": {"Windows": "calc.exe", "Linux": "gnome-calculator", "Darwin": "Calculator"},
            "explorer": {"Windows": "explorer.exe", "Linux": "nautilus", "Darwin": "Finder"},
            "vscode": {"Windows": "code", "Linux": "code", "Darwin": "code"},
            "terminal": {"Windows": "cmd.exe", "Linux": "gnome-terminal", "Darwin": "Terminal"},
            "paint": {"Windows": "mspaint.exe", "Linux": "gimp", "Darwin": "Paintbrush"},
            "word": {"Windows": "winword.exe", "Linux": "libreoffice --writer", "Darwin": "Microsoft Word"},
            "excel": {"Windows": "excel.exe", "Linux": "libreoffice --calc", "Darwin": "Microsoft Excel"},
        }
        app_lower = app_name.lower()
        try:
            if app_lower in app_map:
                cmd = app_map[app_lower].get(self.os_name, app_lower)
            else:
                cmd = app_name

            if self.os_name == "Windows":
                subprocess.Popen(["start", "", cmd], shell=True)
            elif self.os_name == "Darwin":
                subprocess.Popen(["open", "-a", cmd])
            else:
                subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return True, f"Opening {app_name}, sir."
        except Exception as e:
            return False, f"Unable to open {app_name}, sir. Error: {e}"

    def close_application(self, app_name: str):
        """Kill a process by name"""
        try:
            if not PSUTIL_AVAILABLE:
                return False, "psutil not available for process management, sir."
            app_lower = app_name.lower()
            killed = []
            for proc in psutil.process_iter(['name', 'pid']):
                if app_lower in proc.info['name'].lower():
                    proc.kill()
                    killed.append(proc.info['name'])
            if killed:
                return True, f"Closed {', '.join(killed)}, sir."
            return False, f"No running process found for '{app_name}', sir."
        except Exception as e:
            return False, f"Error closing application: {e}"

    def close_window(self):
        """Close the active window"""
        try:
            if self.os_name == "Windows":
                import pyautogui
                pyautogui.hotkey("alt", "f4")
            elif self.os_name == "Linux":
                subprocess.run(["xdotool", "getactivewindow", "windowclose"])
            return True, "Active window closed, sir."
        except Exception as e:
            return False, f"Error closing window: {e}"

    def take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "JARVIS")
            os.makedirs(screenshots_dir, exist_ok=True)
            filepath = os.path.join(screenshots_dir, filename)

            if self.os_name == "Windows":
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
            elif self.os_name == "Darwin":
                subprocess.run(["screencapture", filepath])
            else:
                # Linux — try scrot or gnome-screenshot
                try:
                    subprocess.run(["scrot", filepath], check=True)
                except FileNotFoundError:
                    subprocess.run(["gnome-screenshot", "-f", filepath])

            return True, f"Screenshot saved to {filepath}, sir."
        except Exception as e:
            return False, f"Screenshot failed: {e}"

    def lock_screen(self):
        """Lock the computer screen"""
        try:
            if self.os_name == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            elif self.os_name == "Darwin":
                subprocess.run(["pmset", "displaysleepnow"])
            else:
                subprocess.run(["gnome-screensaver-command", "--lock"])
            return True, "Screen locked, sir."
        except Exception as e:
            return False, f"Lock failed: {e}"

    def set_volume(self, level: int):
        """Set system volume (0–100)"""
        level = max(0, min(100, level))
        try:
            if self.os_name == "Windows":
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level / 100, None)
                return True, f"Volume set to {level}%, sir."
            elif self.os_name == "Linux":
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])
                return True, f"Volume set to {level}%, sir."
            elif self.os_name == "Darwin":
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
                return True, f"Volume set to {level}%, sir."
        except Exception as e:
            return False, f"Volume control unavailable: {e}"

    def shutdown_system(self, delay=60):
        try:
            if self.os_name == "Windows":
                subprocess.run(["shutdown", "/s", "/t", str(delay)])
            else:
                subprocess.run(["shutdown", "-h", f"+{delay//60}"])
            return True, f"System will shut down in {delay} seconds, sir. Say 'cancel shutdown' to abort."
        except Exception as e:
            return False, f"Shutdown failed: {e}"

    def restart_system(self):
        try:
            if self.os_name == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "60"])
            else:
                subprocess.run(["shutdown", "-r", "+1"])
            return True, "System will restart in 60 seconds, sir."
        except Exception as e:
            return False, f"Restart failed: {e}"

    def cancel_shutdown(self):
        try:
            if self.os_name == "Windows":
                subprocess.run(["shutdown", "/a"])
            else:
                subprocess.run(["shutdown", "-c"])
            return True, "Shutdown cancelled, sir."
        except Exception as e:
            return False, f"Cancel failed: {e}"

    def sleep_system(self):
        try:
            if self.os_name == "Windows":
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState 0,1,0"])
            elif self.os_name == "Darwin":
                subprocess.run(["pmset", "sleepnow"])
            else:
                subprocess.run(["systemctl", "suspend"])
            return True, "Putting system to sleep, sir."
        except Exception as e:
            return False, f"Sleep failed: {e}"

    def get_system_info(self) -> dict:
        """Get live system information"""
        info = {
            "os": platform.system(),
            "os_version": platform.version()[:40],
            "machine": platform.machine(),
            "processor": platform.processor()[:40] or "N/A",
            "python": sys.version.split()[0],
        }
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/" if self.os_name != "Windows" else "C:\\")
            info.update({
                "cpu_percent": psutil.cpu_percent(interval=0.5),
                "cpu_count": psutil.cpu_count(),
                "cpu_freq": round(psutil.cpu_freq().current, 1) if psutil.cpu_freq() else 0,
                "memory_total": round(mem.total / (1024**3), 1),
                "memory_used": round(mem.used / (1024**3), 1),
                "memory_percent": mem.percent,
                "disk_total": round(disk.total / (1024**3), 1),
                "disk_used": round(disk.used / (1024**3), 1),
                "disk_percent": disk.percent,
            })
            battery = psutil.sensors_battery()
            if battery:
                info["battery"] = round(battery.percent, 1)
                info["plugged"] = battery.power_plugged
        return info

    def list_processes(self, top_n=10) -> str:
        """List top CPU processes"""
        if not PSUTIL_AVAILABLE:
            return "psutil not available, sir."
        procs = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except Exception:
                pass
        procs.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
        lines = [f"Top {top_n} processes by CPU:"]
        for p in procs[:top_n]:
            lines.append(f"  {p['name'][:25]:<25} CPU: {p['cpu_percent'] or 0:.1f}%  MEM: {p['memory_percent'] or 0:.1f}%")
        return "\n".join(lines)


system_actions = SystemActions()
