import json
from datetime import datetime
from typing import List, Dict, Any
from src.scrapers.base import BaseScraper
from src.scrapers.boards.base_board import BaseJobBoard

class RemotiveBoard(BaseJobBoard):
    name = "remotive"
    display_name = "Remotive"
    
    def __init__(self):
        self.scraper = BaseScraper()
        self.base_url = "https://remotive.com/api/remote-jobs"
    
    def fetch_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        url = f"{self.base_url}?limit={limit}"
        response = self.scraper.fetch(url)
        if not response:
            return []
        
        try:
            data = response.json()
            jobs = data.get("jobs", [])[:limit]
            return [self._standardize(j) for j in jobs]
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"[{self.name}] parse error: {e}")
            return []
    
    def _standardize(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "description": job.get("description", ""),
            "url": job.get("url", ""),
            "location": job.get("candidate_required_location", "Remote"),
            "skills": job.get("tags", []),  # Remotive gives us tags for free
            "source": self.name,
            "posted_date": job.get("publication_date", datetime.now().isoformat()),
            "raw": job
        }