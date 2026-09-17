from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseJobBoard(ABC):
    """Abstract class every job board connector must implement."""
    
    # Class-level metadata
    name: str = "unknown"       # e.g., "remoteok"
    display_name: str = "Unknown"  # e.g., "RemoteOK"
    
    @abstractmethod
    def fetch_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch jobs and return a list of standardized dicts.
        
        Required fields per job:
            - title: str
            - company: str
            - description: str
            - url: str
            - location: str
            - skills: List[str]
            - source: str (must equal self.name)
            - posted_date: str (ISO)
        """
        pass