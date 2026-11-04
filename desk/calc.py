"""Step 5: the calculator. Every ratio is computed in code and shows its arithmetic.

Definitions follow the course's report audit:
- operating margin = operating income / total revenue
- return on average equity = net income / average(this year's, last year's equity)
- debt to equity = (long-term debt + its current portion) / stockholders' equity
- free cash flow = cash from operations - additions to property and equipment
- P/E = price / diluted EPS (latest fiscal year, GAAP)
"""


def _v(fx, concept, which="current"):
    it = fx["items"].get(concept) or {}
    rec = it.get(which)
    return None if rec is None else rec["value"]


def _m(x):
    return f"{x / 1e6:,.0f}M"


def ratios(fx, price=None):
    out = {}
    rev, rev0 = _v(fx, "total_revenue"), _v(fx, "total_revenue", "prior")
    oi = _v(fx, "operating_income")
    ni = _v(fx, "net_income")
    eq, eq0 = _v(fx, "stockholders_equity"), _v(fx, "stockholders_equity", "prior")
    ltd, ltdc = _v(fx, "long_term_debt_noncurrent"), _v(fx, "long_term_debt_current")
    cfo, capex = _v(fx, "cash_from_operations"), _v(fx, "capex")
    eps = _v(fx, "diluted_eps")

    if rev and rev0:
        g = rev / rev0 - 1
        out["revenue_growth"] = {"value": g, "arithmetic": f"{_m(rev)} / {_m(rev0)} - 1 = {g:.2%}"}
    if oi is not None and rev:
        m = oi / rev
        out["operating_margin"] = {"value": m, "arithmetic": f"{_m(oi)} / {_m(rev)} = {m:.2%}"}
    if ni is not None and eq and eq0:
        avg = (eq + eq0) / 2
        r = ni / avg
        out["return_on_average_equity"] = {"value": r, "arithmetic": f"{_m(ni)} / (({_m(eq)} + {_m(eq0)}) / 2 = {_m(avg)}) = {r:.2%}"}
    if ltd is not None and eq:
        cur = ltdc or 0
        d = (ltd + cur) / eq
        out["debt_to_equity"] = {"value": d, "arithmetic": f"({_m(ltd)} + {_m(cur)} current) / {_m(eq)} = {d:.2f}x"}
    if cfo is not None and capex is not None:
        f = cfo - capex
        out["free_cash_flow"] = {"value": f, "arithmetic": f"{_m(cfo)} - {_m(capex)} = {_m(f)}"}
    if price and eps:
        pe = price / eps
        out["pe"] = {"value": pe, "arithmetic": f"${price:,.2f} / ${eps:.2f} = {pe:.1f}x"}
    return out


def operating_margin(rev, oi):
    m = oi / rev
    return {"value": m, "arithmetic": f"{_m(oi)} / {_m(rev)} = {m:.2%}"}
