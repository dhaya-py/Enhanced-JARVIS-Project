"""
Jarvis AI Assistant - Main Entry Point
Production-ready desktop AI assistant
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point"""
    try:
        print("=" * 60)
        print("JARVIS - AI-BASED PERSONAL ASSISTANT SYSTEM")
        print("=" * 60)
        print()
        
        # Import GUI
        from gui.main_window import main as gui_main
        
        # Launch GUI
        gui_main()
        
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
