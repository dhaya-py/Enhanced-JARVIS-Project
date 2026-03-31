"""
JARVIS Sentiment Analyzer — rule-based + TextBlob
"""
import re


POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "happy",
    "joy", "awesome", "brilliant", "perfect", "beautiful", "best", "outstanding",
    "superb", "terrific", "delightful", "pleased", "glad", "excited", "positive",
    "nice", "lovely", "magnificent", "splendid", "stellar", "impressive", "remarkable"
}
NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "hate", "sad", "angry", "disappointed",
    "worst", "disgusting", "annoying", "frustrating", "upset", "unhappy", "negative",
    "poor", "dreadful", "pathetic", "useless", "failure", "broken", "wrong", "error"
}
INTENSIFIERS = {"very", "extremely", "really", "absolutely", "incredibly", "quite", "rather"}
NEGATORS = {"not", "never", "no", "don't", "doesn't", "can't", "won't", "isn't", "aren't"}


class SentimentAnalyzer:

    def analyze(self, text: str) -> str:
        """Analyze sentiment of the given text"""
        if not text:
            return "Please provide text to analyze, sir."
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity      # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1

            return self._format_result(text, polarity, subjectivity)
        except ImportError:
            return self._rule_based(text)

    def _format_result(self, text: str, polarity: float, subjectivity: float) -> str:
        if polarity > 0.5:
            label = "Very Positive 😊"
        elif polarity > 0.1:
            label = "Positive 🙂"
        elif polarity > -0.1:
            label = "Neutral 😐"
        elif polarity > -0.5:
            label = "Negative 😕"
        else:
            label = "Very Negative 😞"

        subj_label = "Highly Subjective" if subjectivity > 0.7 else "Somewhat Subjective" if subjectivity > 0.4 else "Mostly Objective"

        return (f"Sentiment Analysis Results, sir:\n\n"
                f"📝 Text: '{text[:80]}{'...' if len(text)>80 else ''}'\n"
                f"🎭 Sentiment: {label}\n"
                f"📊 Polarity Score: {polarity:+.3f} (range: -1.0 to +1.0)\n"
                f"🔍 Subjectivity: {subjectivity:.3f} ({subj_label})\n\n"
                f"{'This text expresses a positive tone.' if polarity > 0 else 'This text has a negative tone.' if polarity < 0 else 'This text is neutral in tone.'}")

    def _rule_based(self, text: str) -> str:
        words = re.findall(r'\w+', text.lower())
        score = 0
        i = 0
        while i < len(words):
            word = words[i]
            negate = (i > 0 and words[i-1] in NEGATORS)
            multiplier = 1.5 if (i > 0 and words[i-1] in INTENSIFIERS) else 1.0
            if word in POSITIVE_WORDS:
                score += (-1 if negate else 1) * multiplier
            elif word in NEGATIVE_WORDS:
                score += (1 if negate else -1) * multiplier
            i += 1

        if score > 1:
            label = "Positive 🙂"
        elif score > 0:
            label = "Mildly Positive 😊"
        elif score == 0:
            label = "Neutral 😐"
        elif score > -1:
            label = "Mildly Negative 😕"
        else:
            label = "Negative 😞"

        return (f"Sentiment Analysis (rule-based), sir:\n\n"
                f"📝 Text: '{text[:80]}'\n"
                f"🎭 Sentiment: {label}\n"
                f"📊 Score: {score:+.1f}\n\n"
                f"Install TextBlob for enhanced accuracy: pip install textblob")


sentiment_analyzer = SentimentAnalyzer()
