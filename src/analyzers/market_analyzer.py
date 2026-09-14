from typing import List, Dict, Any
from collections import Counter

class MarketAnalyzer:
    def __init__(self, top_n: int = 15, min_score: float = 0.3):
        self.top_n = top_n
        self.min_score = min_score  # only analyze jobs above this match
    
    def analyze(self, resume: Dict[str, Any], scored_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate market insights from scored jobs"""
        
        # Filter to relevant jobs only
        relevant = [j for j in scored_jobs if j["match_score"] >= self.min_score]
        
        if not relevant:
            return {"error": "No jobs above threshold", "threshold": self.min_score}
        
        resume_skills = set(resume.get("skills", []))
        
        # === 1. Skill demand across relevant jobs ===
        all_skills = Counter()
        for job in relevant:
            for skill in job.get("skills", []):
                all_skills[skill] += 1
        
        top_demanded = all_skills.most_common(self.top_n)
        
        # === 2. Missing skills (demanded but not in resume) ===
        missing = [(s, c) for s, c in top_demanded if s not in resume_skills]
        
        # === 3. Your strongest skills (in resume AND in demand) ===
        strengths = [(s, c) for s, c in top_demanded if s in resume_skills]
        
        # === 4. Skill demand by % of jobs ===
        total_jobs = len(relevant)
        skill_pct = [
            {"skill": s, "count": c, "pct": round(c / total_jobs * 100, 1)}
            for s, c in top_demanded
        ]
        
        # === 5. Top companies hiring ===
        companies = Counter(j["company"] for j in relevant).most_common(10)
        
        # === 6. Average match score ===
        avg_score = sum(j["match_score"] for j in relevant) / len(relevant)
        
        # === 7. Skill gap ratio ===
        if all_skills:
            skills_you_have = sum(1 for s in all_skills if s in resume_skills)
            gap_ratio = round(1 - (skills_you_have / len(all_skills)), 2)
        else:
            gap_ratio = 0
        
        return {
            "summary": {
                "total_jobs_scraped": len(scored_jobs),
                "relevant_jobs": len(relevant),
                "min_score_threshold": self.min_score,
                "avg_match_score": round(avg_score, 3),
                "skill_gap_ratio": gap_ratio
            },
            "top_demanded_skills": skill_pct,
            "your_strengths": [{"skill": s, "count": c} for s, c in strengths],
            "skill_gaps": [{"skill": s, "count": c, "pct": round(c / total_jobs * 100, 1)} 
                          for s, c in missing],
            "top_companies": [{"company": c, "openings": n} for c, n in companies],
            "relevant_jobs": relevant  # keep for LLM stage
        }