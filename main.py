"""
Jarvis AI Assistant - Main Entry Point
Enhanced AI Command Center with Web Dashboard
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point"""
    try:
        print("=" * 60)
        print("  J.A.R.V.I.S. — AI Command Center")
        print("  Just A Rather Very Intelligent System")
        print("=" * 60)
        print()

        # Check for legacy mode (Tkinter GUI)
        if '--legacy' in sys.argv:
            print("🖥️  Launching Legacy Tkinter GUI...")
            from gui.main_window import main as gui_main
            gui_main()
        else:
            print("🌐 Launching Web Dashboard...")
            print("   Open http://localhost:5000 in your browser")
            print()
            from web.app import run_server
            run_server()

    except KeyboardInterrupt:
        print("\n\n✓ Jarvis shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Critical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
