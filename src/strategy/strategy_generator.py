import json
import re
from typing import Dict, Any
from anthropic import Anthropic
from config.settings import Config


class StrategyGenerator:
    def __init__(self, model: str = "claude-haiku-4-5"):
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = model

    # ---------- Public API ----------

    def generate(self, resume: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate raw LLM strategy text (report + dashboard JSON)."""
        career_context = self._load_career_context()
        prompt = self._build_prompt(resume, analysis, career_context)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def generate_and_parse(self, resume: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Returns {'report': str, 'dashboard': dict}"""
        raw = self.generate(resume, analysis)

        marker = "## DASHBOARD DATA"
        if marker in raw:
            report_part, dashboard_part = raw.split(marker, 1)
            report = report_part.strip()
            dashboard = self._extract_json(dashboard_part)
        else:
            report = raw.strip()
            dashboard = {}

        return {"report": report, "dashboard": dashboard}

    # ---------- Internals ----------

    def _load_career_context(self) -> str:
        try:
            with open("data/career_context.txt", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from a fenced code block."""
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return {}

    def _build_prompt(self, resume: Dict[str, Any], analysis: Dict[str, Any], career_context: str = "") -> str:
        # Trim data to keep prompt lean
        summary = analysis["summary"]
        demanded = analysis["top_demanded_skills"][:10]
        gaps = analysis["skill_gaps"][:10]
        strengths = analysis["your_strengths"][:10]

        top_jobs = analysis["relevant_jobs"][:5]
        jobs_snippet = "\n".join(
            f"- {j['title']} @ {j['company']} (match: {j['match_score_pct']}%)"
            for j in top_jobs
        )

        return f"""You are a career strategist. Analyze this job market data and create a focused 12-month plan for landing a remote full-time role.

## CANDIDATE'S STATED DIRECTION (READ CAREFULLY — DO NOT IGNORE)
{career_context}

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

1. **Market Positioning** — Based on the candidate's EXISTING skills, which specific role types should they target?
2. **Skill Priorities** — AT MOST 2 skills to add, with clear ROI justification (jobs unlocked per study hour). If no new skills are justified, say so and focus on reframing existing skills instead.
3. **Quarterly Roadmap** — 4 quarters, realistic given 1 hour/day. Include active applications throughout the year, not just at the end.
4. **Quick Wins** — 3 things in the next 2 weeks.
5. **Risks & Watch-outs** — 2-3 honest warnings.

## CRITICAL RULES
- The candidate has 6 years of experience. Do NOT position them as junior.
- Do NOT recommend becoming "senior backend" or pivoting to DevOps.
- Do NOT suggest learning Go, Python, or Ruby unless FRONTEND job data clearly demands them.
- Learning must have measurable ROI: "learning X unlocks Y additional relevant jobs."
- Prioritize landing a role FAST with existing skills over long study periods.
- Respect the 1h/day constraint. No unrealistic plans.
- Be direct and specific. No fluff. Assume the reader is a competent developer who wants hard truths.

## STRUCTURED OUTPUT
After the 5 sections above, add a section titled `## DASHBOARD DATA` containing ONLY a fenced JSON code block (```json ... ```) with this exact schema:

{{
  "quarters": [
    {{
      "label": "Q1 2026",
      "focus": "short focus phrase",
      "actions": ["action 1", "action 2", "action 3"],
      "success_metric": "one measurable outcome"
    }}
  ],
  "quick_wins": [
    {{"task": "task description", "deadline_days": 14}}
  ],
  "skill_priorities": [
    {{"skill": "skill name", "rank": 1, "reason": "one sentence"}}
  ]
}}

Do not include any other text after the JSON block.
"""