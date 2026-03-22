"""
System Verification Script
Tests all Jarvis components to ensure proper setup
"""

import sys
import importlib
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_python_version():
    """Test Python version"""
    print("\n🔍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 11:
        print("   ✓ Python version OK")
        return True
    else:
        print("   ✗ Python 3.11+ required")
        return False

def test_import(module_name, friendly_name=None):
    """Test if a module can be imported"""
    if friendly_name is None:
        friendly_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"   ✓ {friendly_name}")
        return True
    except ImportError as e:
        print(f"   ✗ {friendly_name}: {e}")
        return False

def test_core_dependencies():
    """Test core Python dependencies"""
    print("\n🔍 Checking core dependencies...")
    
    modules = [
        ("tkinter", "Tkinter (GUI)"),
        ("speech_recognition", "SpeechRecognition"),
        ("pyttsx3", "pyttsx3 (TTS)"),
        ("sklearn", "scikit-learn"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("requests", "Requests"),
        ("psutil", "psutil"),
    ]
    
    results = []
    for module, name in modules:
        results.append(test_import(module, name))
    
    return all(results)

def test_optional_dependencies():
    """Test optional dependencies"""
    print("\n🔍 Checking optional dependencies...")
    
    modules = [
        ("openai", "OpenAI API"),
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("face_recognition", "Face Recognition"),
        ("pyautogui", "PyAutoGUI"),
    ]
    
    for module, name in modules:
        test_import(module, name)
    
    print("\n   ℹ️  Optional modules can be installed later")

def test_project_structure():
    """Test project structure"""
    print("\n🔍 Checking project structure...")
    
    required_paths = [
        "config/settings.py",
        "core/engine.py",
        "core/database.py",
        "core/voice_system.py",
        "core/intent_detector.py",
        "modules/system_actions.py",
        "modules/web_actions.py",
        "modules/information.py",
        "modules/gpt_integration.py",
        "gui/main_window.py",
        "data/os_dataset.csv",
        "main.py",
        "requirements.txt",
    ]
    
    base_dir = Path(__file__).parent
    all_found = True
    
    for path_str in required_paths:
        path = base_dir / path_str
        if path.exists():
            print(f"   ✓ {path_str}")
        else:
            print(f"   ✗ {path_str} NOT FOUND")
            all_found = False
    
    return all_found

def test_configuration():
    """Test configuration"""
    print("\n🔍 Checking configuration...")
    
    try:
        from config.settings import config
        
        print(f"   ✓ Configuration loaded")
        print(f"   • Base directory: {config.BASE_DIR}")
        print(f"   • Dataset path: {config.DATASET_PATH}")
        print(f"   • Database path: {config.DB_PATH}")
        print(f"   • Debug mode: {config.DEBUG_MODE}")
        
        if config.has_openai_key():
            print(f"   • OpenAI API: Configured ✓")
        else:
            print(f"   • OpenAI API: Not configured (optional)")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Configuration error: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\n🔍 Testing database...")
    
    try:
        from core.database import db
        
        # Test connection
        stats = db.get_stats()
        print(f"   ✓ Database initialized")
        print(f"   • Total interactions: {stats['total_interactions']}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        return False

def test_intent_detector():
    """Test intent detector"""
    print("\n🔍 Testing intent detector...")
    
    try:
        from core.intent_detector import intent_detector
        
        # Test detection
        intent, action_type, confidence = intent_detector.detect_intent("open notepad")
        
        print(f"   ✓ Intent detector initialized")
        print(f"   • Loaded intents: {len(intent_detector.commands)}")
        print(f"   • Test command: 'open notepad'")
        print(f"   • Detected: {intent} ({action_type}) - {confidence:.2f}")
        
        return confidence > 0.5
        
    except Exception as e:
        print(f"   ✗ Intent detector error: {e}")
        return False

def test_voice_system():
    """Test voice system initialization"""
    print("\n🔍 Testing voice system...")
    
    try:
        from core.voice_system import voice
        
        print(f"   ✓ Voice system initialized")
        
        # Test TTS
        if voice.tts_engine:
            print(f"   ✓ TTS engine available")
        else:
            print(f"   ✗ TTS engine not available")
        
        # Don't test microphone in automated script
        print(f"   ℹ️  Microphone test skipped (run manually)")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Voice system error: {e}")
        return False

def main():
    """Run all tests"""
    print_header("JARVIS SYSTEM VERIFICATION")
    print("\nThis script will verify that Jarvis is properly set up.")
    
    tests = [
        ("Python Version", test_python_version),
        ("Core Dependencies", test_core_dependencies),
        ("Optional Dependencies", test_optional_dependencies),
        ("Project Structure", test_project_structure),
        ("Configuration", test_configuration),
        ("Database", test_database),
        ("Intent Detector", test_intent_detector),
        ("Voice System", test_voice_system),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n   ✗ {test_name} failed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"   {status}  {test_name}")
    
    if passed == total:
        print("\n🎉 All tests passed! Jarvis is ready to run.")
        print("\nRun 'python main.py' to start Jarvis")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        print("\nMissing dependencies can be installed with:")
        print("   pip install -r requirements.txt")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
