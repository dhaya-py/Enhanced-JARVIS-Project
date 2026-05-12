"""
JARVIS PRIME - Intent Detector
Standalone natural language intent classifier.
"""
import re
from pathlib import Path
from core.config import config

class IntentDetector:
    def __init__(self):
        self.patterns = []
        self._load_dataset()

    def _load_dataset(self):
        try:
            csv_path = config.DATASET_PATH
            if not csv_path.exists():
                print(f"[PRIME:Engine] Dataset not found: {csv_path}")
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
            print(f"[PRIME:Engine] Core intelligence loaded {len(self.patterns)} vectors.")
        except Exception as e:
            print(f"[PRIME:Engine] Intelligence initialization failed: {e}")

    def process(self, text: str):
        """Returns (intent, action_type, confidence)"""
        if not text or not self.patterns:
            return None, None, 0.0

        lower = text.lower().strip()
        input_tokens = set(re.findall(r'\w+', lower))
        best_match = None
        best_score = 0.0

        for p in self.patterns:
            if p["command"] in lower:
                score = len(p["command"]) / max(len(lower), 1) + 0.5
                if score > best_score:
                    best_score = score
                    best_match = p
            else:
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

intent_detector = IntentDetector()
