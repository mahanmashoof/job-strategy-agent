import json
from src.matchers.job_matcher import JobMatcher

with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)
with open("data/processed/remoteok_cleaned.json") as f:
    jobs = json.load(f)

matcher = JobMatcher()
scored = matcher.match(resume, jobs)

print(f"✅ Scored {len(scored)} jobs\n")

for job in scored[:10]:
    print(f"🎯 {job['match_score_pct']:>5}% | {job['title']} @ {job['company']}")
    print(f"   Breakdown: {job['score_breakdown']}")
    print(f"   Overlap: {job['skill_overlap']}")
    print(f"   Missing: {job['missing_skills']}")
    print()

with open("data/processed/jobs_scored.json", "w") as f:
    json.dump(scored, f, indent=2)
print("✅ Saved")