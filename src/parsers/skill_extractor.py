import re
from typing import List
from src.parsers.skills_db import ALIAS_MAP

class SkillExtractor:
    def extract(self, text: str) -> List[str]:
        """Extract skills using aliases and word boundaries"""
        text_lower = text.lower()
        found = set()
        
        for alias, canonical in ALIAS_MAP.items():
            # Escape special chars (. + #)
            pattern = rf'(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])'
            if re.search(pattern, text_lower):
                found.add(canonical)
        
        return sorted(found)