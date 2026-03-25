"""
Web Actions Module for Jarvis AI Assistant
Handles web-related operations (open URLs, search, etc.)
"""

import webbrowser
from urllib.parse import quote_plus
from typing import Tuple
from config.settings import config

class WebActions:
    """Handles web-related operations"""
    
    def __init__(self):
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'youtube': 'https://www.youtube.com/results?search_query={}',
            'wikipedia': 'https://en.wikipedia.org/wiki/{}',
        }
        
        self.websites = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'gmail': 'https://mail.google.com',
            'instagram': 'https://www.instagram.com',
            'reddit': 'https://www.reddit.com',
            'stackoverflow': 'https://stackoverflow.com',
            'amazon': 'https://www.amazon.com',
            'netflix': 'https://www.netflix.com',
            'chatgpt': 'https://chat.openai.com',
            'whatsapp': 'https://web.whatsapp.com',
            'wikipedia': 'https://en.wikipedia.org',
            'pinterest': 'https://www.pinterest.com',
            'twitch': 'https://www.twitch.tv',
            'spotify': 'https://open.spotify.com',
            'medium': 'https://medium.com',
            'w3schools': 'https://www.w3schools.com',
        }
        
        if config.DEBUG_MODE:
            print("✓ Web Actions initialized")
    
    def open_website(self, site_name: str) -> Tuple[bool, str]:
        """
        Open a website by name
        
        Args:
            site_name: Name of the website (e.g., 'youtube', 'github')
            
        Returns:
            Tuple of (success, message)
        """
        try:
            site_name = site_name.lower()
            
            if site_name in self.websites:
                url = self.websites[site_name]
                webbrowser.open(url)
                return True, f"Opening {site_name}"
            else:
                # Try to construct URL
                url = f"https://www.{site_name}.com"
                webbrowser.open(url)
                return True, f"Opening {site_name}"
                
        except Exception as e:
            return False, f"Error opening website: {e}"
    
    def open_url(self, url: str) -> Tuple[bool, str]:
        """
        Open a specific URL
        
        Args:
            url: Full URL to open
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return True, f"Opening {url}"
            
        except Exception as e:
            return False, f"Error opening URL: {e}"
    
    def google_search(self, query: str) -> Tuple[bool, str]:
        """
        Perform a Google search
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (success, message)
        """
        try:
            encoded_query = quote_plus(query)
            search_url = self.search_engines['google'].format(encoded_query)
            webbrowser.open(search_url)
            return True, f"Searching Google for {query}"
            
        except Exception as e:
            return False, f"Error performing search: {e}"
    
    def youtube_search(self, query: str) -> Tuple[bool, str]:
        """
        Search YouTube
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (success, message)
        """
        try:
            encoded_query = quote_plus(query)
            search_url = self.search_engines['youtube'].format(encoded_query)
            webbrowser.open(search_url)
            return True, f"Searching YouTube for {query}"
            
        except Exception as e:
            return False, f"Error searching YouTube: {e}"
    
    def wikipedia_search(self, query: str) -> Tuple[bool, str]:
        """
        Search Wikipedia
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Replace spaces with underscores for Wikipedia URLs
            formatted_query = query.replace(' ', '_')
            search_url = self.search_engines['wikipedia'].format(formatted_query)
            webbrowser.open(search_url)
            return True, f"Opening Wikipedia for {query}"
            
        except Exception as e:
            return False, f"Error searching Wikipedia: {e}"
    
    def play_youtube_video(self, video_name: str) -> Tuple[bool, str]:
        """
        Play a YouTube video
        
        Args:
            video_name: Name of the video to search and play
            
        Returns:
            Tuple of (success, message)
        """
        return self.youtube_search(video_name)

# Global web actions instance
web_actions = WebActions()
