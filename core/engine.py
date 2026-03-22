"""
Jarvis Engine - Main AI Assistant Engine
Orchestrates all modules and handles the execution flow
"""

import threading
import time
from typing import Callable, Optional
from datetime import datetime

from config.settings import config
from core.database import db
from core.voice_system import voice
from core.intent_detector import intent_detector
from modules.system_actions import system_actions
from modules.web_actions import web_actions
from modules.information import info_provider
from modules.gpt_integration import gpt

class JarvisEngine:
    """Main engine for Jarvis AI Assistant"""
    
    def __init__(self):
        self.is_running = False
        self.engine_thread = None
        self.status_callback = None
        
        if config.DEBUG_MODE:
            print("=" * 50)
            print("JARVIS AI ASSISTANT - ENGINE INITIALIZED")
            print("=" * 50)
    
    def set_status_callback(self, callback: Callable[[str], None]):
        """Set callback function for status updates"""
        self.status_callback = callback
    
    def _update_status(self, message: str):
        """Update status via callback"""
        if self.status_callback:
            self.status_callback(message)
        if config.DEBUG_MODE:
            print(f"📊 Status: {message}")
    
    def start(self):
        """Start the Jarvis engine"""
        if self.is_running:
            self._update_status("Already running")
            return
        
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._run_engine, daemon=True)
        self.engine_thread.start()
        
        self._update_status("Started")
        if config.DEBUG_MODE:
            print("\n🚀 Jarvis Engine STARTED\n")
    
    def stop(self):
        """Stop the Jarvis engine"""
        if not self.is_running:
            self._update_status("Not running")
            return
        
        self.is_running = False
        self._update_status("Stopped")
        
        if config.DEBUG_MODE:
            print("\n🛑 Jarvis Engine STOPPED\n")
    
    def _run_engine(self):
        """Main engine loop - runs in separate thread"""
        try:
            voice.speak("Jarvis activated")
            
            while self.is_running:
                try:
                    # Update status
                    self._update_status("Listening...")
                    
                    # Listen for command
                    command = voice.listen()
                    
                    if not command:
                        continue
                    
                    # Process command
                    self._update_status(f"Processing: {command}")
                    response = self._process_command(command)
                    
                    # Speak response
                    self._update_status(f"Responding...")
                    voice.speak(response)
                    
                    # Log interaction
                    db.log_interaction(command, response)
                    
                    # Small delay
                    time.sleep(0.5)
                    
                except Exception as e:
                    error_msg = f"Error in engine loop: {e}"
                    print(f"✗ {error_msg}")
                    if config.DEBUG_MODE:
                        import traceback
                        traceback.print_exc()
                    
                    # Don't crash - continue running
                    time.sleep(1)
            
        except Exception as e:
            print(f"✗ Critical error in engine: {e}")
            self.is_running = False
            self._update_status("Error - Stopped")
    
    def _process_command(self, command: str) -> str:
        """
        Process user command and generate response
        
        Args:
            command: User's voice command
            
        Returns:
            Response string
        """
        try:
            if config.DEBUG_MODE:
                print(f"\n{'='*50}")
                print(f"COMMAND: {command}")
                print(f"{'='*50}")
            
            # Detect intent
            intent, action_type, confidence = intent_detector.detect_intent(command)
            
            if config.DEBUG_MODE:
                print(f"Intent: {intent}, Type: {action_type}, Confidence: {confidence:.3f}")
            
            # If confidence is low, use GPT
            if not intent or confidence < config.INTENT_THRESHOLD:
                if config.DEBUG_MODE:
                    print("Using GPT for response")
                response = gpt.get_response(command)
                return response
            
            # Process based on action type
            if action_type == "system":
                response = self._handle_system_action(intent, command)
            elif action_type == "web":
                response = self._handle_web_action(intent, command)
            elif action_type == "info":
                response = self._handle_info_action(intent, command)
            elif action_type == "action":
                response = self._handle_action(intent, command)
            elif action_type == "control":
                response = self._handle_control(intent, command)
            else:
                response = gpt.get_response(command)
            
            if config.DEBUG_MODE:
                print(f"RESPONSE: {response}")
                print(f"{'='*50}\n")
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing command: {e}"
            print(f"✗ {error_msg}")
            return "Sorry, I encountered an error processing that request."
    
    def _handle_system_action(self, intent: str, command: str) -> str:
        """Handle system-related actions"""
        try:
            if intent == "open_notepad":
                success, msg = system_actions.open_application("notepad")
                return msg
            
            elif intent == "open_chrome":
                success, msg = system_actions.open_application("chrome")
                return msg
            
            elif intent == "open_calculator":
                success, msg = system_actions.open_application("calculator")
                return msg
            
            elif intent == "open_explorer":
                success, msg = system_actions.open_application("explorer")
                return msg
            
            elif intent == "close_window":
                success, msg = system_actions.close_window()
                return msg
            
            elif intent == "close_chrome":
                success, msg = system_actions.close_application("chrome")
                return msg
            
            elif intent == "close_notepad":
                success, msg = system_actions.close_application("notepad")
                return msg
            
            elif intent == "take_screenshot":
                success, msg = system_actions.take_screenshot()
                return msg
            
            elif intent == "lock_screen":
                success, msg = system_actions.lock_screen()
                return msg
            
            elif intent == "shutdown_system":
                success, msg = system_actions.shutdown_system()
                return msg
            
            elif intent == "restart_system":
                success, msg = system_actions.restart_system()
                return msg
            
            elif intent == "sleep_system":
                success, msg = system_actions.sleep_system()
                return msg
            
            else:
                return f"System action '{intent}' is not yet implemented"
                
        except Exception as e:
            return f"Error executing system action: {e}"
    
    def _handle_web_action(self, intent: str, command: str) -> str:
        """Handle web-related actions"""
        try:
            if intent == "open_youtube":
                success, msg = web_actions.open_website("youtube")
                return msg
            
            elif intent == "open_facebook":
                success, msg = web_actions.open_website("facebook")
                return msg
            
            elif intent == "open_twitter":
                success, msg = web_actions.open_website("twitter")
                return msg
            
            elif intent == "open_linkedin":
                success, msg = web_actions.open_website("linkedin")
                return msg
            
            elif intent == "open_github":
                success, msg = web_actions.open_website("github")
                return msg
            
            elif intent == "google_search":
                # Extract search query from command
                query = command.replace("search", "").replace("google", "").replace("for", "").strip()
                if query:
                    success, msg = web_actions.google_search(query)
                    return msg
                else:
                    return "What would you like me to search for?"
            
            else:
                return f"Web action '{intent}' is not yet implemented"
                
        except Exception as e:
            return f"Error executing web action: {e}"
    
    def _handle_info_action(self, intent: str, command: str) -> str:
        """Handle informational queries"""
        try:
            if intent == "get_time":
                return info_provider.get_time()
            
            elif intent == "get_date":
                return info_provider.get_date()
            
            elif intent == "get_weather":
                # Extract city from command if present
                city = "London"  # Default
                success, msg = info_provider.get_weather(city)
                return msg
            
            elif intent == "about_jarvis":
                return info_provider.get_about_jarvis()
            
            elif intent == "show_help":
                return info_provider.get_help()
            
            elif intent == "acknowledge":
                return info_provider.acknowledge()
            
            else:
                return gpt.get_response(command)
                
        except Exception as e:
            return f"Error getting information: {e}"
    
    def _handle_action(self, intent: str, command: str) -> str:
        """Handle action commands"""
        try:
            if intent == "send_email":
                return "Email functionality is not yet configured. Please set up email credentials in the .env file."
            
            elif intent == "play_music":
                return "Music playback is not yet implemented."
            
            elif intent == "stop_music":
                return "Music control is not yet implemented."
            
            else:
                return gpt.get_response(command)
                
        except Exception as e:
            return f"Error executing action: {e}"
    
    def _handle_control(self, intent: str, command: str) -> str:
        """Handle control commands"""
        if intent == "stop":
            self.stop()
            return "Stopping Jarvis"
        
        elif intent == "exit":
            self.stop()
            return "Goodbye"
        
        else:
            return "Control action not recognized"
    
    def is_active(self) -> bool:
        """Check if engine is running"""
        return self.is_running
    
    def get_status(self) -> str:
        """Get current engine status"""
        return "Running" if self.is_running else "Stopped"

# Global engine instance
engine = JarvisEngine()
