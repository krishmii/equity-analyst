"""The agent team as a LangGraph graph. The process is code; the work inside each node is the model's.

    steps -> research_analyst -> financial_analyst -> investment_advisor -> strategy_manager -> verifier -> END

Every edge is fixed (add_edge, no conditional routing): a model never decides which node runs next.
The Manager's one retry happens inside the Manager node, in code. No role runs more than twice.
The Verifier is the last node on every run. There is no option that removes it.
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, START, StateGraph

from agent_team import manager
from agent_team.runfolder import save_json, save_text
from agent_team.steps import run_steps
from agent_team.verifier import verify

ROLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "roles")
MAX_RUNS_PER_ROLE = 2


class DeskState(TypedDict, total=False):
    ticker: str
    peers: List[str]
    price: float
    run_folder: str
    data: Dict[str, Any]
    outputs: Dict[str, str]
    role_runs: Dict[str, int]
    flags: List[str]
    report_path: str
    marks: Dict[str, int]


def _instructions(role):
    with open(os.path.join(ROLES_DIR, f"{role}.md"), encoding="utf-8") as f:
        text = f.read()
    with open(os.path.join(ROLES_DIR, "SOURCES.md"), encoding="utf-8") as f:
        return text + "\n\n" + f.read()


def _texts(folder):
    from agent_team.runfolder import load_texts
    return load_texts(folder)


def _task(role, state):
    """Each role receives only what the graph gives it, as JSON: task, context, expected output."""
    d, out = state["data"], state.get("outputs", {})
    if role == "research_analyst":
        t = _texts(state["run_folder"])
        ctx = {"company": d["company"], "ticker": d["ticker"], "10-K_text": t.get("10-K", "")[:60000],
               "release_text": t.get("Release", "")[:30000]}
        return {"task": "Describe business model, competitive position, catalysts, recent developments.",
                "context": ctx, "expected_output": "Markdown: ## Overview, ## Market Positioning and Growth Outlook"}
    if role == "financial_analyst":
        ctx = {k: d[k] for k in ("company", "ticker", "price", "facts", "ratios", "quarter", "peers")}
        return {"task": "Statement analysis and valuation from the facts and ratios given.", "context": ctx,
                "expected_output": "Markdown: ## Valuation Insights, with the eleven core claims table, every number sourced"}
    if role == "investment_advisor":
        ctx = {"research_analyst": out.get("research_analyst", ""), "financial_analyst": out.get("financial_analyst", "")}
        return {"task": "Thesis and Buy/Hold/Sell from the two analysts' outputs only.", "context": ctx,
                "expected_output": "Markdown: ## Future Developments and Strategic Recommendations, ## Investment Recommendation"}
    raise ValueError(role)


def _run_role(role, state, feedback=None):
    from desk.roles import call_model
    runs = state.setdefault("role_runs", {})
    if runs.get(role, 0) >= MAX_RUNS_PER_ROLE:
        raise RuntimeError(f"{role} already ran {MAX_RUNS_PER_ROLE} times")
    runs[role] = runs.get(role, 0) + 1
    task = _task(role, state)
    user = json.dumps(task, indent=1, default=str)
    if feedback:
        user += "\n\nThe Strategy Manager sent your part back once: " + "; ".join(feedback) + ". Return all your sections."
    n = runs[role]
    save_json(state["run_folder"], f"nodes/{role}_input_{n}.json", task)
    text = call_model(_instructions(role), user)
    save_text(state["run_folder"], f"nodes/{role}_output_{n}.md", text)
    return text


# ---------------- nodes ----------------
def steps_node(state: DeskState):
    folder, data = run_steps(state["ticker"], state.get("peers", []), state.get("price"))
    return {"run_folder": folder, "data": data, "outputs": {}, "role_runs": {}, "flags": []}


def role_node(role):
    def node(state: DeskState):
        print(f"[node] {role}")
        outputs = dict(state.get("outputs", {}))
        outputs[role] = _run_role(role, state)
        return {"outputs": outputs, "role_runs": state["role_runs"]}
    return node


def manager_node(state: DeskState):
    print("[node] strategy_manager")
    outputs = dict(state["outputs"])
    fails = manager.check(outputs)
    save_json(state["run_folder"], "nodes/strategy_manager_check_1.json", fails)
    for role, why in fails.items():  # one retry per failing role, in code
        print(f"   sent back to {role} once: {why}")
        outputs[role] = _run_role(role, {**state, "outputs": outputs}, feedback=why)
    still = manager.check(outputs)
    save_json(state["run_folder"], "nodes/strategy_manager_check_2.json", still)
    flags = [f"{r}: {w}" for r, ws in still.items() for w in ws]
    d = state["data"]
    report = manager.compile_report(d["filings_line"], datetime.now().isoformat(timespec="seconds"),
                                    d["company"], d["ticker"], outputs, flags)
    path = save_text(state["run_folder"], "report.md", report)
    return {"outputs": outputs, "flags": flags, "report_path": path}


def verifier_node(state: DeskState):
    counts, _ = verify(state["run_folder"])
    return {"marks": counts}


def build_graph():
    g = StateGraph(DeskState)
    g.add_node("steps", steps_node)
    g.add_node("research_analyst", role_node("research_analyst"))
    g.add_node("financial_analyst", role_node("financial_analyst"))
    g.add_node("investment_advisor", role_node("investment_advisor"))
    g.add_node("strategy_manager", manager_node)
    g.add_node("verifier", verifier_node)
    g.add_edge(START, "steps")
    g.add_edge("steps", "research_analyst")
    g.add_edge("research_analyst", "financial_analyst")
    g.add_edge("financial_analyst", "investment_advisor")
    g.add_edge("investment_advisor", "strategy_manager")
    g.add_edge("strategy_manager", "verifier")
    g.add_edge("verifier", END)
    return g.compile()
