The Coca-Cola Company (KO, CIK 0000021344) — filings read: 10-K FY2025 0001628280-26-010047 (accepted 2026-02-20 09:46:32); 10-Q Q2 2026 0001628280-26-050503 (accepted 2026-07-29 14:04:37; the latest 10-Q as of the release date); 8-K Item 2.02 earnings release, Exhibit 99.1, 0001628280-26-067403 (accepted 2026-10-27 06:58:13); XBRL company facts
fallback — produced with the four roles' tasks from the Lab 03 request sent to a model in one message, on the filings above. Run time: 2026-11-04 (submitted under an extension).

# The Coca-Cola Company (KO) — Equity Research Report

Partner's pick (Jeenay Dedhia). Peers: PepsiCo (PEP), Keurig Dr Pepper (KDP). Price: $91.18, KO's NYSE close on Tue Oct 27, 2026, the release date. (Note: the release was accepted 06:58 ET, before the open; the last close before it was $92.70 on Oct 26, which gives P/E 30.5x.)

## Overview

*Research Analyst — every claim quotes its line.*

- **What it is.** "The Coca-Cola Company is a total beverage company, and beverage products bearing our trademarks, sold in the United States since 1886, are now sold in more than 200 countries and territories." [10-K, Item 1]
- **Business model.** "Our Company operates in two lines of business: concentrate operations and finished product operations." [10-K, Item 1] Concentrate operations "typically generate net operating revenues by selling beverage concentrates, sometimes referred to as 'beverage bases,' syrups…" to bottlers [10-K, Item 1]. Distribution runs "through our network of independent bottling partners, distributors, wholesalers and retailers as well as our consolidated bottling and distribution operations." [10-K, Item 1]
- **Scale.** "Beverages bearing trademarks owned by or licensed to the Company account for 2.2 billion of the estimated 65 billion servings of all beverages consumed worldwide every day." [10-K, Item 1]
- **The quarter in one line.** "Net revenues grew 7% to $13.4 billion, and organic revenues (non-GAAP) grew 7%, driven by a 7% increase in concentrate sales and 1% growth in price/mix." [Release]

## Market Positioning and Growth Outlook

- **Competition.** "The commercial beverage industry is highly competitive and consists of numerous companies, ranging from small or emerging to very large and well established." [10-K, Item 1, Competition]
- **Share.** "The company gained value share in total nonalcoholic ready-to-drink ('NARTD') beverages." [Release] By region, share was gained in Latin America, North America and Asia Pacific, while in EMEA "The company lost value share in total NARTD beverages, as gains in Nigeria and Morocco were more than offset by losses in France and the United Kingdom." [Release]
- **Volume.** "Unit case volume grew 5%, led by India, China, Mexico and Brazil." [Release] North America was the soft spot: "Unit case volume was even, as growth in Trademark Coca-Cola was offset by a decline in water, sports, coffee and tea." [Release]
- **Brands.** "Trademark Coca-Cola grew 5% and Coca-Cola Zero Sugar grew 16%, both driven by growth across all geographic operating segments." [Release]
- **Timing caveat.** "Concentrate sales were 2 points ahead of unit case volume due to the timing of concentrate shipments." [Release] — part of the quarter's revenue growth is shipment timing, not consumer demand.
- **Guidance.** Full-year 2026 organic revenue (non-GAAP) guidance moved from "Approx. 5% growth" to "At least 5% growth"; comparable EPS (non-GAAP) to "At least 11% growth" from "9% to 10% growth." [Release, Full Year 2026 Guidance] These are non-GAAP and are not used as core claims.

## Valuation Insights

*Financial Analyst — every number from the XBRL facts of 10-K 0001628280-26-010047 (FY ended 2025-12-31, prior year 2024-12-31) or from the release income statement; every ratio computed in code (`desk/calc.py`) and shown with its arithmetic. $ in millions except per share.*

### The eleven core claims

| # | Claim | Value | Arithmetic / definition | Source |
|---|---|---|---|---|
| 1 | Total revenue, FY2025 | $47,941 | "Net operating revenues" = total revenue (KO reports one revenue line) | 10-K income statement; tag `Revenues`, period end 2025-12-31 |
| 2 | Revenue growth vs FY2024 | +1.87% | 47,941 / 47,061 − 1 | 10-K, both years in the same filing; tag `Revenues` |
| 3 | Operating income; operating margin | $13,762; 28.71% | 13,762 / 47,941 (margin on total revenue) | 10-K; tag `OperatingIncomeLoss`, 2025-12-31 |
| 4 | Net income attributable to KO | $13,107 | — | 10-K; tag `NetIncomeLoss`, 2025-12-31 |
| 5 | Diluted EPS (GAAP), FY2025 | $3.04 | — | 10-K per-share section; tag `EarningsPerShareDiluted`, 2025-12-31 |
| 6 | Return on average equity | 45.97% | 13,107 / ((32,169 + 24,856) / 2 = 28,512.5); equity = equity attributable to shareowners of KO, average of two year-ends | 10-K balance sheet; tag `StockholdersEquity` at 2025-12-31 and 2024-12-31 |
| 7 | Debt to equity | 1.37x | (42,119 long-term debt + 1,822 current maturities) / 32,169; excludes the 1,551 of short-term loans and notes payable, per the audit's definition | 10-K balance sheet; tags `LongTermDebtAndCapitalLeaseObligations`, `LongTermDebtAndCapitalLeaseObligationsCurrent`, 2025-12-31 |
| 8 | Free cash flow, FY2025 | $5,296 | 7,408 cash from operations − 2,112 purchases of PP&E | 10-K cash flow; tags `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment` |
| 9 | Q3 2026 revenue | $13,380 | "Net Operating Revenues $ 13,380 $ 12,455 7" | Release, income statement, three months ended Oct 2, 2026 |
| 10 | Q3 growth vs Q3 2025 | +7.43% | 13,380 / 12,455 − 1 | Release, the two columns of the same line |
| 11 | Q3 2026 diluted EPS (GAAP) | $0.93 | "Diluted Net Income Per Share $ 0.93 $ 0.86 8" | Release, per-share section |

**Tag trap, met and handled.** KO stopped reporting `LongTermDebtNoncurrent` and `LongTermDebtCurrent` after FY2023; the desk picks the candidate tag whose latest year is newest (`LongTermDebtAndCapitalLeaseObligations…`). A reader that took the first tag found would have printed FY2023 debt.

### Other numbers

| Item | Value | Arithmetic | Source |
|---|---|---|---|
| P/E (on FY2025 GAAP diluted EPS) | 30.0x | $91.18 / $3.04 | Price: NYSE close Oct 27, 2026; EPS: 10-K |
| FY2024 operating income (context) | $9,992 | — | 10-K; `OperatingIncomeLoss`, 2024-12-31 |
| Q3 2026 operating margin (as reported) | 33.4% | 4,465 / 13,380 | Release: "Operating Income 4,465 3,982 12" |
| 9-month 2026 cash from operations | $12,471 vs $3,652 | — | Release, cash flow statement, nine months |

**Why FY2025 cash flow looks low.** Nine-month 2025 operating cash flow was depressed by working capital ("Net change in operating assets and liabilities (498) (8,040)" [Release]), and the release notes "In March 2025, the company made the remaining milestone payment for fairlife." So FY2025 FCF ($5,296) understates the run-rate; 2026 year-to-date cash from operations is $12,471.

### Peers — operating margin on one definition (operating income ÷ total revenue, each from its own latest 10-K)

| Company | Fiscal year | Revenue | Operating income | Operating margin | Source |
|---|---|---|---|---|---|
| Coca-Cola (KO) | FY ended 2025-12-31 | $47,941 | $13,762 | 28.71% | 10-K 0001628280-26-010047; `Revenues` |
| PepsiCo (PEP) | FY ended 2025-12-27 | $93,925 | $11,498 | 12.24% | 10-K 0000077476-26-000007; `Revenues` |
| Keurig Dr Pepper (KDP) | FY ended 2025-12-31 | $16,603 | $3,575 | 21.53% | 10-K 0001418135-26-000016; `RevenueFromContractWithCustomerExcludingAssessedTax` (KDP's total net sales) |

Definition note: PEP and KDP use different revenue tags; both are each company's total revenue line, so the margins are comparable. PepsiCo's lower margin reflects its large snack and finished-goods distribution business; KO's concentrate model keeps more of each revenue dollar.

## Future Developments and Strategic Recommendations

*Investment Advisor — from the two analysts' outputs only.*

- **Portfolio reshaping.** The guidance notes assume "the pending sale of our bottling operations in Africa closes during the fourth quarter of 2026," and flag an "Approx. 8% headwind from acquisitions and divestitures" to 2027 comparable net revenues [Release]. Refranchising lowers reported revenue but should lift margins further toward the concentrate model.
- **Watch items.** (1) Concentrate shipments ran 2 points ahead of volume in Q3 — expect some give-back. (2) North America volume was flat. (3) The guidance excludes "the impact of ongoing tax litigation with the U.S. Internal Revenue Service, if the company were not to prevail" [Release].
- **Strategic recommendation.** Keep pushing Zero Sugar (+16%) and emerging-market volume (India, China, Mexico, Brazil), where growth is coming from; keep North America pricing disciplined given flat volume.

## Investment Recommendation

**Recommendation: Hold**

**Deciding number: P/E of 30.0x** ($91.18 / $3.04 FY2025 GAAP diluted EPS, claim 5).

Thesis: KO is a high-quality compounder — a 28.71% operating margin, more than double PepsiCo's 12.24% and above KDP's 21.53%, and a 45.97% return on average equity. The quarter was strong (revenue +7.43%, GAAP diluted EPS $0.93 vs $0.86). But full-year FY2025 revenue grew only 1.87%, part of Q3's growth is shipment timing, and 2027 reported revenue faces divestiture headwinds. At 30.0x trailing GAAP earnings, that quality is already priced in; the stock is a hold, not a buy, at $91.18.

---

This is a learning exercise, not financial advice.

AI assistance: Claude (Anthropic), used in Claude in Chrome and Cowork to build the desk code and draft this fallback report. I verified the sources myself; the judgments are mine.

Any remaining errors are my own.
