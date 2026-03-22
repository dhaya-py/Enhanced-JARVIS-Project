"""
Voice System for Jarvis AI Assistant
Handles speech recognition (input) and text-to-speech (output)
"""

import speech_recognition as sr
import pyttsx3
from typing import Optional
from config.settings import config

class VoiceSystem:
    """Manages voice input and output"""
    
    def __init__(self):
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize TTS engine (single instance)
        self.tts_engine = None
        self._initialize_tts()
        
        # Voice settings
        self.timeout = config.VOICE_TIMEOUT
        self.phrase_limit = config.VOICE_PHRASE_LIMIT
        
        if config.DEBUG_MODE:
            print("✓ Voice System initialized")
    
    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice properties
            self.tts_engine.setProperty('rate', config.TTS_RATE)
            
            # Try to set a voice (prefer female voice if available)
            voices = self.tts_engine.getProperty('voices')
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)  # Usually female
            
            if config.DEBUG_MODE:
                print("✓ TTS Engine initialized")
        except Exception as e:
            print(f"✗ TTS initialization error: {e}")
            self.tts_engine = None
    
    def listen(self) -> Optional[str]:
        """
        Listen to microphone and convert speech to text
        
        Returns:
            Recognized text or None if failed
        """
        try:
            with sr.Microphone() as source:
                if config.DEBUG_MODE:
                    print("🎤 Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_limit
                )
                
                if config.DEBUG_MODE:
                    print("🔄 Processing...")
                
                # Recognize speech using Google
                text = self.recognizer.recognize_google(audio)
                
                if config.DEBUG_MODE:
                    print(f"✓ Recognized: {text}")
                
                return text.lower()
                
        except sr.WaitTimeoutError:
            if config.DEBUG_MODE:
                print("✗ Listening timeout")
            return None
        except sr.UnknownValueError:
            if config.DEBUG_MODE:
                print("✗ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"✗ Recognition service error: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error in listen(): {e}")
            return None
    
    def speak(self, text: str) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
        
        try:
            if config.DEBUG_MODE:
                print(f"🔊 Speaking: {text}")
            
            if self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            else:
                print("✗ TTS engine not available")
                return False
                
        except Exception as e:
            print(f"✗ Error in speak(): {e}")
            # Try to reinitialize TTS engine
            self._initialize_tts()
            return False
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is accessible
        
        Returns:
            True if microphone works, False otherwise
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                return True
        except Exception as e:
            print(f"✗ Microphone test failed: {e}")
            return False
    
    def test_speakers(self) -> bool:
        """
        Test if speakers work
        
        Returns:
            True if speakers work, False otherwise
        """
        return self.speak("Testing audio output")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.tts_engine:
                self.tts_engine.stop()
        except:
            pass

# Global voice system instance
voice = VoiceSystem()
