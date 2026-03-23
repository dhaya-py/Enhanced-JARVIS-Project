"""
Text Summarizer Module
Extractive summarization using TF-IDF sentence ranking
"""

import re
import math
from collections import Counter

class TextSummarizer:
    """Summarizes text using extractive TF-IDF approach"""

    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """Summarize text into key sentences"""
        try:
            # Clean text
            text = text.strip()
            if len(text) < 100:
                return f"📝 Text is too short to summarize. Here it is:\n{text}"

            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            if len(sentences) <= num_sentences:
                return f"📝 Summary:\n{text}"

            # Calculate TF-IDF scores
            word_freq = Counter()
            for sentence in sentences:
                words = re.findall(r'\w+', sentence.lower())
                word_freq.update(words)

            # Score each sentence
            sentence_scores = []
            for i, sentence in enumerate(sentences):
                words = re.findall(r'\w+', sentence.lower())
                if not words:
                    sentence_scores.append(0)
                    continue

                score = sum(word_freq[w] for w in words) / len(words)

                # Boost first sentences (usually more important)
                if i < 2:
                    score *= 1.5

                sentence_scores.append(score)

            # Get top sentences (maintain original order)
            top_indices = sorted(
                sorted(range(len(sentence_scores)), key=lambda i: sentence_scores[i], reverse=True)[:num_sentences]
            )

            summary_sentences = [sentences[i] for i in top_indices]
            summary = ' '.join(summary_sentences)

            return (
                f"📝 Summary ({len(summary_sentences)} key sentences from {len(sentences)} total):\n\n"
                f"{summary}\n\n"
                f"📊 Compression: {len(summary)}/{len(text)} characters ({round(len(summary)/len(text)*100)}%)"
            )

        except Exception as e:
            return f"Error summarizing text: {e}"

text_summarizer = TextSummarizer()
