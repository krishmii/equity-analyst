# Checkpoint 2 — the verifier's marks on the seeded-error test

Agent team: `agent_team/` (LangGraph). Graph, fixed in code, the same on every run:
`steps → research_analyst → financial_analyst → investment_advisor → strategy_manager → verifier`.
The verifier is the last node on every run; no option removes it (`tests/test_agent_team.py` checks this).

Base run: `runs/COSTCO_WHOLESALE_CORP_NEW_2026-11-04_fallback` (COST, peers WMT, TGT, BJ, price $896.48 = Nasdaq close Sep 24, 2026, the last close before the release).
Note: this run's steps output was assembled from EDGAR through the browser and its report is a fallback, because the build environment could not reach EDGAR or a model API. The Verifier itself ran in code on it. The model half of the Verifier records "not run (no API_KEY)"; it runs when API_KEY is set in `.env`.

Command: `python tools/seed_tests.py runs/COSTCO_WHOLESALE_CORP_NEW_2026-11-04_fallback`
(each test verifies a copy with the same code path as `python run_team.py --verify-only <folder>`).

## Test 1 — seeded EPS (the checkpoint's known answer)

Copy: `runs/COSTCO_WHOLESALE_CORP_NEW_2026-11-04_fallback_seeded_eps` — diluted EPS changed from $20.76 to $21.76, its source line changed to match.

Verifier's mark (from `verified_report.md` in that folder):

| # | Part | Report said | Source | Code check | Mark | Correction / real line |
|---|---|---|---|---|---|---|
| 9 | Valuation Insights | $21.76 | line: 10-K "Diluted $ 21.76 $ 18.21 $ 16.56" | quoted line is not in 10-K; real line: "Diluted $ 20.76 $ 18.21 $ 16.56" | **wrong** | $20.76 {line: 10-K "Diluted $ 20.76 $ 18.21 $ 16.56"} |

Expected: marked wrong and corrected to the 10-K's figure ($20.76), with the 10-K's per-share line beside it. **Met.**
All other 28 numbers in the copy: correct.

Partner check of test 1 against the 10-K (per-share section, p. 37): ____

## Test 2 — invented number

Copy: `..._invented_growth` — added "Revenue grew 14.14%", four points above what the 10-K's two revenue figures give, with both figures quoted.
Mark: **wrong**, recomputed 303,154 / 275,235 − 1 = 10.14%. **Met.**

## Test 3 — clean report

The base run verified as it is: 29 correct, 0 wrong, 0 unsupported. No correct number flagged. **Met.**

## Test 4 — skip test

`agent_team/graph.py` uses only fixed edges (no conditional routing) and `run_team.py` has no option that skips the verifier. `python -m pytest -q` passes.
