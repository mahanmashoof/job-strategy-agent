import json
from anthropic import Anthropic
from config.settings import Config
from typing import Dict, Any

class StrategyGenerator:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = model
    
    def generate(self, resume: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate a 12-month strategy report"""
        
        prompt = self._build_prompt(resume, analysis)
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _build_prompt(self, resume: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        # Trim data to keep prompt lean
        summary = analysis["summary"]
        demanded = analysis["top_demanded_skills"][:10]
        gaps = analysis["skill_gaps"][:10]
        strengths = analysis["your_strengths"][:10]
        
        # Sample top jobs
        top_jobs = analysis["relevant_jobs"][:5]
        jobs_snippet = "\n".join([
            f"- {j['title']} @ {j['company']} (match: {j['match_score_pct']}%)"
            for j in top_jobs
        ])
        
        return f"""You are a career strategist. Analyze this job market data and create a focused 12-month plan for landing a remote full-time role.

## CANDIDATE PROFILE
Current skills: {', '.join(resume.get('skills', []))}
CV word count: {resume.get('word_count', 0)}

## MARKET DATA (from {summary['relevant_jobs']} relevant remote jobs)
Average match score: {summary['avg_match_score']}
Skill gap ratio: {summary['skill_gap_ratio']} (0 = perfect fit, 1 = no overlap)

### Top demanded skills:
{json.dumps(demanded, indent=2)}

### Candidate's strengths (in demand + already has):
{json.dumps(strengths, indent=2)}

### Top skill gaps (in demand, missing from CV):
{json.dumps(gaps, indent=2)}

### Sample of top-matching jobs:
{jobs_snippet}

## YOUR TASK
Write a 12-month strategy with these sections:

1. **Market Positioning** — What kind of role should they target? (2-3 sentences)
2. **Skill Priorities** — Top 3 skills to learn, in order, with reasoning (why these over the others)
3. **Quarterly Roadmap** — Break the 12 months into 4 quarters. Each quarter: focus, 2-3 concrete actions, success metric.
4. **Quick Wins** — 3 things they can do in the next 2 weeks to improve their standing.
5. **Risks & Watch-outs** — 2-3 honest warnings about this market.

Be direct and specific. No fluff. Use markdown formatting. Assume the reader is a competent developer who wants hard truths, not encouragement.
"""