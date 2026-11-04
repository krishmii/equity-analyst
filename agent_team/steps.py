"""The steps node: Lab 02's seven steps, in code, no model. Saves everything it read."""
import os

from desk import calc, edgar, facts, release
from agent_team.runfolder import save_json


def xbrl_index(cf):
    """Every annual 10-K value of every candidate tag: {tag: {period_end: value}}.
    The Verifier compares XBRL-sourced numbers against this, exactly."""
    out = {}
    for concept, tags in facts.CONCEPTS.items():
        for tag in tags:
            rows = facts._annual_rows(cf, tag, concept in facts.INSTANT)
            if rows:
                d = out.setdefault(tag, {})
                for r in sorted(rows, key=lambda r: r.get("filed", "")):
                    d[r["end"]] = r["val"]
    return out


def run_steps(ticker, peers, price):
    print("[node] steps")
    cik, company = edgar.resolve_cik(ticker)
    _, picks = edgar.list_filings(cik)
    folder, saved = edgar.download_documents(cik, company, picks, out_root="runs")
    # rename the 10-K/10-Q/8-K files to the names the Verifier reads
    names = {"10-K": "10k.txt", "10-Q": "10q.txt", "8-K": "earnings_release_ex99_1.txt"}
    for form, path in saved.items():
        new = os.path.join(folder, names[form])
        if path != new:
            os.replace(path, new)
    cf = edgar.company_facts(cik)
    fx = facts.read_facts(cf, picks["10-K"]["accession"])
    rt = calc.ratios(fx, price)
    with open(os.path.join(folder, "earnings_release_ex99_1.txt"), encoding="utf-8") as f:
        q = release.quarter_lines(f.read())
    peer_out = []
    for p in peers:
        pcik, pname = edgar.resolve_cik(p)
        pfx = facts.read_facts(edgar.company_facts(pcik))
        rev, oi = pfx["items"]["total_revenue"], pfx["items"]["operating_income"]
        row = {"ticker": p, "name": pname, "fiscal_year_end": pfx["fiscal_year_end"], "accession": pfx["accession"],
               "revenue": rev["current"], "revenue_tag": rev["tag"], "operating_income": oi["current"]}
        if rev["current"] and oi["current"]:
            row["operating_margin"] = calc.operating_margin(rev["current"]["value"], oi["current"]["value"])
        peer_out.append(row)
    filings_line = "; ".join(f"{f} {r['accession']}" for f, r in picks.items())
    data = {"ticker": ticker.upper(), "cik": cik, "company": company, "price": price,
            "filings": picks, "filings_line": f"Filings read: {company} ({ticker.upper()}) — {filings_line}",
            "facts": fx, "ratios": rt, "quarter": q, "peers": peer_out, "xbrl_index": xbrl_index(cf)}
    save_json(folder, "facts.json", data)
    return folder, data
