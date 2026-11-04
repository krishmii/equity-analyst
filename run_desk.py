"""The desk: a ticker in, a five-part report out.

    python run_desk.py TICKER --peers PEER1,PEER2 --price P
    python run_desk.py TICKER --peers PEER1,PEER2 --price P --no-model   # steps only (Lab 02)
    python run_desk.py TICKER --step 4                                   # one step only

Nothing in this code names a company; the ticker is an argument.
"""
import argparse
import json
import os
from datetime import datetime

from desk import calc, edgar, facts, release


def fmt(rec, unit=""):
    if rec is None:
        return "n/a"
    v = rec["value"]
    s = f"{v:,.2f}" if abs(v) < 1000 else f"{v / 1e6:,.0f}M"
    return f"{s}{unit}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--peers", default="", help="comma-separated tickers")
    ap.add_argument("--price", type=float, default=None, help="last close before the release")
    ap.add_argument("--step", type=int, default=None, help="run steps 1..N only")
    ap.add_argument("--no-model", action="store_true", help="run the seven steps without the four roles")
    a = ap.parse_args()
    last = a.step or 7
    peers = [p.strip().upper() for p in a.peers.split(",") if p.strip()]

    # 1
    print("== Step 1: ticker -> CIK")
    cik, company = edgar.resolve_cik(a.ticker)
    print(f"   {a.ticker.upper()} -> CIK {cik} ({company})")
    if last < 2:
        return

    # 2
    print("== Step 2: latest 10-K, 10-Q and earnings 8-K (Item 2.02)")
    _, picks = edgar.list_filings(cik)
    for form, rec in picks.items():
        print(f"   {form}: {rec['accession']}  accepted {rec['accepted']}  (period {rec['report_date']}, items {rec['items'] or '-'})")
    if last < 3:
        return

    # 3
    print("== Step 3: download and save as text")
    folder, saved = edgar.download_documents(cik, company, picks)
    for form, path in saved.items():
        print(f"   {form} -> {path}")
    texts = {f: open(p, encoding="utf-8").read() for f, p in saved.items()}
    if last < 4:
        return

    # 4
    print("== Step 4: XBRL facts, latest fiscal year (prior year beside it)")
    cf = edgar.company_facts(cik)
    fx = facts.read_facts(cf, picks["10-K"]["accession"])
    print(f"   fiscal year end {fx['fiscal_year_end']} (10-K period {picks['10-K']['report_date']}); prior {fx['prior_year_end']}")
    for c, it in fx["items"].items():
        cur = it["current"]
        print(f"   {it['label']:<42} {fmt(cur):>12}  prior {fmt(it['prior']):>12}  tag {it['tag']}  end {cur and cur['end']}  accn {cur and cur['accn']}")
    bad = facts.check_periods(fx)
    if fx["fiscal_year_end"] != picks["10-K"]["report_date"]:
        bad.append(f"revenue year {fx['fiscal_year_end']} != 10-K period {picks['10-K']['report_date']} (tag trap?)")
    for b in bad:
        print(f"   CHECK FAILED: {b}")
    if last < 5:
        return

    # 5
    print("== Step 5: calculator")
    rt = calc.ratios(fx, a.price)
    for k, r in rt.items():
        print(f"   {k:<26} {r['arithmetic']}")
    if last < 6:
        return

    # 6
    print("== Step 6: the quarter, from the release (word for word)")
    q = release.quarter_lines(texts.get("8-K", ""))
    for ln in q["revenue_lines"]:
        print(f"   revenue: {ln}")
    for ln in q["eps_lines"]:
        print(f"   EPS:     {ln}")
    if last < 7:
        return

    # 7
    print("== Step 7: peers, same definition")
    peer_out = []
    for p in peers:
        pcik, pname = edgar.resolve_cik(p)
        pfx = facts.read_facts(edgar.company_facts(pcik))
        rev, oi = pfx["items"]["total_revenue"], pfx["items"]["operating_income"]
        row = {"ticker": p, "name": pname, "fiscal_year_end": pfx["fiscal_year_end"],
               "revenue": rev["current"], "revenue_tag": rev["tag"],
               "operating_income": oi["current"], "accession": pfx["accession"]}
        if rev["current"] and oi["current"]:
            row["operating_margin"] = calc.operating_margin(rev["current"]["value"], oi["current"]["value"])
            print(f"   {p} FY{pfx['fiscal_year_end']}: {row['operating_margin']['arithmetic']}  (tag {rev['tag']}, accn {pfx['accession']})")
        peer_out.append(row)

    with open(os.path.join(folder, "facts.json"), "w") as f:
        json.dump({"ticker": a.ticker.upper(), "cik": cik, "company": company, "filings": picks,
                   "facts": fx, "ratios": rt, "quarter": q, "peers": peer_out, "price": a.price}, f, indent=2, default=str)
    print(f"   saved {os.path.join(folder, 'facts.json')}")
    if a.no_model:
        return

    # the four roles
    from desk.roles import run_roles
    body, problems = run_roles(company, a.ticker.upper(), texts, fx, rt, q, peer_out, a.price)
    filings_line = "; ".join(f"{f} {r['accession']}" for f, r in picks.items())
    head = (f"Filings read: {company} ({a.ticker.upper()}) — {filings_line}\n"
            f"Run time: {datetime.now().isoformat(timespec='seconds')}\n\n")
    if problems:
        head += "> Strategy Manager flags: " + "; ".join(problems) + "\n\n"
    foot = ("\n\n---\nThis is a learning exercise, not financial advice.\n\n"
            "AI assistance: [the tools you used]. I verified the sources myself; the judgments are mine.\n\n"
            "Any remaining errors are my own.\n")
    path = os.path.join(folder, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + f"# {company} ({a.ticker.upper()}) — Equity Research Report\n\n" + body + foot)
    print(f"REPORT: {path}")


if __name__ == "__main__":
    main()
