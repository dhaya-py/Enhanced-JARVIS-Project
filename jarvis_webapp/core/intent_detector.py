"""
JARVIS Intent Detector — CSV-based cosine similarity matching
"""
import re
from pathlib import Path
from config.settings import config


class IntentDetector:
    def __init__(self):
        self.patterns = []
        self._load_dataset()

    def _load_dataset(self):
        try:
            csv_path = config.DATASET_PATH
            if not csv_path.exists():
                print(f"[IntentDetector] Dataset not found: {csv_path}")
                return
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[1:]  # skip header
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    cmd, intent, action_type = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    self.patterns.append({
                        "command": cmd.lower(),
                        "intent": intent,
                        "action_type": action_type,
                        "tokens": set(re.findall(r'\w+', cmd.lower()))
                    })
            print(f"[IntentDetector] Loaded {len(self.patterns)} patterns")
        except Exception as e:
            print(f"[IntentDetector] Error: {e}")

    def detect_intent(self, user_input: str):
        """Returns (intent, action_type, confidence)"""
        if not user_input or not self.patterns:
            return None, None, 0.0

        lower = user_input.lower().strip()
        input_tokens = set(re.findall(r'\w+', lower))
        best_match = None
        best_score = 0.0

        for p in self.patterns:
            # Exact substring match → high confidence
            if p["command"] in lower:
                score = len(p["command"]) / max(len(lower), 1) + 0.5
                if score > best_score:
                    best_score = score
                    best_match = p
            else:
                # Jaccard similarity
                if not p["tokens"] or not input_tokens:
                    continue
                inter = len(p["tokens"] & input_tokens)
                union = len(p["tokens"] | input_tokens)
                score = inter / union if union > 0 else 0
                if score > best_score:
                    best_score = score
                    best_match = p

        if best_match and best_score >= config.INTENT_THRESHOLD:
            return best_match["intent"], best_match["action_type"], best_score

        return None, None, best_score

    def add_intent(self, command: str, intent: str, action_type: str):
        self.patterns.append({
            "command": command.lower(),
            "intent": intent,
            "action_type": action_type,
            "tokens": set(re.findall(r'\w+', command.lower()))
        })


intent_detector = IntentDetector()
