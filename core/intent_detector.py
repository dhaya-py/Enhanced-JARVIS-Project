"""
Intent Detection Module for Jarvis AI Assistant
Uses scikit-learn for intent classification
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, Optional
from config.settings import config

class IntentDetector:
    """Detects user intent from commands"""
    
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.commands = []
        self.intents = []
        self.action_types = []
        self.command_vectors = None
        self.threshold = config.INTENT_THRESHOLD
        
        self._load_dataset()
        
        if config.DEBUG_MODE:
            print("✓ Intent Detector initialized")
    
    def _load_dataset(self):
        """Load and process the intent dataset"""
        try:
            dataset_path = config.DATASET_PATH
            
            if not dataset_path.exists():
                print(f"✗ Dataset not found at {dataset_path}")
                return
            
            # Load CSV
            df = pd.read_csv(dataset_path)
            
            if df.empty:
                print("✗ Dataset is empty")
                return
            
            # Extract columns
            self.commands = df['command'].tolist()
            self.intents = df['intent'].tolist()
            self.action_types = df['action_type'].tolist()
            
            # Vectorize commands
            self.command_vectors = self.vectorizer.fit_transform(self.commands)
            
            if config.DEBUG_MODE:
                print(f"✓ Loaded {len(self.commands)} intents from dataset")
                
        except Exception as e:
            print(f"✗ Error loading dataset: {e}")
    
    def detect_intent(self, user_input: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Detect intent from user input
        
        Args:
            user_input: User's command text
            
        Returns:
            Tuple of (intent, action_type, confidence)
        """
        if not self.commands or not user_input:
            return None, None, 0.0
        
        try:
            # Vectorize user input
            user_vector = self.vectorizer.transform([user_input.lower()])
            
            # Calculate cosine similarity with all commands
            similarities = cosine_similarity(user_vector, self.command_vectors)[0]
            
            # Get best match
            best_match_idx = np.argmax(similarities)
            confidence = similarities[best_match_idx]
            
            if config.DEBUG_MODE:
                print(f"🔍 Intent detection: confidence={confidence:.3f}")
            
            # Check if confidence meets threshold
            if confidence >= self.threshold:
                intent = self.intents[best_match_idx]
                action_type = self.action_types[best_match_idx]
                
                if config.DEBUG_MODE:
                    print(f"✓ Detected intent: {intent} ({action_type})")
                
                return intent, action_type, confidence
            else:
                if config.DEBUG_MODE:
                    print(f"✗ Confidence below threshold ({confidence:.3f} < {self.threshold})")
                return None, None, confidence
                
        except Exception as e:
            print(f"✗ Error in intent detection: {e}")
            return None, None, 0.0
    
    def get_similar_commands(self, user_input: str, top_k: int = 3) -> list:
        """
        Get top-k similar commands for suggestions
        
        Args:
            user_input: User's command text
            top_k: Number of suggestions to return
            
        Returns:
            List of similar commands
        """
        if not self.commands or not user_input:
            return []
        
        try:
            user_vector = self.vectorizer.transform([user_input.lower()])
            similarities = cosine_similarity(user_vector, self.command_vectors)[0]
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            suggestions = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity
                    suggestions.append({
                        'command': self.commands[idx],
                        'intent': self.intents[idx],
                        'confidence': similarities[idx]
                    })
            
            return suggestions
            
        except Exception as e:
            print(f"✗ Error getting suggestions: {e}")
            return []
    
    def add_custom_intent(self, command: str, intent: str, action_type: str):
        """
        Add a custom intent at runtime
        
        Args:
            command: Command phrase
            intent: Intent label
            action_type: Type of action
        """
        try:
            self.commands.append(command.lower())
            self.intents.append(intent)
            self.action_types.append(action_type)
            
            # Re-vectorize
            self.command_vectors = self.vectorizer.fit_transform(self.commands)
            
            if config.DEBUG_MODE:
                print(f"✓ Added custom intent: {command} -> {intent}")
                
        except Exception as e:
            print(f"✗ Error adding custom intent: {e}")
    
    def get_all_intents(self) -> list:
        """Get list of all available intents"""
        return list(set(zip(self.intents, self.action_types)))

# Global intent detector instance
intent_detector = IntentDetector()
