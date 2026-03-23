"""
News Fetcher Module
Uses free RSS feeds for latest news
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class NewsFetcher:
    """Fetches news from free RSS feeds"""

    def __init__(self):
        self.feeds = {
            'tech': [
                'https://feeds.feedburner.com/TechCrunch/',
                'https://www.wired.com/feed/rss',
            ],
            'world': [
                'http://feeds.bbci.co.uk/news/world/rss.xml',
                'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
            ],
            'science': [
                'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
            ],
            'sports': [
                'http://feeds.bbci.co.uk/sport/rss.xml',
            ],
            'business': [
                'http://feeds.bbci.co.uk/news/business/rss.xml',
            ],
            'general': [
                'http://feeds.bbci.co.uk/news/rss.xml',
            ],
        }

    def get_news(self, category: str = 'general', limit: int = 5) -> list:
        """Get news as list of dicts"""
        feeds = self.feeds.get(category, self.feeds['general'])
        articles = []

        for feed_url in feeds:
            try:
                response = requests.get(feed_url, timeout=10,
                                         headers={'User-Agent': 'JarvisAI/1.0'})
                if response.status_code == 200:
                    root = ET.fromstring(response.content)

                    for item in root.findall('.//item')[:limit]:
                        title = item.findtext('title', '')
                        link = item.findtext('link', '')
                        pub_date = item.findtext('pubDate', '')
                        desc = item.findtext('description', '')

                        if title:
                            articles.append({
                                'title': title,
                                'link': link,
                                'date': pub_date,
                                'description': desc[:200] if desc else '',
                                'source': feed_url.split('/')[2]
                            })

                    if len(articles) >= limit:
                        break
            except:
                continue

        return articles[:limit]

    def get_news_text(self, category: str = 'general') -> str:
        """Get news as formatted text"""
        articles = self.get_news(category, 5)

        if not articles:
            return f"📰 Couldn't fetch {category} news right now. Check your internet connection."

        text = f"📰 Latest {category.title()} News:\n\n"
        for i, article in enumerate(articles, 1):
            text += f"{i}. {article['title']}\n"
            if article.get('description'):
                desc = article['description'][:100]
                text += f"   {desc}...\n"
            text += "\n"

        return text

    def get_headline(self) -> str:
        """Get a single top headline"""
        articles = self.get_news('general', 1)
        if articles:
            return articles[0]['title']
        return ""

news_fetcher = NewsFetcher()
