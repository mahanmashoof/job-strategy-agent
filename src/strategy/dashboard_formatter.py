from typing import Dict, Any

class DashboardFormatter:
    def format(self, report: str, dashboard: Dict[str, Any]) -> str:
        """Combine LLM report with a structured dashboard"""
        lines = ["# 🎯 12-Month Strategy Report", ""]
        lines.append(report)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📊 Action Dashboard")
        lines.append("")
        
        # Quarter table
        quarters = dashboard.get("quarters", [])
        if quarters:
            lines.append("### Quarterly Roadmap")
            lines.append("")
            lines.append("| Quarter | Focus | Actions | Success Metric | Status |")
            lines.append("|---------|-------|---------|----------------|--------|")
            for q in quarters:
                actions = "<br>".join(f"• {a}" for a in q.get("actions", []))
                lines.append(
                    f"| **{q.get('label', '')}** | {q.get('focus', '')} | {actions} | {q.get('success_metric', '')} | ⬜ |"
                )
            lines.append("")
        
        # Quick wins checklist
        quick_wins = dashboard.get("quick_wins", [])
        if quick_wins:
            lines.append("### ⚡ Quick Wins (Next 2 Weeks)")
            lines.append("")
            for w in quick_wins:
                lines.append(f"- [ ] {w.get('task', '')} *(by day {w.get('deadline_days', '?')})*")
            lines.append("")
        
        # Skill priorities
        skills = dashboard.get("skill_priorities", [])
        if skills:
            lines.append("### 🧠 Skill Priorities")
            lines.append("")
            for s in skills:
                lines.append(f"**{s.get('rank', '?')}. {s.get('skill', '')}** — {s.get('reason', '')}")
            lines.append("")
        
        return "\n".join(lines)