from datetime import datetime
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from src.scrapers.base import BaseScraper
from src.scrapers.boards.base_board import BaseJobBoard

class WWRBoard(BaseJobBoard):
    name = "wwr"
    display_name = "We Work Remotely"
    
    def __init__(self):
        self.scraper = BaseScraper()
        self.feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    
    def fetch_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        response = self.scraper.fetch(self.feed_url)
        if not response:
            return []
        
        try:
            root = ET.fromstring(response.content)
            items = root.findall(".//item")[:limit]
            return [self._standardize(item) for item in items]
        except ET.ParseError as e:
            print(f"[{self.name}] XML error: {e}")
            return []
    
    def _standardize(self, item: ET.Element) -> Dict[str, Any]:
        def text(tag: str) -> str:
            el = item.find(tag)
            return el.text if el is not None and el.text else ""
        
        # WWR puts company name in the <title> as "Company: Job Title"
        raw_title = text("title")
        if ": " in raw_title:
            company, title = raw_title.split(": ", 1)
        else:
            company, title = "Unknown", raw_title
        
        # Region is often in <region> tag
        region = text("region") or "Remote"
        
        return {
            "title": title.strip(),
            "company": company.strip(),
            "description": text("description"),
            "url": text("link"),
            "location": region,
            "skills": [],  # RSS doesn't have tags; cleaner will extract
            "source": self.name,
            "posted_date": text("pubDate") or datetime.now().isoformat(),
            "raw": {"title": raw_title}
        }