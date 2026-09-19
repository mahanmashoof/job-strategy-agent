from datetime import datetime
from typing import List, Dict, Any
from src.scrapers.base import BaseScraper
from src.scrapers.boards.base_board import BaseJobBoard

class HimalayasBoard(BaseJobBoard):
    name = "himalayas"
    display_name = "Himalayas"
    
    def __init__(self):
        self.scraper = BaseScraper()
        self.base_url = "https://himalayas.app/jobs/api"
        self.max_per_page = 20  # API hard cap [citation:1]
    
    def fetch_jobs(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Fetch jobs with cursor-based pagination"""
        import time
        
        all_jobs = []
        seen_cursors = set()
        cursor = None
        max_pages = 50  # safety cap
        
        for _ in range(max_pages):
            url = f"{self.base_url}?limit=20"
            if cursor:
                url += f"&cursor={cursor}"
            
            response = self.scraper.fetch(url)
            if not response:
                break
            
            try:
                data = response.json()
            except Exception as e:
                print(f"[{self.name}] JSON error: {e}")
                break
            
            jobs = data.get("jobs", [])
            if not jobs:
                break
            
            # Detect duplicate cursor → stop
            new_cursor = data.get("nextCursor")
            if new_cursor in seen_cursors:
                break
            seen_cursors.add(new_cursor)
            
            all_jobs.extend([self._standardize(j) for j in jobs])
            
            if len(all_jobs) >= limit:
                break
            
            cursor = new_cursor
            if not cursor:
                break
            
            time.sleep(0.5)  # rate-limit safety
        
        return all_jobs[:limit]
    
    def _standardize(self, job: Dict[str, Any]) -> Dict[str, Any]:
        # Build location string from restrictions [citation:3]
        restrictions = job.get("locationRestrictions", [])
        if restrictions:
            location = ", ".join(restrictions) if isinstance(restrictions[0], str) else "Restricted"
        else:
            location = "Worldwide"
        
        return {
            "title": job.get("title", ""),
            "company": job.get("companyName", ""),
            "description": job.get("description", ""),
            "url": job.get("applicationLink", "") or job.get("guid", ""),
            "location": location,
            "location_restrictions": restrictions,  # for geo_filter
            "skills": job.get("categories", []) or job.get("parentCategories", []),
            "source": self.name,
            "posted_date": str(job.get("pubDate", datetime.now().isoformat())),
            "raw": {"minSalary": job.get("minSalary"), "maxSalary": job.get("maxSalary")}
        }