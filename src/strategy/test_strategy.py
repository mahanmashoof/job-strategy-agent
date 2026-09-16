import json
import os
from src.strategy.strategy_generator import StrategyGenerator
from src.strategy.dashboard_formatter import DashboardFormatter

os.makedirs("output", exist_ok=True)

with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)
with open("data/processed/market_analysis.json") as f:
    analysis = json.load(f)

generator = StrategyGenerator()
print("⏳ Generating strategy...")
result = generator.generate_and_parse(resume, analysis)

formatter = DashboardFormatter()
final = formatter.format(result["report"], result["dashboard"])

with open("output/strategy_report.md", "w", encoding="utf-8") as f:
    f.write(final)

print(f"✅ Saved ({len(final)} chars)")
print(f"Dashboard parsed: {bool(result['dashboard'])}")
print()
print(final[:1200])