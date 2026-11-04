"""The agent team's process, tested without a network or a model key:
fixed node order, the Manager's one retry, the Verifier on every run, and no way to skip it."""
import os
import re
import shutil

import pytest

from agent_team import graph as G
from agent_team.runfolder import load_json

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED = os.path.join(HERE, "runs", "COSTCO_WHOLESALE_CORP_NEW_2026-11-04_fallback")


def _sections(report, *titles):
    parts = re.split(r"(?m)^(## .+)$", report)
    keep = []
    for i in range(1, len(parts), 2):
        if parts[i][3:].strip() in titles:
            keep.append(parts[i] + parts[i + 1])
    return "\n".join(keep)


@pytest.fixture
def team(tmp_path, monkeypatch, capsys):
    report = open(os.path.join(SAVED, "report.md"), encoding="utf-8").read()
    canned = {
        "research_analyst": _sections(report, "Overview", "Market Positioning and Growth Outlook"),
        "financial_analyst": _sections(report, "Valuation Insights"),
        "investment_advisor": _sections(report, "Future Developments and Strategic Recommendations", "Investment Recommendation"),
    }
    calls = []

    def fake_steps(ticker, peers, price):
        print("[node] steps")
        dst = tmp_path / "run"
        shutil.copytree(SAVED, dst, ignore=shutil.ignore_patterns("report.md", "verified_report.md", "verifier_marks.json"))
        return str(dst), load_json(str(dst), "facts.json")

    def fake_model(system, user):
        first = system.splitlines()[0]
        role = next(r for r in canned if r.replace("_", " ").title() in first)
        calls.append(role)
        out = canned[role]
        if role == "investment_advisor" and calls.count(role) == 1:  # first try forgets a part
            out = out.split("## Investment Recommendation")[0]
        return out

    monkeypatch.setattr(G, "run_steps", fake_steps)
    monkeypatch.setattr("desk.roles.call_model", fake_model)
    monkeypatch.delenv("API_KEY", raising=False)
    final = G.build_graph().invoke({"ticker": "TEST", "peers": [], "price": 1.0})
    return final, calls, capsys.readouterr().out


def test_node_order_retry_and_verifier(team):
    final, calls, out = team
    order = re.findall(r"\[node\] (\w+)", out)
    assert order == ["steps", "research_analyst", "financial_analyst", "investment_advisor",
                     "strategy_manager", "verifier"]
    assert calls.count("investment_advisor") == 2          # sent back once
    assert max(calls.count(r) for r in set(calls)) <= 2     # no role more than twice
    assert os.path.exists(os.path.join(final["run_folder"], "verified_report.md"))
    assert final["marks"]["wrong"] == 0 and final["marks"]["unsupported"] == 0


def test_no_way_to_skip_the_verifier():
    src = open(os.path.join(HERE, "agent_team", "graph.py"), encoding="utf-8").read()
    src += open(os.path.join(HERE, "run_team.py"), encoding="utf-8").read()
    assert "add_conditional_edges" not in src
    assert not re.search(r"(no|skip)[-_]?verif", src, re.I)
