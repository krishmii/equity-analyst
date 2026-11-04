# How every number is sourced (shared by all roles; the Verifier parses this)

Write each number, then its source in braces, right after it:

- From the XBRL facts:   `$20.76 {xbrl: EarningsPerShareDiluted 2026-08-30}`
- From a filing line:    `$20.76 {line: 10-K "Diluted $ 20.76 $ 18.21 $ 16.56"}`
  The quoted line is copied word for word from the saved filing text. Document is one of 10-K, 10-Q, Release.
- A ratio:               `28.40% {calc: 9,226 / ((35,803 + 29,164) / 2)}`
  Inputs are numbers already sourced in the report. Name the definition in words beside it
  (e.g. "return on average equity", "margin on total revenue").

Units: write money in millions as `$303,154M`, in billions as `$303.2B`, per-share as `$20.76`,
percentages as `10.14%`, multiples as `43.2x`.
A number with no source is marked unsupported by the Verifier. If the filings do not state it, write "not stated in the filings".
