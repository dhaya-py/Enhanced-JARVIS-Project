"""
File Manager Module
Search, organize, and manage files
"""

import os
from pathlib import Path
from datetime import datetime

class FileManager:
    """File search and management"""

    def search_files(self, query: str, search_path: str = None) -> str:
        """Search for files by name"""
        try:
            if not search_path:
                search_path = str(Path.home())

            results = []
            query_lower = query.lower()

            # Search common directories
            search_dirs = [
                os.path.join(search_path, 'Desktop'),
                os.path.join(search_path, 'Documents'),
                os.path.join(search_path, 'Downloads'),
            ]

            for search_dir in search_dirs:
                if not os.path.exists(search_dir):
                    continue
                try:
                    for root, dirs, files in os.walk(search_dir):
                        # Limit depth to avoid long searches
                        depth = root.replace(search_dir, '').count(os.sep)
                        if depth > 3:
                            continue

                        for file in files:
                            if query_lower in file.lower():
                                filepath = os.path.join(root, file)
                                try:
                                    size = os.path.getsize(filepath)
                                    results.append({
                                        'name': file,
                                        'path': filepath,
                                        'size': self._format_size(size)
                                    })
                                except:
                                    pass

                            if len(results) >= 10:
                                break
                        if len(results) >= 10:
                            break
                except PermissionError:
                    continue

            if not results:
                return f"📁 No files found matching '{query}' in Desktop, Documents, and Downloads."

            text = f"📁 Found {len(results)} file(s) matching '{query}':\n\n"
            for f in results:
                text += f"  📄 {f['name']} ({f['size']})\n     {f['path']}\n\n"
            return text

        except Exception as e:
            return f"📁 Error searching files: {e}"

    def _format_size(self, size_bytes: int) -> str:
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def get_disk_usage(self) -> str:
        """Get disk usage info"""
        try:
            import psutil
            partitions = psutil.disk_partitions()
            text = "💾 Disk Usage:\n\n"
            for p in partitions:
                try:
                    usage = psutil.disk_usage(p.mountpoint)
                    text += (
                        f"  Drive {p.device}\n"
                        f"  Total: {self._format_size(usage.total)} | "
                        f"Used: {self._format_size(usage.used)} ({usage.percent}%) | "
                        f"Free: {self._format_size(usage.free)}\n\n"
                    )
                except:
                    continue
            return text
        except:
            return "Unable to get disk info"

file_manager = FileManager()
