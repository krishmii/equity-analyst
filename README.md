# Equity Analyst — FIN 67110 research desk

An AI equity-research desk following the four-role system of Francis & Zhang (2026), *Finance Research Letters* 103, 110127. A ticker in, a five-part report out. Nothing in the desk's code names a company; tests may.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # then fill in SEC_USER_AGENT, PROVIDER, API_KEY
python check_env.py         # prints your User-Agent and the first 4 characters of your key
```

`.env` is in `.gitignore`. Check on github.com that it was never pushed.

## Run

```bash
# the seven steps only (Lab 02, no model key)
python run_desk.py KO --peers PEP,KDP --price 91.18 --no-model

# the full desk: seven steps + four roles -> report.md (Lab 03)
python run_desk.py KO --peers PEP,KDP --price 91.18

# one step only
python run_desk.py COST --step 4

# known-answer tests
python -m pytest -q
```

Each run saves to `runs/<Company>_<date_time>/`: the 10-K, 10-Q and Exhibit 99.1 as text, `facts.json`, and `report.md`.

## The seven steps (`desk/`)

1. Ticker → CIK (`company_tickers.json`)
2. Latest 10-K, 10-Q, and the latest 8-K that reports **Item 2.02** (with accession number and "Accepted" time)
3. Download the documents (8-K → Exhibit 99.1) as plain text
4. XBRL company facts for the latest fiscal year, prior year beside it; among candidate tags, the one whose latest year is newest
5. Calculator in code: revenue growth, operating margin, return on average equity, debt/equity (current portion included), FCF, P/E
6. The quarter's revenue and GAAP diluted EPS lines, word for word from the release
7. Peers: the same facts, operating margin on the same definition

## The four roles (`desk/roles.py`)

Strategy Manager (checklist in code) → Research Analyst, Financial Analyst, Investment Advisor (one model call each, JSON hand-off). The Manager checks the five parts, sends a failing part back once, then compiles.

## Reports

- `reports/KO_fallback_report.md` — Checkpoint 1, partner's pick (Coca-Cola), fallback report
- `reports/KO_audit.md` — the hand audit (marks filled by hand)

---

This is a learning exercise, not financial advice.

AI assistance: [the tools you used]. I verified the sources myself; the judgments are mine.

Any remaining errors are my own.
