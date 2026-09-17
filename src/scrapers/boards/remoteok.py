import json
from datetime import datetime
from typing import List, Dict, Any
from src.scrapers.base import BaseScraper
from src.scrapers.boards.base_board import BaseJobBoard

class RemoteOKBoard(BaseJobBoard):
    name = "remoteok"
    display_name = "RemoteOK"
    
    def __init__(self):
        self.scraper = BaseScraper()
        self.base_url = "https://remoteok.com/api"
    
    def fetch_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        response = self.scraper.fetch(self.base_url)
        if not response:
            return []
        
        try:
            data = response.json()
            jobs = data[1:] if isinstance(data, list) else []
            jobs = jobs[:limit]
            
            return [self._standardize(j) for j in jobs]
        except json.JSONDecodeError as e:
            print(f"[{self.name}] JSON error: {e}")
            return []
    
    def _standardize(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": job.get("position", ""),
            "company": job.get("company", ""),
            "description": job.get("description", ""),
            "url": job.get("url", ""),
            "location": job.get("location", "Remote"),
            "skills": [],  # will be filled by cleaner
            "source": self.name,
            "posted_date": job.get("date", datetime.now().isoformat()),
            "raw": job
        }