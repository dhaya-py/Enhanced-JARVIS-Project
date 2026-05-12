"""
JARVIS PRIME - Entry Point
CLI to boot the core daemon or test connectivity.
"""
import sys
import argparse
from core.config import config

def start_daemon():
    """Boot the core FastAPI daemon using Uvicorn."""
    import uvicorn
    print(f"==================================================")
    print(f"  JARVIS PRIME DAEMON ONLINE")
    print(f"  Listening at ws://{config.DAEMON_HOST}:{config.DAEMON_PORT}/ws")
    print(f"==================================================")
    uvicorn.run("core.daemon:app", host=config.DAEMON_HOST, port=config.DAEMON_PORT, log_level="warning")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JARVIS PRIME Control Interface")
    parser.add_argument("mode", choices=["daemon"], help="Run 'daemon' to start the core.")
    args = parser.parse_args()
    
    if args.mode == "daemon":
        start_daemon()
