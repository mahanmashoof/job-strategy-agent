import sys
from src.scrapers.boards.registry import fetch_all
from src.cleaners.job_cleaner import JobCleaner
from src.parsers.resume_parser import ResumeParser
from src.matchers.job_matcher import JobMatcher
from src.analyzers.market_analyzer import MarketAnalyzer
from src.strategy.strategy_generator import StrategyGenerator
from src.strategy.dashboard_formatter import DashboardFormatter
from src.utils.file_io import write_json, write_text, read_json


def main():
    print("=" * 60)
    print("🚀 JOB STRATEGY AGENT")
    print("=" * 60)
    
    # 1. Fetch
    print("\n[1/6] Fetching jobs from all boards...")
    raw_jobs = fetch_all(limit_per_board=999999)
    write_json("data/raw/all_jobs.json", raw_jobs)
    print(f"   → {len(raw_jobs)} jobs collected")
    
    # 2. Clean
    print("\n[2/6] Cleaning + filtering...")
    cleaned = JobCleaner().clean(raw_jobs, filter_titles=True)
    write_json("data/processed/jobs_cleaned.json", cleaned)
    print(f"   → {len(cleaned)} jobs after cleaning")
    
    if not cleaned:
        print("❌ No jobs survived cleaning. Check target_roles.txt")
        sys.exit(1)
    
    # 3. Parse resume
    print("\n[3/6] Parsing CV...")
    resume = ResumeParser().load().parse()
    write_json("data/processed/resume_parsed.json", resume)
    print(f"   → {len(resume['skills'])} skills extracted")
    
    # 4. Score
    print("\n[4/6] Scoring jobs against CV...")
    scored = JobMatcher().match(resume, cleaned)
    write_json("data/processed/jobs_scored.json", scored)
    top = scored[0] if scored else None
    if top:
        print(f"   → Top match: {top['match_score_pct']}% — {top['title']}")
    
    # 5. Analyze
    print("\n[5/6] Analyzing market...")
    analysis = MarketAnalyzer(top_n=15, min_score=0.3).analyze(resume, scored)
    write_json("data/processed/market_analysis.json", analysis)
    s = analysis["summary"]
    print(f"   → {s['relevant_jobs']} relevant jobs, gap ratio: {s['skill_gap_ratio']}")
    
    # 6. Strategy
    print("\n[6/6] Generating strategy (LLM)...")
    result = StrategyGenerator().generate_and_parse(resume, analysis)
    final = DashboardFormatter().format(result["report"], result["dashboard"])
    write_text("output/strategy_report.md", final)
    print(f"   → Report saved ({len(final)} chars)")
    
    print("\n" + "=" * 60)
    print(f"✅ DONE — check output/strategy_report.md")
    print("=" * 60)


if __name__ == "__main__":
    main()