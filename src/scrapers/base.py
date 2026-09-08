import time
import requests
from typing import Optional, Dict, Any
from config.settings import Config

class BaseScraper:
    def __init__(self, delay: int = Config.DELAY_BETWEEN_REQUESTS):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": Config.USER_AGENT
        })
        self.delay = delay
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure we don't hit rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def fetch(self, url: str, max_retries: int = Config.MAX_RETRIES) -> Optional[requests.Response]:
        """Fetch URL with retries and rate limiting"""
        self._rate_limit()
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait = (attempt + 1) * 2  # exponential backoff
                    time.sleep(wait)
                else:
                    print(f"Failed after {max_retries} attempts")
                    return None
        return None