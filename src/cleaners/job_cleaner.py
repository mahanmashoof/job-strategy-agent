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
    
    def clean(self, jobs: List[Dict[str, Any]], filter_titles: bool = True) -> List[Dict[str, Any]]:
        """Clean and validate job data"""
        cleaned = []
        seen_urls = set()
        
        # Load target roles for filtering
        target_roles = []
        if filter_titles:
            try:
                with open("data/target_roles.txt") as f:
                    target_roles = [line.strip().lower() for line in f if line.strip()]
            except FileNotFoundError:
                pass
        
        skipped_no_match = 0
        
        for job in jobs:
            # Skip if missing critical fields
            if not job.get("title") or not job.get("company"):
                continue
            
            # Remove duplicates by URL
            url = job.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # NEW: Title filter
            if target_roles:
                title_lower = job["title"].lower()
                if not any(role in title_lower for role in target_roles):
                    skipped_no_match += 1
                    continue
            
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
                "word_count": len(desc.split()),
                "skill_count": len(skills)
            })
        
        if skipped_no_match:
            print(f"ℹ️  Filtered out {skipped_no_match} jobs (title didn't match target roles)")
        
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
        from email.utils import parsedate_to_datetime
        if not date_str:
            return datetime.now().isoformat()
        
        # Unix timestamp
        if date_str.isdigit():
            return datetime.fromtimestamp(int(date_str)).isoformat()
        
        # RFC 822 (RSS feeds: "Wed, 19 Aug 2026 20:37:20 +0000")
        try:
            return parsedate_to_datetime(date_str).isoformat()
        except (TypeError, ValueError):
            pass
        
        # ISO and common formats
        for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%b %d, %Y"]:
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue
        
        return datetime.now().isoformat()