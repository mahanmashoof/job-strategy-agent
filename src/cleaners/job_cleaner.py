import re
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

class JobCleaner:
    def __init__(self):
        self.known_skills = self._load_skills()
    
    def _load_skills(self) -> set:
        from src.parsers.skills_db import SKILLS
        return set(SKILLS.keys())
    
    def clean(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and validate job data"""
        cleaned = []
        seen_urls = set()
        
        for job in jobs:
            # Skip if missing critical fields
            if not job.get("title") or not job.get("company"):
                continue
            
            # Remove duplicates by URL
            url = job.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Clean description
            desc = job.get("description", "")
            desc = self._clean_html(desc)
            desc = self._normalize_whitespace(desc)
            
            # Extract skills properly
            skills = self._extract_skills(desc)
            
            # Parse date
            posted_date = self._parse_date(job.get("posted_date", ""))
            
            cleaned.append({
                "title": job["title"].strip(),
                "company": job["company"].strip(),
                "description": desc,
                "url": url,
                "location": job.get("location", "Remote").strip(),
                "skills": skills,
                "source": job.get("source", "unknown"),
                "posted_date": posted_date,
                # Metadata
                "word_count": len(desc.split()),
                "skill_count": len(skills)
            })
        
        return cleaned
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags"""
        # Simple HTML tag removal
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remove markdown links [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize spaces and newlines"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_skills(self, text: str) -> List[str]:
        from src.parsers.skill_extractor import SkillExtractor
        return SkillExtractor().extract(text)
    
    def _parse_date(self, date_str: str) -> str:
        """Parse various date formats to ISO"""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # Try to parse if it's a timestamp
            if date_str.isdigit():
                dt = datetime.fromtimestamp(int(date_str))
                return dt.isoformat()
            
            # Try common formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%b %d, %Y"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # If all fail, return today
            return datetime.now().isoformat()
        except:
            return datetime.now().isoformat()