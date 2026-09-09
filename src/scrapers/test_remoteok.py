from src.scrapers.remoteok import RemoteOKScraper
import json

scraper = RemoteOKScraper()
jobs = scraper.fetch_jobs(limit=10)

print(f"✅ Fetched {len(jobs)} jobs")

if jobs:
    # Show first job summary
    first = jobs[0]
    print(f"\n📋 Sample job:")
    print(f"  Title: {first['title']}")
    print(f"  Company: {first['company']}")
    print(f"  Skills found: {first['skills']}")
    
    # Save to file
    with open("data/raw/remoteok_sample.json", "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"\n✅ Saved to data/raw/remoteok_sample.json")