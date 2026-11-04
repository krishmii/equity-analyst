"""Steps 1-3: ticker -> CIK -> filings -> plain-text documents.

Nothing in this file names a company. The ticker is always an argument.
"""
import os
import re
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_nodash}/"

_session = None


def _headers():
    ua = os.getenv("SEC_USER_AGENT")
    if not ua:
        raise SystemExit("SEC_USER_AGENT is missing from .env (format: 'Your Name your@email.edu').")
    return {"User-Agent": ua, "Accept-Encoding": "gzip, deflate"}


def get(url, as_json=False):
    """GET with the SEC User-Agent, a polite pause (SEC allows 10 requests/second) and one retry."""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(_headers())
    for attempt in range(3):
        time.sleep(0.15)
        r = _session.get(url, timeout=60)
        if r.status_code == 200:
            return r.json() if as_json else r.text
        if r.status_code in (403, 429, 503):
            time.sleep(2 * (attempt + 1))
            continue
        r.raise_for_status()
    r.raise_for_status()


# ---------- Step 1 ----------
def resolve_cik(ticker):
    data = get(TICKERS_URL, as_json=True)
    t = ticker.upper().replace(".", "-")
    for row in data.values():
        if row["ticker"].upper() == t:
            return str(row["cik_str"]).zfill(10), row["title"]
    raise SystemExit(f"Ticker {ticker} not found in SEC company_tickers.json")


# ---------- Step 2 ----------
def _accepted_time(cik_int, acc):
    """Read the 'Accepted' time from the filing's EDGAR index page."""
    acc_nodash = acc.replace("-", "")
    url = ARCHIVE_URL.format(cik_int=cik_int, acc_nodash=acc_nodash) + f"{acc}-index.html"
    html = get(url)
    m = re.search(r"Accepted</div>\s*<div class=\"info\">([^<]+)</div>", html)
    return (m.group(1).strip() if m else "not found"), url


def list_filings(cik):
    """Latest 10-K, latest 10-Q and the latest 8-K that reports Item 2.02."""
    sub = get(SUBMISSIONS_URL.format(cik=cik), as_json=True)
    r = sub["filings"]["recent"]
    picks = {}
    for i, form in enumerate(r["form"]):
        items = r.get("items", [""] * len(r["form"]))[i] or ""
        rec = {
            "form": form,
            "accession": r["accessionNumber"][i],
            "filing_date": r["filingDate"][i],
            "report_date": r["reportDate"][i],
            "primary_document": r["primaryDocument"][i],
            "items": items,
        }
        if form == "10-K" and "10-K" not in picks:
            picks["10-K"] = rec
        elif form == "10-Q" and "10-Q" not in picks:
            picks["10-Q"] = rec
        elif form == "8-K" and "8-K" not in picks:
            # The newest 8-K is often NOT the earnings release: require Item 2.02.
            if "2.02" in items.split(","):
                picks["8-K"] = rec
        if len(picks) == 3:
            break
    cik_int = int(cik)
    for rec in picks.values():
        rec["accepted"], rec["index_url"] = _accepted_time(cik_int, rec["accession"])
    return sub, picks


# ---------- Step 3 ----------
def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def _exhibit_99_1(cik_int, acc):
    """Find the document whose type is EX-99.1 on the filing index (file names vary)."""
    acc_nodash = acc.replace("-", "")
    base = ARCHIVE_URL.format(cik_int=cik_int, acc_nodash=acc_nodash)
    html = get(base + f"{acc}-index.html")
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.select("table.tableFile tr"):
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cells) >= 4 and cells[3].upper().startswith("EX-99.1"):
            a = row.find("a")
            if a and a.get("href"):
                href = a["href"]
                if href.startswith("/ix?doc="):
                    href = href[len("/ix?doc="):]
                return "https://www.sec.gov" + href if href.startswith("/") else base + href
    raise SystemExit(f"No EX-99.1 found in {acc}")


def download_documents(cik, company, picks, out_root="runs"):
    cik_int = int(cik)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    slug = re.sub(r"[^A-Za-z0-9]+", "_", company).strip("_")
    folder = os.path.join(out_root, f"{slug}_{stamp}")
    os.makedirs(folder, exist_ok=True)
    saved = {}
    for form, rec in picks.items():
        if form == "8-K":
            url = _exhibit_99_1(cik_int, rec["accession"])
            name = "earnings_release_ex99_1.txt"
        else:
            url = ARCHIVE_URL.format(cik_int=cik_int, acc_nodash=rec["accession"].replace("-", "")) + rec["primary_document"]
            name = f"{form.replace('-', '').lower()}.txt"
        text = html_to_text(get(url))
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"SOURCE: {url}\nACCESSION: {rec['accession']}\n\n{text}")
        rec["document_url"] = url
        saved[form] = path
    return folder, saved


def company_facts(cik):
    return get(FACTS_URL.format(cik=cik), as_json=True)
