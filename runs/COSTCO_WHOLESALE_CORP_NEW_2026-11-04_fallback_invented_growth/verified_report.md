Filings read: COSTCO WHOLESALE CORP /NEW (COST) — 10-K 0000909832-26-000093; 10-Q 0000909832-26-000051; 8-K 0000909832-26-000084 (Ex. 99.1)

## Verifier marks

Correct: 31 · Wrong: 1 · Unsupported: 0 · Skipped: the Investment Recommendation (thesis)

| # | Part | Report said | Source | Code check | Model check | Mark | Correction / real line |
|---|---|---|---|---|---|---|---|
| 1 | Overview | $5,907M | line: 10-K "Membership fees 5,907 5,323 4,828" | line found in 10-K | not run (no API_KEY in .env) | **correct** |  |
| 2 | Overview | $303,154M | xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 | facts: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 = 303,154,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 3 | Market Positioning and Growth Outlook | 20.9% | line: Release "Digitally-Enabled 19.5% 19.8% 20.9% 20.7%" | line found in Release | not run (no API_KEY in .env) | **correct** |  |
| 4 | Valuation Insights | 14.14% | calc: 303,154 / 275,235 - 1 | recomputed 303,154 / 275,235 - 1 = 10.14% | not run (no API_KEY in .env) | **wrong** | 10.14% {calc: 303,154 / 275,235 - 1} |
| 5 | Valuation Insights | $275,235M | xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2025-08-31 | facts: RevenueFromContractWithCustomerExcludingAssessedTax 2025-08-31 = 275,235,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 6 | Valuation Insights | $303,154M | xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 | facts: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 = 303,154,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 7 | Valuation Insights | $303,154M | xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 | facts: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30 = 303,154,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 8 | Valuation Insights | 10.14% | calc: 303,154 / 275,235 - 1 | recomputed 303,154 / 275,235 - 1 = 10.14% | not run (no API_KEY in .env) | **correct** |  |
| 9 | Valuation Insights | $11,685M | xbrl: OperatingIncomeLoss 2026-08-30 | facts: OperatingIncomeLoss 2026-08-30 = 11,685,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 10 | Valuation Insights | 3.85% | calc: 11,685 / 303,154 | recomputed 11,685 / 303,154 = 3.85% | not run (no API_KEY in .env) | **correct** |  |
| 11 | Valuation Insights | $9,226M | line: 10-K "NET INCOME $ 9,226 $ 8,099 $ 7,367" | line found in 10-K | not run (no API_KEY in .env) | **correct** |  |
| 12 | Valuation Insights | $20.76 | line: 10-K "Diluted $ 20.76 $ 18.21 $ 16.56" | line found in 10-K | not run (no API_KEY in .env) | **correct** |  |
| 13 | Valuation Insights | 28.40% | calc: 9,226 / ((35,803 + 29,164) / 2) | recomputed 9,226 / ((35,803 + 29,164) / 2) = 28.40% | not run (no API_KEY in .env) | **correct** |  |
| 14 | Valuation Insights | 0.17x | calc: (3,914 + 2,248) / 35,803 | recomputed (3,914 + 2,248) / 35,803 = 0.17x | not run (no API_KEY in .env) | **correct** |  |
| 15 | Valuation Insights | $9,382M | calc: 15,817 - 6,435 | recomputed 15,817 - 6,435 = $9,382M | not run (no API_KEY in .env) | **correct** |  |
| 16 | Valuation Insights | $95,723M | line: Release "Total revenue 95,723 86,156 303,154 275,235" | line found in Release | not run (no API_KEY in .env) | **correct** |  |
| 17 | Valuation Insights | 11.10% | calc: 95,723 / 86,156 - 1 | recomputed 95,723 / 86,156 - 1 = 11.10% | not run (no API_KEY in .env) | **correct** |  |
| 18 | Valuation Insights | $6.75 | line: Release "Diluted $ 6.75 $ 5.87 $ 20.76 $ 18.21" | line found in Release | not run (no API_KEY in .env) | **correct** |  |
| 19 | Valuation Insights | $35,803M | xbrl: StockholdersEquity 2026-08-30 | facts: StockholdersEquity 2026-08-30 = 35,803,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 20 | Valuation Insights | $29,164M | xbrl: StockholdersEquity 2025-08-31 | facts: StockholdersEquity 2025-08-31 = 29,164,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 21 | Valuation Insights | $3,914M | xbrl: LongTermDebtNoncurrent 2026-08-30 | facts: LongTermDebtNoncurrent 2026-08-30 = 3,914,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 22 | Valuation Insights | $2,248M | xbrl: LongTermDebtCurrent 2026-08-30 | facts: LongTermDebtCurrent 2026-08-30 = 2,248,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 23 | Valuation Insights | $15,817M | xbrl: NetCashProvidedByUsedInOperatingActivities 2026-08-30 | facts: NetCashProvidedByUsedInOperatingActivities 2026-08-30 = 15,817,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 24 | Valuation Insights | $6,435M | xbrl: PaymentsToAcquirePropertyPlantAndEquipment 2026-08-30 | facts: PaymentsToAcquirePropertyPlantAndEquipment 2026-08-30 = 6,435,000,000 | not run (no API_KEY in .env) | **correct** |  |
| 25 | Valuation Insights | 11.09% | calc: (297,247 - 264,279) / 297,247 | recomputed (297,247 - 264,279) / 297,247 = 11.09% | not run (no API_KEY in .env) | **correct** |  |
| 26 | Valuation Insights | 12.82% | calc: (303,154 - 264,279) / 303,154 | recomputed (303,154 - 264,279) / 303,154 = 12.82% | not run (no API_KEY in .env) | **correct** |  |
| 27 | Valuation Insights | $15,825M | line: Release "Net cash provided by operating activities 15,825 13,335" | line found in Release | not run (no API_KEY in .env) | **correct** |  |
| 28 | Valuation Insights | 43.2x | calc: 896.48 / 20.76 | recomputed 896.48 / 20.76 = 43.2x | not run (no API_KEY in .env) | **correct** |  |
| 29 | Valuation Insights | 4.18% | calc: 29,825 / 713,163 | recomputed 29,825 / 713,163 = 4.18% | not run (no API_KEY in .env) | **correct** |  |
| 30 | Valuation Insights | 4.88% | calc: 5,117 / 104,780 | recomputed 5,117 / 104,780 = 4.88% | not run (no API_KEY in .env) | **correct** |  |
| 31 | Valuation Insights | 3.81% | calc: 816.604 / 21,457.274 | recomputed 816.604 / 21,457.274 = 3.81% | not run (no API_KEY in .env) | **correct** |  |
| 32 | Future Developments and Strategic Recommendations | 20.9% | line: Release "Digitally-Enabled 19.5% 19.8% 20.9% 20.7%" | line found in Release | not run (no API_KEY in .env) | **correct** |  |

---
fallback — the four roles' tasks answered in one message on this run's saved facts and texts (no model API in this environment). Run time: 2026-11-04.

# COSTCO WHOLESALE CORP /NEW (COST) — Equity Research Report

Price: $896.48, Nasdaq close on Sep 24, 2026, the last close before the release (accepted 16:17:37 ET, after the close). Peers: Walmart (WMT), Target (TGT), BJ's Wholesale (BJ).

## Overview

Costco runs membership warehouses on "the concept that offering members low prices on a limited selection of nationally-branded and private-label products in a wide range of merchandise categories will produce high sales volumes and rapid inventory turnover." [10-K, Note 1] It "operated 939 warehouses worldwide" at fiscal year end [10-K, Note 1]. Revenue has two lines: net sales and membership fees; membership fees were $5,907M {line: 10-K "Membership fees 5,907 5,323 4,828"} of $303,154M {xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30} total revenue.

## Market Positioning and Growth Outlook

"Net sales for the fiscal year increased 10.1 percent, to $297.2 billion, from $269.9 billion last year." [Release] Total company comparable sales were 8.4% for the year, 6.6% adjusted for gasoline and FX {line: Release "Total Company 9.4% 6.7% 8.4% 6.6%"}; digitally-enabled comparable sales grew 20.9% {line: Release "Digitally-Enabled 19.5% 19.8% 20.9% 20.7%"}. The fourth quarter included "a non-recurring benefit of $0.15 per diluted share from IEEPA tariff refunds received in the quarter" [Release].

## Valuation Insights


Revenue grew ~~14.14%~~ **10.14% {calc: 303,154 / 275,235 - 1}** [verifier: wrong], from $275,235M {xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2025-08-31} to $303,154M {xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30}.
All money in millions except per share. Revenue is **total revenue** (net sales + membership fees); margins are on total revenue; return on equity uses **average** equity; debt includes the current portion.

| # | Core claim | Value |
|---|---|---|
| 1 | Total revenue, FY2026 | $303,154M {xbrl: RevenueFromContractWithCustomerExcludingAssessedTax 2026-08-30} |
| 2 | Revenue growth vs FY2025 | 10.14% {calc: 303,154 / 275,235 - 1} |
| 3 | Operating income | $11,685M {xbrl: OperatingIncomeLoss 2026-08-30} |
| 3 | Operating margin on total revenue | 3.85% {calc: 11,685 / 303,154} |
| 4 | Net income | $9,226M {line: 10-K "NET INCOME $ 9,226 $ 8,099 $ 7,367"} |
| 5 | Diluted EPS, GAAP | $20.76 {line: 10-K "Diluted $ 20.76 $ 18.21 $ 16.56"} |
| 6 | Return on average equity | 28.40% {calc: 9,226 / ((35,803 + 29,164) / 2)} |
| 7 | Debt to equity, current portion included | 0.17x {calc: (3,914 + 2,248) / 35,803} |
| 8 | Free cash flow | $9,382M {calc: 15,817 - 6,435} |
| 9 | Q4 FY2026 total revenue (16 weeks) | $95,723M {line: Release "Total revenue 95,723 86,156 303,154 275,235"} |
| 10 | Q4 growth vs Q4 FY2025 | 11.10% {calc: 95,723 / 86,156 - 1} |
| 11 | Q4 diluted EPS, GAAP | $6.75 {line: Release "Diluted $ 6.75 $ 5.87 $ 20.76 $ 18.21"} |

Inputs: equity $35,803M {xbrl: StockholdersEquity 2026-08-30} and $29,164M {xbrl: StockholdersEquity 2025-08-31}; long-term debt $3,914M {xbrl: LongTermDebtNoncurrent 2026-08-30} and current portion $2,248M {xbrl: LongTermDebtCurrent 2026-08-30}; cash from operations $15,817M {xbrl: NetCashProvidedByUsedInOperatingActivities 2026-08-30}; additions to property and equipment $6,435M {xbrl: PaymentsToAcquirePropertyPlantAndEquipment 2026-08-30}.

Definition traps: gross margin on net sales is 11.09% {calc: (297,247 - 264,279) / 297,247}, on total revenue 12.82% {calc: (303,154 - 264,279) / 303,154}; Costco's own definition is on net sales. The release's cash flow statement is "Subject to Reclassification" and shows $15,825M {line: Release "Net cash provided by operating activities 15,825 13,335"} — the 10-K's audited figure is used above.

**Valuation.** P/E is 43.2x {calc: 896.48 / 20.76} on FY2026 GAAP diluted EPS.

**Peers — operating margin on total revenue, each from its own latest 10-K (fiscal years differ):**

| Peer | Fiscal year end | Operating margin |
|---|---|---|
| Walmart | 2026-01-31 | 4.18% {calc: 29,825 / 713,163} |
| Target | 2026-01-31 | 4.88% {calc: 5,117 / 104,780} |
| BJ's Wholesale | 2026-01-31 | 3.81% {calc: 816.604 / 21,457.274} |

## Future Developments and Strategic Recommendations

Growth is coming from traffic and digital (digitally-enabled comparable sales 20.9% {line: Release "Digitally-Enabled 19.5% 19.8% 20.9% 20.7%"}). The Q4 tariff-refund benefit will not repeat. Keep reinvesting in member value; watch whether adjusted comparable sales hold near 6.6%.

## Investment Recommendation

Recommendation: Hold
Deciding number: P/E of 43.2x (896.48 / 20.76)
Thesis: a high-quality, steadily growing compounder (revenue +10.14%, return on average equity 28.40%), but at 43.2x trailing earnings the quality is priced in.

---
This is a learning exercise, not financial advice.

AI assistance: Claude (Anthropic), used in Claude in Chrome and Cowork to build the desk code and draft this fallback report. I verified the sources myself; the judgments are mine.

Any remaining errors are my own.
