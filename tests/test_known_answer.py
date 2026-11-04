"""Known-answer tests. A test may name a company; the desk's code may not.

Fixture: a slice of The Coca-Cola Company's XBRL company facts (CIK 0000021344),
FY2025 10-K, accession 0001628280-26-010047, plus older filings that exercise the
tag trap (LongTermDebtNoncurrent stops in FY2023; the filer moved to
LongTermDebtAndCapitalLeaseObligations).
"""
from desk import calc, facts, release

K25 = "0001628280-26-010047"
K24 = "0000021344-25-000011"
K23 = "0000021344-24-000009"


def dur(start, end, val, accn, form="10-K"):
    return {"start": start, "end": end, "val": val, "accn": accn, "form": form, "filed": accn}


def inst(end, val, accn, form="10-K"):
    return {"end": end, "val": val, "accn": accn, "form": form, "filed": accn}


def usd(*rows):
    return {"units": {"USD": list(rows)}}


FIXTURE = {"facts": {"us-gaap": {
    "Revenues": usd(dur("2024-01-01", "2024-12-31", 47061e6, K25), dur("2025-01-01", "2025-12-31", 47941e6, K25),
                    dur("2023-01-01", "2023-12-31", 45754e6, K24)),
    "OperatingIncomeLoss": usd(dur("2024-01-01", "2024-12-31", 9992e6, K25), dur("2025-01-01", "2025-12-31", 13762e6, K25)),
    "NetIncomeLoss": usd(dur("2024-01-01", "2024-12-31", 10631e6, K25), dur("2025-01-01", "2025-12-31", 13107e6, K25)),
    "EarningsPerShareDiluted": {"units": {"USD/shares": [dur("2024-01-01", "2024-12-31", 2.46, K25),
                                                          dur("2025-01-01", "2025-12-31", 3.04, K25),
                                                          dur("2025-07-01", "2025-09-26", 0.86, "q", "10-Q")]}},
    "StockholdersEquity": usd(inst("2024-12-31", 24856e6, K25), inst("2025-12-31", 32169e6, K25)),
    "LongTermDebtNoncurrent": usd(inst("2023-12-31", 35547e6, K23)),
    "LongTermDebtAndCapitalLeaseObligations": usd(inst("2024-12-31", 42375e6, K25), inst("2025-12-31", 42119e6, K25)),
    "LongTermDebtCurrent": usd(inst("2023-12-31", 1960e6, K23)),
    "LongTermDebtAndCapitalLeaseObligationsCurrent": usd(inst("2024-12-31", 648e6, K25), inst("2025-12-31", 1822e6, K25)),
    "NetCashProvidedByUsedInOperatingActivities": usd(dur("2024-01-01", "2024-12-31", 6805e6, K25), dur("2025-01-01", "2025-12-31", 7408e6, K25)),
    "PaymentsToAcquirePropertyPlantAndEquipment": usd(dur("2024-01-01", "2024-12-31", 2064e6, K25), dur("2025-01-01", "2025-12-31", 2112e6, K25)),
}}}


def test_tag_trap_and_periods():
    fx = facts.read_facts(FIXTURE, K25)
    assert fx["fiscal_year_end"] == "2025-12-31"
    assert fx["items"]["long_term_debt_noncurrent"]["tag"] == "LongTermDebtAndCapitalLeaseObligations"
    assert facts.check_periods(fx) == []


def test_core_ratios():
    fx = facts.read_facts(FIXTURE, K25)
    r = calc.ratios(fx, price=92.70)
    assert round(r["revenue_growth"]["value"], 4) == 0.0187
    assert round(r["operating_margin"]["value"], 4) == 0.2871
    assert round(r["return_on_average_equity"]["value"], 4) == 0.4597
    assert round(r["debt_to_equity"]["value"], 3) == 1.366
    assert r["free_cash_flow"]["value"] == 5296e6
    assert round(r["pe"]["value"], 1) == 30.5


def test_release_lines():
    text = """Net Operating Revenues $ 13,380 $ 12,455 7
Comparable EPS (Non-GAAP) Grew 11% to $0.91
Diluted Net Income Per Share1
$ 0.93 $ 0.86 8"""
    q = release.quarter_lines(text)
    assert q["revenue_lines"][0].startswith("Net Operating Revenues $ 13,380")
    assert "0.93" in q["eps_lines"][0]
