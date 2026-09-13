from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    # Weights must sum to 1.0
    WEIGHT_SKILLS = 0.50
    WEIGHT_TITLE = 0.25
    WEIGHT_TFIDF = 0.25
    
    def __init__(self, target_roles_path: str = "data/target_roles.txt"):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        self.target_roles = self._load_target_roles(target_roles_path)
    
    def _load_target_roles(self, path: str) -> List[str]:
        try:
            with open(path, "r") as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def match(self, resume: Dict[str, Any], jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not jobs:
            return []
        
        # === TF-IDF baseline ===
        resume_text = resume["raw_text"]
        job_texts = [self._job_to_text(j) for j in jobs]
        tfidf_matrix = self.vectorizer.fit_transform([resume_text] + job_texts)
        similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]
        
        # === Score each job ===
        resume_skills = set(resume.get("skills", []))
        scored = []
        
        for job, tfidf_score in zip(jobs, similarities):
            job_skills = set(job.get("skills", []))
            overlap = resume_skills & job_skills
            missing = job_skills - resume_skills
            
            # --- Skill score (0-1) ---
            # Coverage: how many of job's skills you have
            # Weighted: overlap ratio, but boost if job requires few skills (more signal)
            if job_skills:
                coverage = len(overlap) / len(job_skills)
            else:
                coverage = 0
            
            # --- Title score (0-1) ---
            title_score = self._title_match(job.get("title", ""))
            
            # --- Combined weighted score ---
            combined = (
                self.WEIGHT_SKILLS * coverage +
                self.WEIGHT_TITLE * title_score +
                self.WEIGHT_TFIDF * min(tfidf_score * 5, 1.0)  # scale up weak tfidf
            )
            
            scored.append({
                **job,
                "match_score": round(combined, 4),
                "match_score_pct": round(combined * 100, 1),
                "score_breakdown": {
                    "skills": round(coverage, 3),
                    "title": round(title_score, 3),
                    "tfidf": round(float(tfidf_score), 4)
                },
                "skill_overlap": sorted(list(overlap)),
                "missing_skills": sorted(list(missing)),
                "overlap_ratio": round(coverage, 2)
            })
        
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return scored
    
    def _title_match(self, title: str) -> float:
        """Return 1.0 if title matches any target role, else fuzzy score"""
        if not title or not self.target_roles:
            return 0.0
        
        title_lower = title.lower()
        
        # Exact substring match (strongest signal)
        for role in self.target_roles:
            if role in title_lower:
                return 1.0
        
        # Partial word overlap
        title_words = set(title_lower.split())
        best = 0.0
        for role in self.target_roles:
            role_words = set(role.split())
            if not role_words:
                continue
            overlap = len(title_words & role_words) / len(role_words)
            best = max(best, overlap * 0.7)  # cap partial at 0.7
        return best
    
    def _job_to_text(self, job: Dict[str, Any]) -> str:
        return f"{job.get('title', '')} {job.get('description', '')}"