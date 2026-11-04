"""The Strategy Manager: a checklist in code (roles/strategy_manager.md). No model call."""
import re

PARTS = [
    "Overview",
    "Market Positioning and Growth Outlook",
    "Valuation Insights",
    "Future Developments and Strategic Recommendations",
    "Investment Recommendation",
]
OWNER = {PARTS[0]: "research_analyst", PARTS[1]: "research_analyst", PARTS[2]: "financial_analyst",
         PARTS[3]: "investment_advisor", PARTS[4]: "investment_advisor"}


def has_part(md, part):
    return re.search(rf"(?mi)^##\s+{re.escape(part)}\s*$", md or "") is not None


def check(outputs):
    """Return {role: [failing parts]} for the five parts and the recommendation's consistency."""
    fails = {}
    for part, role in OWNER.items():
        if not has_part(outputs.get(role, ""), part):
            fails.setdefault(role, []).append(f"missing '## {part}'")
    ia = outputs.get("investment_advisor", "")
    recs = re.findall(r"(?m)^\**Recommendation:\**\s*\**(Buy|Hold|Sell)\b", ia)
    if len(recs) != 1:
        fails.setdefault("investment_advisor", []).append("needs exactly one 'Recommendation: Buy|Hold|Sell' line")
    if not re.search(r"(?mi)^\**Deciding number:", ia):
        fails.setdefault("investment_advisor", []).append("needs a 'Deciding number:' line")
    return fails


def compile_report(filings_line, run_time, company, ticker, outputs, flags):
    head = f"{filings_line}\nRun time: {run_time}\n\n"
    if flags:
        head += "> Strategy Manager flags after one retry: " + "; ".join(flags) + "\n\n"
    body = "\n\n".join(outputs[r] for r in ("research_analyst", "financial_analyst", "investment_advisor"))
    foot = ("\n\n---\nThis is a learning exercise, not financial advice.\n\n"
            "AI assistance: [the tools you used]. I verified the sources myself; the judgments are mine.\n\n"
            "Any remaining errors are my own.\n")
    return head + f"# {company} ({ticker}) — Equity Research Report\n\n" + body + foot
