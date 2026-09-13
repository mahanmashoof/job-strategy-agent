from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),  # unigrams + bigrams
            max_features=5000
        )
    
    def match(self, resume: Dict[str, Any], jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score each job against the resume"""
        if not jobs:
            return []
        
        resume_text = resume["raw_text"]
        job_texts = [self._job_to_text(j) for j in jobs]
        
        # Fit on resume + all jobs together (shared vocabulary)
        all_texts = [resume_text] + job_texts
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        resume_vec = tfidf_matrix[0]
        job_vecs = tfidf_matrix[1:]
        
        # Cosine similarity
        similarities = cosine_similarity(resume_vec, job_vecs)[0]
        
        # Attach score + skill overlap to each job
        resume_skills = set(resume.get("skills", []))
        scored = []
        for job, score in zip(jobs, similarities):
            job_skills = set(job.get("skills", []))
            overlap = resume_skills & job_skills
            missing = job_skills - resume_skills
            
            scored.append({
                **job,
                "match_score": round(float(score), 4),
                "skill_overlap": sorted(list(overlap)),
                "missing_skills": sorted(list(missing)),
                "overlap_ratio": round(len(overlap) / len(job_skills), 2) if job_skills else 0
            })
        
        # Sort by score descending
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return scored
    
    def _job_to_text(self, job: Dict[str, Any]) -> str:
        """Combine title + description for vectorization"""
        return f"{job.get('title', '')} {job.get('description', '')}"