"""
JARVIS Text Summarizer — extractive summarization
"""
import re


class TextSummarizer:

    def summarize(self, text: str, sentences: int = 3) -> str:
        if not text or len(text) < 50:
            return "Please provide a longer text to summarize, sir."
        try:
            result = self._extractive_summarize(text, sentences)
            word_count = len(text.split())
            return (f"Summary ({word_count} words → {sentences} key sentences), sir:\n\n{result}")
        except Exception as e:
            return f"Summarization error, sir: {e}"

    def _extractive_summarize(self, text: str, n: int) -> str:
        # Split into sentences
        sents = re.split(r'(?<=[.!?])\s+', text.strip())
        sents = [s.strip() for s in sents if len(s.split()) >= 5]
        if len(sents) <= n:
            return text

        # Score by word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        stop = {"the","a","an","is","it","in","on","at","to","for","of","and","or","but",
                "this","that","was","are","be","been","by","as","with","from","have","has"}
        freq = {}
        for w in words:
            if w not in stop and len(w) > 2:
                freq[w] = freq.get(w, 0) + 1

        scores = []
        for s in sents:
            score = sum(freq.get(w, 0) for w in re.findall(r'\b\w+\b', s.lower()) if w not in stop)
            scores.append(score)

        # Pick top n by score, maintain original order
        indexed = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:n]
        top_indices = sorted([i for i, _ in indexed])
        return " ".join(sents[i] for i in top_indices)


text_summarizer = TextSummarizer()
