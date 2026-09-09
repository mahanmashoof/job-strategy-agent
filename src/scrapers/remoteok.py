import json
from typing import List, Dict, Any
from datetime import datetime
from src.scrapers.base import BaseScraper

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://remoteok.com/api"
    
    def fetch_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch jobs from RemoteOK API"""
        response = self.fetch(self.base_url)
        if not response:
            return []
        
        try:
            data = response.json()
            # Skip first item (it's just metadata)
            jobs = data[1:] if isinstance(data, list) else []
            
            # Limit results
            jobs = jobs[:limit]
            
            # Standardize format
            standardized = []
            for job in jobs:
                standardized.append({
                    "title": job.get("position", ""),
                    "company": job.get("company", ""),
                    "description": job.get("description", ""),
                    "url": job.get("url", ""),
                    "location": job.get("location", "Remote"),
                    "skills": self._extract_skills(job.get("description", "")),
                    "source": "remoteok",
                    "posted_date": job.get("date", datetime.now().isoformat()),
                    "raw": job  # keep for debugging
                })
            
            return standardized
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return []
    
    def _extract_skills(self, description: str) -> List[str]:
        """Simple skill extraction from description"""
        # We'll improve this in later days
        common_skills = ["python", "javascript", "react", "node", "aws", 
                        "docker", "postgres", "mongodb", "typescript", "go"]
        return [skill for skill in common_skills if skill in description.lower()]