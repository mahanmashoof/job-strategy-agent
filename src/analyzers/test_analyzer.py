import json
from src.analyzers.market_analyzer import MarketAnalyzer

with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)
with open("data/processed/jobs_scored.json") as f:
    jobs = json.load(f)

analyzer = MarketAnalyzer(top_n=15, min_score=0.3)
report = analyzer.analyze(resume, jobs)

# Print summary
s = report["summary"]
print("=" * 60)
print("📊 MARKET ANALYSIS")
print("=" * 60)
print(f"Scraped: {s['total_jobs_scraped']} | Relevant: {s['relevant_jobs']} | Avg score: {s['avg_match_score']}")
print(f"Skill gap ratio: {s['skill_gap_ratio']} (0 = perfect fit, 1 = nothing in common)")
print()

print("🔥 TOP DEMANDED SKILLS:")
for item in report["top_demanded_skills"]:
    marker = "✅" if item["skill"] in {s["skill"] for s in report["your_strengths"]} else "❌"
    print(f"  {marker} {item['skill']:<15} {item['pct']:>5}% ({item['count']} jobs)")

print()
print("🎯 YOUR STRENGTHS (in demand + you have):")
for s in report["your_strengths"]:
    print(f"  ✅ {s['skill']}")

print()
print("⚠️  TOP SKILL GAPS (in demand, missing from CV):")
for g in report["skill_gaps"][:10]:
    print(f"  ❌ {g['skill']:<15} {g['pct']:>5}% ({g['count']} jobs)")

print()
print("🏢 TOP COMPANIES HIRING:")
for c in report["top_companies"]:
    print(f"  {c['company']} ({c['openings']})")

# Save full report
with open("data/processed/market_analysis.json", "w") as f:
    json.dump(report, f, indent=2)
print("\n✅ Saved to data/processed/market_analysis.json")