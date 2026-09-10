import json
from src.parsers.resume_parser import ResumeParser

parser = ResumeParser().load()
parsed = parser.parse()

print(f"✅ Parsed CV")
print(f"  Name: {parsed['name']}")
print(f"  Email: {parsed['email']}")
print(f"  Skills found: {parsed['skills']}")
print(f"  Word count: {parsed['word_count']}")

# Save
with open("data/processed/resume_parsed.json", "w") as f:
    json.dump(parsed, f, indent=2)

print(f"\n✅ Saved to data/processed/resume_parsed.json")