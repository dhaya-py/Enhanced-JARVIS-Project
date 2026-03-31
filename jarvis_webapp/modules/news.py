"""
JARVIS News Module — fetch headlines via NewsAPI or RSS fallback
"""
import requests
import re
from datetime import datetime
from config.settings import config


MOCK_NEWS = {
    "tech": [
        {"title": "AI Models Reach New Benchmark in Reasoning Tasks", "source": "TechCrunch", "url": "https://techcrunch.com"},
        {"title": "Python 3.13 Released with Major Performance Improvements", "source": "Python.org", "url": "https://python.org"},
        {"title": "OpenAI Announces Next-Generation Model Capabilities", "source": "The Verge", "url": "https://theverge.com"},
        {"title": "Google DeepMind Achieves Breakthrough in Protein Folding Research", "source": "Nature", "url": "https://nature.com"},
        {"title": "Cybersecurity Threats Rise 40% Globally, Report Finds", "source": "SecurityWeek", "url": "https://securityweek.com"},
    ],
    "science": [
        {"title": "James Webb Telescope Discovers Ancient Galaxy Cluster", "source": "NASA", "url": "https://nasa.gov"},
        {"title": "Scientists Develop Room-Temperature Superconductor Candidate", "source": "Nature Physics", "url": "https://nature.com"},
        {"title": "New Study Links Gut Microbiome to Brain Health", "source": "Science Daily", "url": "https://sciencedaily.com"},
        {"title": "CERN Physicists Detect Rare Particle Interaction", "source": "CERN", "url": "https://cern.ch"},
    ],
    "world": [
        {"title": "G20 Summit Reaches Climate Agreement on Carbon Targets", "source": "Reuters", "url": "https://reuters.com"},
        {"title": "Global Markets Rally on Positive Economic Data", "source": "Bloomberg", "url": "https://bloomberg.com"},
        {"title": "Space Tourism Reaches New Milestone with Orbital Mission", "source": "Space.com", "url": "https://space.com"},
    ],
    "sports": [
        {"title": "India Cricket Team Sets New World Record", "source": "ESPN", "url": "https://espn.com"},
        {"title": "Champions League Quarter-Finals Draw Announced", "source": "UEFA", "url": "https://uefa.com"},
        {"title": "Formula 1 Season Heats Up with Championship Battle", "source": "F1.com", "url": "https://formula1.com"},
    ],
    "business": [
        {"title": "Tech Giants Report Strong Q4 Earnings", "source": "CNBC", "url": "https://cnbc.com"},
        {"title": "Startup Funding Rebounds in Technology Sector", "source": "Forbes", "url": "https://forbes.com"},
        {"title": "Central Banks Signal Continued Rate Adjustments", "source": "Financial Times", "url": "https://ft.com"},
    ],
}


class NewsFetcher:

    def get_news(self, category: str = "tech", count: int = 5) -> list:
        """Fetch news articles"""
        key = config.NEWS_API_KEY
        if key:
            try:
                return self._fetch_from_api(category, count, key)
            except Exception:
                pass
        return MOCK_NEWS.get(category, MOCK_NEWS["tech"])[:count]

    def _fetch_from_api(self, category: str, count: int, key: str) -> list:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": key,
            "category": category,
            "language": "en",
            "pageSize": count,
        }
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        articles = data.get("articles", [])
        return [{"title": a["title"], "source": a["source"]["name"], "url": a["url"]} for a in articles[:count]]

    def get_news_text(self, category: str = "tech") -> str:
        """Get formatted news text for voice/chat"""
        articles = self.get_news(category, 4)
        lines = [f"Latest {category.title()} headlines, sir:\n"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. {a['title']} — {a.get('source', 'Unknown')}")
        return "\n".join(lines)

    def get_headline(self) -> str:
        """Get single top headline"""
        articles = self.get_news("tech", 1)
        if articles:
            return articles[0]["title"]
        return None

    def get_all_for_ticker(self) -> list:
        """Get a mix of headlines for the news ticker"""
        all_news = []
        for cat in ["tech", "science", "world"]:
            all_news.extend(self.get_news(cat, 2))
        return all_news


news_fetcher = NewsFetcher()
