import json
from src.matchers.job_matcher import JobMatcher

# Load data
with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)

with open("data/processed/remoteok_cleaned.json") as f:
    jobs = json.load(f)

# Match
matcher = JobMatcher()
scored = matcher.match(resume, jobs)

print(f"✅ Scored {len(scored)} jobs\n")

for job in scored[:5]:
    print(f"🎯 {job['match_score']:.3f} | {job['title']} @ {job['company']}")
    print(f"   Overlap: {job['skill_overlap']}")
    print(f"   Missing: {job['missing_skills']}")
    print()

# Save
with open("data/processed/jobs_scored.json", "w") as f:
    json.dump(scored, f, indent=2)

print("✅ Saved to data/processed/jobs_scored.json")