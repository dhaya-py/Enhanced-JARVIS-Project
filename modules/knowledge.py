"""
Knowledge Base Module
Uses Wikipedia API + DuckDuckGo for knowledge queries
"""

import requests

class KnowledgeBase:
    """Knowledge retrieval from free sources"""

    def search(self, query: str) -> str:
        """Search for knowledge about a topic"""
        # Try Wikipedia first
        result = self._search_wikipedia(query)
        if result:
            return result

        # Try DuckDuckGo
        result = self._search_duckduckgo(query)
        if result:
            return result

        return f"I couldn't find specific information about '{query}'. Try rephrasing your question."

    def _search_wikipedia(self, query: str) -> str:
        """Search Wikipedia API (free, no key)"""
        try:
            # Search for page
            search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(' ', '_')
            response = requests.get(search_url, timeout=5,
                                     headers={'User-Agent': 'JarvisAI/1.0'})

            if response.status_code == 200:
                data = response.json()
                title = data.get('title', query)
                extract = data.get('extract', '')

                if extract:
                    # Truncate if too long
                    if len(extract) > 500:
                        extract = extract[:500] + "..."

                    return (
                        f"📚 {title}\n\n"
                        f"{extract}\n\n"
                        f"🔗 Source: Wikipedia"
                    )

            # Fallback: search API
            search_api = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 1
            }
            response = requests.get(search_api, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = data.get('query', {}).get('search', [])
                if results:
                    title = results[0]['title']
                    # Get the summary of the found page
                    return self._search_wikipedia(title)

        except Exception as e:
            pass
        return None

    def _search_duckduckgo(self, query: str) -> str:
        """Search DuckDuckGo Instant Answers"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {'q': query, 'format': 'json', 'no_html': 1}
            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()

                if data.get('Abstract'):
                    return (
                        f"📖 {data.get('Heading', query)}\n\n"
                        f"{data['Abstract']}\n\n"
                        f"🔗 Source: {data.get('AbstractSource', 'DuckDuckGo')}"
                    )

                if data.get('Answer'):
                    return f"💡 {data['Answer']}"

                if data.get('Definition'):
                    return f"📝 Definition: {data['Definition']}"

                # Check related topics
                topics = data.get('RelatedTopics', [])
                if topics:
                    first = topics[0]
                    if isinstance(first, dict) and first.get('Text'):
                        return f"📖 {first['Text']}"

        except:
            pass
        return None

knowledge_base = KnowledgeBase()
