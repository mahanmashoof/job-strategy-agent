import json
from src.cleaners.job_cleaner import JobCleaner

# Load sample data
with open("data/raw/remoteok_sample.json", "r") as f:
    raw_jobs = json.load(f)

# Clean it
cleaner = JobCleaner()
cleaned_jobs = cleaner.clean(raw_jobs)

print(f"✅ Cleaned {len(cleaned_jobs)} jobs from {len(raw_jobs)} raw")

# Show sample
if cleaned_jobs:
    job = cleaned_jobs[0]
    print(f"\n📋 Cleaned sample:")
    print(f"  Title: {job['title']}")
    print(f"  Company: {job['company']}")
    print(f"  Skills: {job['skills']}")
    print(f"  Word count: {job['word_count']}")
    print(f"  Skill count: {job['skill_count']}")

# Save cleaned data
with open("data/processed/remoteok_cleaned.json", "w") as f:
    json.dump(cleaned_jobs, f, indent=2)

print(f"\n✅ Saved to data/processed/remoteok_cleaned.json")