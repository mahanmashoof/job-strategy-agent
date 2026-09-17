from src.scrapers.boards.registry import fetch_all, list_boards
import json

print(f"Registered boards: {list_boards()}")
jobs = fetch_all(limit_per_board=100)
print(f"\n✅ Total: {len(jobs)} jobs")

with open("data/raw/all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)
print("Saved to data/raw/all_jobs.json")