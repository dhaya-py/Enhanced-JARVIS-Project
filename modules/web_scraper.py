"""
Web Scraper Module
Extract text content from web pages
"""

import requests
from bs4 import BeautifulSoup

class WebScraper:
    """Web page scraping and text extraction"""

    def scrape_text(self, url: str) -> str:
        """Scrape text content from a URL"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements
            for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()

            # Extract title
            title = soup.title.string if soup.title else 'No title'

            # Get main text
            text = soup.get_text(separator='\n', strip=True)

            # Clean up
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = '\n'.join(lines[:50])  # Limit to 50 lines

            if len(clean_text) > 2000:
                clean_text = clean_text[:2000] + "..."

            return (
                f"🌐 Scraped: {title}\n"
                f"🔗 URL: {url}\n"
                f"📄 Content ({len(lines)} lines):\n\n"
                f"{clean_text}"
            )

        except requests.exceptions.Timeout:
            return f"❌ Timeout: {url} took too long to respond"
        except requests.exceptions.ConnectionError:
            return f"❌ Cannot connect to {url}"
        except Exception as e:
            return f"❌ Scraping error: {e}"

    def extract_links(self, url: str) -> str:
        """Extract all links from a page"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text(strip=True)[:50]
                if href.startswith(('http://', 'https://')) and text:
                    links.append({'text': text, 'url': href})

            if not links:
                return f"🔗 No links found on {url}"

            text = f"🔗 Links from {url} ({len(links)} found):\n\n"
            for i, link in enumerate(links[:20], 1):
                text += f"  {i}. {link['text']}\n     {link['url']}\n\n"
            return text

        except Exception as e:
            return f"❌ Error extracting links: {e}"

    def extract_headings(self, url: str) -> str:
        """Extract headings from a page"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            headings = []
            for tag in ['h1', 'h2', 'h3']:
                for h in soup.find_all(tag):
                    text = h.get_text(strip=True)
                    if text:
                        headings.append({'level': tag.upper(), 'text': text})

            if not headings:
                return f"📑 No headings found on {url}"

            text = f"📑 Headings from {url}:\n\n"
            for h in headings[:20]:
                text += f"  [{h['level']}] {h['text']}\n"
            return text

        except Exception as e:
            return f"❌ Error extracting headings: {e}"

web_scraper = WebScraper()
