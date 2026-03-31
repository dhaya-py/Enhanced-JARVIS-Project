"""
JARVIS File Manager — file search and info
"""
import os
import glob
from pathlib import Path
from datetime import datetime


class FileManager:

    def search_files(self, name: str, search_dir: str = None) -> str:
        """Search for files by name"""
        if not name:
            return "Please specify a file name to search, sir."
        if not search_dir:
            search_dir = str(Path.home())

        try:
            matches = []
            pattern = f"**/*{name}*"
            for path in Path(search_dir).glob(pattern):
                if len(matches) >= 10:
                    break
                try:
                    stat = path.stat()
                    matches.append({
                        "name": path.name,
                        "path": str(path),
                        "size": self._format_size(stat.st_size),
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    })
                except PermissionError:
                    pass

            if not matches:
                return f"No files matching '{name}' found in {search_dir}, sir."

            lines = [f"Found {len(matches)} file(s) matching '{name}', sir:\n"]
            for m in matches:
                lines.append(f"📄 {m['name']}")
                lines.append(f"   📍 {m['path']}")
                lines.append(f"   📏 {m['size']}  🕐 {m['modified']}\n")
            return "\n".join(lines)
        except Exception as e:
            return f"File search error, sir: {e}"

    def get_disk_usage(self, path: str = None) -> str:
        """Get disk usage info"""
        if not path:
            path = str(Path.home())
        try:
            usage = os.statvfs(path) if os.name != 'nt' else None
            if usage:
                total = usage.f_blocks * usage.f_frsize
                free = usage.f_bfree * usage.f_frsize
                used = total - free
                pct = (used / total) * 100
                return (f"Disk usage for {path}, sir:\n"
                        f"Total: {self._format_size(total)}\n"
                        f"Used: {self._format_size(used)} ({pct:.1f}%)\n"
                        f"Free: {self._format_size(free)}")
            import shutil
            total, used, free = shutil.disk_usage(path)
            pct = (used / total) * 100
            return (f"Disk usage, sir:\n"
                    f"Total: {self._format_size(total)}\n"
                    f"Used: {self._format_size(used)} ({pct:.1f}%)\n"
                    f"Free: {self._format_size(free)}")
        except Exception as e:
            return f"Could not retrieve disk info, sir: {e}"

    def list_directory(self, path: str = None) -> str:
        """List directory contents"""
        if not path:
            path = str(Path.home())
        try:
            items = list(Path(path).iterdir())[:20]
            dirs = [i for i in items if i.is_dir()]
            files = [i for i in items if i.is_file()]
            lines = [f"Directory: {path}\n",
                     f"📁 {len(dirs)} folder(s), 📄 {len(files)} file(s)\n"]
            for d in dirs[:5]:
                lines.append(f"📁 {d.name}/")
            for f in files[:10]:
                try:
                    size = self._format_size(f.stat().st_size)
                    lines.append(f"📄 {f.name} ({size})")
                except Exception:
                    lines.append(f"📄 {f.name}")
            if len(items) > 15:
                lines.append(f"...and more items.")
            return "\n".join(lines)
        except PermissionError:
            return f"Access denied to {path}, sir."
        except Exception as e:
            return f"Error listing directory, sir: {e}"

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"


file_manager = FileManager()
