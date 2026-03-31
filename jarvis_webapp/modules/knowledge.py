"""
JARVIS Knowledge Base — Wikipedia API lookups
"""
import requests
import re


class KnowledgeBase:

    def search(self, query: str) -> str:
        """Look up a topic on Wikipedia"""
        if not query or len(query) < 2:
            return "Please provide a topic to look up, sir."
        try:
            # Wikipedia REST API
            q = query.strip()
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(q)}"
            r = requests.get(url, headers={"User-Agent": "JARVIS/3.0 (educational project)"}, timeout=8)
            if r.status_code == 200:
                data = r.json()
                title = data.get("title", q)
                extract = data.get("extract", "")
                if extract:
                    # Limit to 3 sentences
                    sentences = re.split(r'(?<=[.!?])\s+', extract)
                    summary = " ".join(sentences[:3])
                    return f"Regarding '{title}', sir:\n\n{summary}"
                return f"I found an article on '{title}' but it had no summary, sir."
            elif r.status_code == 404:
                # Try search endpoint
                return self._search_fallback(query)
            return f"Wikipedia returned status {r.status_code}, sir. Try rephrasing your query."
        except requests.Timeout:
            return "Knowledge retrieval timed out, sir. Please check your connection."
        except Exception as e:
            return self._offline_knowledge(query)

    def _search_fallback(self, query: str) -> str:
        """Use Wikipedia search API"""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 1,
            }
            r = requests.get(url, params=params, timeout=8)
            data = r.json()
            results = data.get("query", {}).get("search", [])
            if results:
                title = results[0]["title"]
                snippet = re.sub(r'<[^>]+>', '', results[0].get("snippet", ""))
                return f"On '{title}', sir: {snippet}... (For full details, check Wikipedia.)"
            return f"I couldn't find information about '{query}' on Wikipedia, sir."
        except Exception:
            return self._offline_knowledge(query)

    def _offline_knowledge(self, query: str) -> str:
        """Offline fallback facts"""
        facts = {
            "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991, known for its clear syntax and versatility in web, AI, and data science.",
            "ai": "Artificial Intelligence (AI) is the simulation of human intelligence in machines, encompassing machine learning, natural language processing, computer vision, and robotics.",
            "machine learning": "Machine Learning is a subset of AI where algorithms learn from data to make predictions or decisions without being explicitly programmed.",
            "deep learning": "Deep Learning is a subset of machine learning using neural networks with many layers to learn complex patterns in large datasets.",
            "jarvis": "J.A.R.V.I.S. — Just A Rather Very Intelligent System — is Tony Stark's AI assistant from the Marvel universe, and the inspiration for this project.",
            "flask": "Flask is a lightweight Python web framework that provides the tools needed to build web applications quickly and with minimal code.",
        }
        low = query.lower()
        for key, fact in facts.items():
            if key in low:
                return f"Regarding '{query}', sir:\n\n{fact}"
        return (f"I'm unable to fetch information about '{query}' right now, sir. "
                f"Network connection may be unavailable. Try again when connected.")


knowledge_base = KnowledgeBase()
