import json
from src.strategy.strategy_generator import StrategyGenerator

with open("data/processed/resume_parsed.json") as f:
    resume = json.load(f)
with open("data/processed/market_analysis.json") as f:
    analysis = json.load(f)

generator = StrategyGenerator()
print("⏳ Generating strategy...")
report = generator.generate(resume, analysis)

# Save
with open("output/strategy_report.md", "w") as f:
    f.write(report)

print("✅ Saved to output/strategy_report.md\n")
print("=" * 60)
print(report[:1500])  # preview first 1500 chars
print("...")