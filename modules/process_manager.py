"""
Process Manager Module
List, search, and kill system processes
"""

import psutil
from datetime import datetime

class ProcessManager:
    """System process management"""

    def list_processes(self, limit: int = 15) -> str:
        """List top processes sorted by memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    info = proc.info
                    if info['memory_percent'] and info['memory_percent'] > 0.1:
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by memory usage
            processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
            top = processes[:limit]

            text = f"⚙️ Top {len(top)} Processes (by memory):\n\n"
            text += f"  {'PID':<8} {'Name':<25} {'RAM %':<8} {'CPU %':<8}\n"
            text += f"  {'─'*8} {'─'*25} {'─'*8} {'─'*8}\n"

            for p in top:
                name = (p['name'] or 'Unknown')[:24]
                mem = p.get('memory_percent', 0)
                cpu = p.get('cpu_percent', 0)
                text += f"  {p['pid']:<8} {name:<25} {mem:<8.1f} {cpu:<8.1f}\n"

            total_procs = len(list(psutil.process_iter()))
            text += f"\n📊 Total running processes: {total_procs}"
            return text

        except Exception as e:
            return f"❌ Error listing processes: {e}"

    def search_process(self, name: str) -> str:
        """Search for a process by name"""
        try:
            found = []
            name_lower = name.lower()
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent', 'status']):
                try:
                    if name_lower in (proc.info['name'] or '').lower():
                        found.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if not found:
                return f"⚙️ No process found matching '{name}'"

            text = f"⚙️ Found {len(found)} process(es) matching '{name}':\n\n"
            for p in found:
                text += f"  PID: {p['pid']} | {p['name']} | RAM: {p.get('memory_percent', 0):.1f}% | Status: {p.get('status', 'unknown')}\n"
            return text

        except Exception as e:
            return f"❌ Error searching: {e}"

    def kill_process(self, identifier: str) -> str:
        """Kill a process by name or PID"""
        try:
            # Try PID first
            try:
                pid = int(identifier)
                proc = psutil.Process(pid)
                proc_name = proc.name()
                proc.terminate()
                return f"⚙️ Terminated process: {proc_name} (PID: {pid})"
            except ValueError:
                pass

            # Kill by name
            killed = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if identifier.lower() in (proc.info['name'] or '').lower():
                        proc.terminate()
                        killed += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if killed > 0:
                return f"⚙️ Terminated {killed} process(es) matching '{identifier}'"
            return f"⚙️ No process found matching '{identifier}'"

        except Exception as e:
            return f"❌ Error killing process: {e}"

    def get_summary(self) -> dict:
        """Get process summary for dashboard"""
        try:
            total = len(list(psutil.process_iter()))
            return {
                'total': total,
                'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory().percent
            }
        except:
            return {'total': 0, 'cpu': 0, 'memory': 0}

process_manager = ProcessManager()
