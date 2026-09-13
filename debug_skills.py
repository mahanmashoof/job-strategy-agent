import json

with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)
with open("data/processed/remoteok_cleaned.json") as f:
    jobs = json.load(f)

print("RESUME SKILLS:")
print(resume["skills"])
print()

print("SAMPLE JOB SKILLS:")
for job in jobs[:3]:
    print(f"  {job['title']}: {job['skills']}")