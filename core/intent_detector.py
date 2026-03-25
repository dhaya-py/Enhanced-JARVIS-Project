"""
Intent Detection Module for Jarvis AI Assistant
Uses scikit-learn for intent classification + fuzzy matching fallback
"""

import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, Optional
from config.settings import config

class IntentDetector:
    """Detects user intent from commands using cosine similarity + fuzzy matching"""
    
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.commands = []
        self.intents = []
        self.action_types = []
        self.command_vectors = None
        self.threshold = config.INTENT_THRESHOLD
        
        self._load_dataset()
        
        if config.DEBUG_MODE:
            print("✓ Intent Detector initialized (with fuzzy matching)")
    
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
    
    def _fuzzy_match(self, user_input: str) -> Tuple[int, float]:
        """
        Fuzzy string matching fallback using SequenceMatcher.
        Returns (best_index, fuzzy_score).
        """
        user_lower = user_input.lower().strip()
        best_score = 0.0
        best_idx = 0
        
        for i, cmd in enumerate(self.commands):
            score = SequenceMatcher(None, user_lower, cmd.lower()).ratio()
            if score > best_score:
                best_score = score
                best_idx = i
        
        return best_idx, best_score

    def detect_intent(self, user_input: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Detect intent from user input using cosine similarity + fuzzy fallback.
        
        Args:
            user_input: User's command text
            
        Returns:
            Tuple of (intent, action_type, confidence)
        """
        if not self.commands or not user_input:
            return None, None, 0.0
        
        try:
            # ── Stage 1: Cosine similarity ──────────────────────
            user_vector = self.vectorizer.transform([user_input.lower()])
            similarities = cosine_similarity(user_vector, self.command_vectors)[0]
            
            cosine_idx = int(np.argmax(similarities))
            cosine_score = float(similarities[cosine_idx])
            
            # ── Stage 2: Fuzzy matching fallback ────────────────
            fuzzy_idx, fuzzy_score = self._fuzzy_match(user_input)
            # Weight fuzzy slightly lower so cosine is preferred when both are close
            weighted_fuzzy = fuzzy_score * 0.85
            
            # Pick the better match
            if cosine_score >= weighted_fuzzy:
                best_idx = cosine_idx
                confidence = cosine_score
                method = "cosine"
            else:
                best_idx = fuzzy_idx
                confidence = weighted_fuzzy
                method = "fuzzy"
            
            if config.DEBUG_MODE:
                print(f"🔍 Intent: cosine={cosine_score:.3f}, fuzzy={fuzzy_score:.3f} (weighted={weighted_fuzzy:.3f}), using={method}")
            
            # Check if confidence meets threshold
            if confidence >= self.threshold:
                intent = self.intents[best_idx]
                action_type = self.action_types[best_idx]
                
                if config.DEBUG_MODE:
                    print(f"✓ Detected intent: {intent} ({action_type}) via {method}")
                
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
        Get top-k similar commands for suggestions (combines cosine + fuzzy).
        """
        if not self.commands or not user_input:
            return []
        
        try:
            user_lower = user_input.lower()
            user_vector = self.vectorizer.transform([user_lower])
            cosine_sims = cosine_similarity(user_vector, self.command_vectors)[0]
            
            # Combine cosine and fuzzy scores
            combined_scores = []
            for i, cmd in enumerate(self.commands):
                fuzzy = SequenceMatcher(None, user_lower, cmd.lower()).ratio()
                combined = max(float(cosine_sims[i]), fuzzy * 0.85)
                combined_scores.append(combined)
            
            # Get top-k indices
            top_indices = np.argsort(combined_scores)[-top_k:][::-1]
            
            suggestions = []
            seen_intents = set()
            for idx in top_indices:
                if combined_scores[idx] > 0.15 and self.intents[idx] not in seen_intents:
                    suggestions.append({
                        'command': self.commands[idx],
                        'intent': self.intents[idx],
                        'confidence': combined_scores[idx]
                    })
                    seen_intents.add(self.intents[idx])
            
            return suggestions
            
        except Exception as e:
            print(f"✗ Error getting suggestions: {e}")
            return []
    
    def get_fuzzy_suggestions(self, user_input: str, top_k: int = 3) -> str:
        """
        Get 'Did you mean...?' style suggestions for unrecognized commands.
        Returns a formatted string or empty string if no good matches.
        """
        suggestions = self.get_similar_commands(user_input, top_k)
        if not suggestions:
            return ""
        
        # Only show if best suggestion has reasonable confidence
        if suggestions[0]['confidence'] < 0.25:
            return ""
        
        lines = ["🤔 I'm not sure what you mean. Did you mean:"]
        for i, s in enumerate(suggestions, 1):
            lines.append(f"  {i}. \"{s['command']}\"")
        lines.append("\nTry rephrasing or type 'help' for available commands.")
        return "\n".join(lines)
    
    def add_custom_intent(self, command: str, intent: str, action_type: str):
        """Add a custom intent at runtime"""
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
