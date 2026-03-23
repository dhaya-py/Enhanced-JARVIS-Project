"""
Sentiment Analysis Module
Uses TextBlob for sentiment and emotion detection
"""

from textblob import TextBlob

class SentimentAnalyzer:
    """Analyzes sentiment and emotion in text"""

    def analyze(self, text: str) -> str:
        """Analyze sentiment of given text"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity      # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1

            # Determine sentiment label
            if polarity > 0.5:
                sentiment = "Very Positive 😄"
                emoji = "🟢"
            elif polarity > 0.1:
                sentiment = "Positive 🙂"
                emoji = "🟢"
            elif polarity > -0.1:
                sentiment = "Neutral 😐"
                emoji = "🟡"
            elif polarity > -0.5:
                sentiment = "Negative 😞"
                emoji = "🔴"
            else:
                sentiment = "Very Negative 😢"
                emoji = "🔴"

            # Subjectivity
            if subjectivity > 0.6:
                sub_label = "Highly Subjective (opinion-based)"
            elif subjectivity > 0.3:
                sub_label = "Moderately Subjective"
            else:
                sub_label = "Objective (fact-based)"

            return (
                f"{emoji} Sentiment Analysis:\n"
                f"• Text: \"{text[:80]}{'...' if len(text) > 80 else ''}\"\n"
                f"• Sentiment: {sentiment}\n"
                f"• Polarity Score: {polarity:.2f} (range: -1 to 1)\n"
                f"• Subjectivity: {subjectivity:.2f} — {sub_label}\n"
            )
        except Exception as e:
            return f"Error analyzing sentiment: {e}"

    def get_polarity(self, text: str) -> float:
        """Get raw polarity score"""
        try:
            return TextBlob(text).sentiment.polarity
        except:
            return 0.0

sentiment_analyzer = SentimentAnalyzer()
