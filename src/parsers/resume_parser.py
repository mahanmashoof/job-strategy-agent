import re
from typing import Dict, Any, List

class ResumeParser:
    def __init__(self, cv_path: str = "data/cv.md"):
        self.cv_path = cv_path
        self.raw_text = ""
        self.parsed = {}
    
    def load(self) -> "ResumeParser":
        """Load CV file"""
        with open(self.cv_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
        return self
    
    def parse(self) -> Dict[str, Any]:
        """Parse CV into structured data"""
        self.parsed = {
            "raw_text": self.raw_text,
            "name": self._extract_name(),
            "email": self._extract_email(),
            "skills": self._extract_skills(),
            "word_count": len(self.raw_text.split())
        }
        return self.parsed
    
    def _extract_email(self) -> str:
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', self.raw_text)
        return match.group(0) if match else ""
    
    def _extract_name(self) -> str:
        """Assume first non-empty line is the name"""
        for line in self.raw_text.splitlines():
            line = line.strip()
            if line and len(line) < 60:
                return line
        return ""
    
    def _extract_skills(self) -> List[str]:
        """Extract skills using the same list as job cleaner"""
        from src.cleaners.job_cleaner import JobCleaner
        cleaner = JobCleaner()
        
        text_lower = self.raw_text.lower()
        found = []
        for skill in cleaner.known_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text_lower):
                found.append(skill)
        return sorted(found)