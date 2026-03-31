"""
JARVIS Web Actions — open websites, search, web navigation
"""
import webbrowser
import urllib.parse

SITE_MAP = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://linkedin.com",
    "instagram": "https://instagram.com",
    "reddit": "https://reddit.com",
    "netflix": "https://netflix.com",
    "amazon": "https://amazon.in",
    "flipkart": "https://flipkart.com",
    "stackoverflow": "https://stackoverflow.com",
    "wikipedia": "https://wikipedia.org",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "translate": "https://translate.google.com",
    "drive": "https://drive.google.com",
    "docs": "https://docs.google.com",
    "sheets": "https://sheets.google.com",
    "meet": "https://meet.google.com",
    "zoom": "https://zoom.us",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "chatgpt": "https://chat.openai.com",
    "claude": "https://claude.ai",
    "anthropic": "https://anthropic.com",
}


class WebActions:
    SITE_MAP = SITE_MAP

    def open_website(self, site_name: str):
        """Open a website by name or URL"""
        site_lower = site_name.lower().strip()
        url = SITE_MAP.get(site_lower)
        if not url:
            # Try as direct URL
            if site_lower.startswith("http"):
                url = site_lower
            else:
                url = f"https://{site_lower}.com"
        # Return URL for frontend to open (webbrowser won't work in server context)
        return True, f"Opening {site_name} for you, sir.", url

    def google_search(self, query: str):
        """Perform a Google search"""
        if not query:
            return False, "What would you like me to search for, sir?", None
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        return True, f"Searching Google for '{query}', sir.", url

    def youtube_search(self, query: str):
        """Search YouTube"""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        return True, f"Searching YouTube for '{query}', sir.", url

    def wikipedia_search(self, query: str):
        encoded = urllib.parse.quote_plus(query)
        url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded}"
        return True, f"Opening Wikipedia search for '{query}', sir.", url

    def get_site_url(self, site_name: str) -> str:
        return SITE_MAP.get(site_name.lower(), f"https://{site_name}.com")


web_actions = WebActions()
