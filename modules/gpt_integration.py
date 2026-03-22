"""
GPT Integration Module for Jarvis AI Assistant
Handles OpenAI GPT API integration with graceful fallback
"""

from typing import Optional
from config.settings import config

class GPTIntegration:
    """Handles GPT API interactions"""
    
    def __init__(self):
        self.client = None
        self.available = False
        
        if config.has_openai_key():
            self._initialize_client()
        
        if config.DEBUG_MODE:
            status = "available" if self.available else "not available (using fallback)"
            print(f"✓ GPT Integration initialized ({status})")
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)
            self.available = True
            
            if config.DEBUG_MODE:
                print("✓ OpenAI client initialized")
                
        except ImportError:
            print("✗ OpenAI library not installed. Install with: pip install openai")
            self.available = False
        except Exception as e:
            print(f"✗ Error initializing OpenAI client: {e}")
            self.available = False
    
    def get_response(self, user_input: str, context: Optional[str] = None) -> str:
        """
        Get response from GPT
        
        Args:
            user_input: User's query
            context: Optional context for the conversation
            
        Returns:
            GPT's response or fallback response
        """
        if not self.available or not self.client:
            return self._fallback_response(user_input)
        
        try:
            # Construct messages
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, an AI personal assistant. "
                        "Provide helpful, concise, and friendly responses. "
                        "Keep responses under 100 words unless asked for more detail."
                    )
                }
            ]
            
            if context:
                messages.append({"role": "system", "content": context})
            
            messages.append({"role": "user", "content": user_input})
            
            # Call GPT API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7,
            )
            
            answer = response.choices[0].message.content.strip()
            
            if config.DEBUG_MODE:
                print(f"✓ GPT response: {answer[:50]}...")
            
            return answer
            
        except Exception as e:
            if config.DEBUG_MODE:
                print(f"✗ GPT API error: {e}")
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> str:
        """
        Provide fallback response when GPT is not available
        
        Args:
            user_input: User's query
            
        Returns:
            Fallback response
        """
        # Simple keyword-based responses
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I assist you today?"
        
        elif any(word in user_input_lower for word in ['how are you', 'how do you do']):
            return "I'm functioning well, thank you! How can I help you?"
        
        elif any(word in user_input_lower for word in ['your name', 'who are you']):
            return "I'm Jarvis, your AI personal assistant. I'm here to help you with various tasks!"
        
        elif any(word in user_input_lower for word in ['what can you', 'help', 'commands']):
            return (
                "I can help you with system tasks, web searches, time and date information, "
                "opening applications, and answering general questions. Try asking me to do something!"
            )
        
        elif any(word in user_input_lower for word in ['thank', 'thanks']):
            return "You're welcome! Happy to help!"
        
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you']):
            return "Goodbye! Have a great day!"
        
        else:
            return (
                "I'm not sure how to respond to that. "
                "Try asking me to open an application, search the web, or tell you the time. "
                "You can also say 'help' to see what I can do."
            )
    
    def is_available(self) -> bool:
        """Check if GPT integration is available"""
        return self.available
    
    def test_connection(self) -> bool:
        """Test GPT API connection"""
        if not self.available:
            return False
        
        try:
            response = self.get_response("Hello")
            return bool(response)
        except:
            return False

# Global GPT integration instance
gpt = GPTIntegration()
