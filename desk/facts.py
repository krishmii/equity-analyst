"""Steps 4 and 7: read the statements as data from the XBRL company facts.

Rules (from Lab 02 and the report audit):
- When a concept has several candidate tags, choose the tag whose latest
  fiscal year is newest (filers move between tags across years).
- Read every concept for the SAME fiscal year as revenue, with the prior year beside it.
- Every value keeps its tag, period end and accession number.
"""
from datetime import date

# Candidate tags, in order of preference when two tags tie on the newest year.
CONCEPTS = {
    "total_revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
                      "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"],
    "diluted_eps": ["EarningsPerShareDiluted"],
    "stockholders_equity": ["StockholdersEquity",
                            "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "long_term_debt_noncurrent": ["LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations",
                                  "LongTermDebtAndFinanceLeaseObligationsNoncurrent"],
    "long_term_debt_current": ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent",
                               "LongTermDebtAndFinanceLeaseObligationsCurrent"],
    "cash_from_operations": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
INSTANT = {"stockholders_equity", "long_term_debt_noncurrent", "long_term_debt_current"}
LABELS = {
    "total_revenue": "Total revenue",
    "operating_income": "Operating income",
    "net_income": "Net income attributable to the company",
    "diluted_eps": "Diluted EPS (GAAP)",
    "stockholders_equity": "Stockholders' equity",
    "long_term_debt_noncurrent": "Long-term debt (noncurrent)",
    "long_term_debt_current": "Current portion of long-term debt",
    "cash_from_operations": "Cash from operations",
    "capex": "Additions to property and equipment",
}


def _days(start, end):
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def _annual_rows(facts, tag, instant):
    node = facts.get("facts", {}).get("us-gaap", {}).get(tag)
    if not node:
        return []
    unit = "USD/shares" if "USD/shares" in node["units"] else ("USD" if "USD" in node["units"] else next(iter(node["units"])))
    rows = []
    for x in node["units"][unit]:
        if x.get("form") not in ("10-K", "10-K/A"):
            continue
        if instant:
            if "start" in x:
                continue
        else:
            if "start" not in x or not (350 <= _days(x["start"], x["end"]) <= 380):
                continue
        rows.append({**x, "tag": tag, "unit": unit})
    return rows


def pick_tag(facts, concept):
    """Among candidate tags, choose the one whose latest year is newest."""
    instant = concept in INSTANT
    best = None
    for tag in CONCEPTS[concept]:
        rows = _annual_rows(facts, tag, instant)
        if not rows:
            continue
        latest = max(r["end"] for r in rows)
        if best is None or latest > best[1]:
            best = (tag, latest, rows)
    return best  # (tag, latest_end, rows) or None


def _value_at(rows, end, accn_pref=None):
    """Value for a period end; prefer the figure as reported in the given filing."""
    hits = [r for r in rows if r["end"] == end]
    if not hits:
        return None
    if accn_pref:
        pref = [r for r in hits if r["accn"] == accn_pref]
        if pref:
            return pref[-1]
    return sorted(hits, key=lambda r: r.get("filed", ""))[-1]


def read_facts(facts, tenk_accession=None):
    """Return {concept: {current, prior}} for the fiscal year of revenue in the latest 10-K."""
    rev = pick_tag(facts, "total_revenue")
    if rev is None:
        raise SystemExit("No revenue tag found in company facts.")
    tag, fy_end, rows = rev
    cur_rev = _value_at(rows, fy_end, tenk_accession)
    accn = tenk_accession or cur_rev["accn"]
    # prior fiscal year end = the revenue row in the same filing that ends ~1 year earlier
    prior_candidates = sorted({r["end"] for r in rows if 350 <= _days(r["end"], fy_end) <= 380})
    prior_end = prior_candidates[-1] if prior_candidates else None

    out = {"fiscal_year_end": fy_end, "prior_year_end": prior_end, "accession": accn, "items": {}}
    for concept in CONCEPTS:
        picked = pick_tag(facts, concept)
        item = {"label": LABELS[concept], "tag": None, "current": None, "prior": None}
        if picked:
            ptag, _, prows = picked
            item["tag"] = ptag
            for key, end in (("current", fy_end), ("prior", prior_end)):
                if end is None:
                    continue
                r = _value_at(prows, end, accn)
                if r:
                    item[key] = {"value": r["val"], "end": r["end"], "start": r.get("start"),
                                 "accn": r["accn"], "form": r["form"], "unit": r["unit"]}
        out["items"][concept] = item
    return out


def check_periods(fx):
    """Lab 02 check: every current period end equals the 10-K's fiscal year end."""
    bad = []
    for c, it in fx["items"].items():
        if it["current"] is None:
            bad.append(f"{c}: no value for {fx['fiscal_year_end']}")
        elif it["current"]["end"] != fx["fiscal_year_end"]:
            bad.append(f"{c}: period end {it['current']['end']} != {fx['fiscal_year_end']}")
    return bad
