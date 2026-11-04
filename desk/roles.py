"""The four roles of Francis & Zhang (2026), Figure 1, on top of the seven steps.

- Strategy Manager: a checklist in code. Sends each role a JSON task
  {task, context, expected_output}, checks the five parts, sends a failing
  part back to its role ONCE, then compiles the report.
- Research Analyst, Financial Analyst, Investment Advisor: one model call each,
  each with its own instructions, each seeing only what the Manager sends it.

Provider is chosen in .env: PROVIDER=openai | anthropic | google, key in API_KEY,
optional MODEL. Nothing here names a company.
"""
import json
import os

from dotenv import load_dotenv

load_dotenv()

PARTS = [
    "Overview",
    "Market Positioning and Growth Outlook",
    "Valuation Insights",
    "Future Developments and Strategic Recommendations",
    "Investment Recommendation",
]

DEFAULT_MODELS = {"openai": "gpt-4.1", "anthropic": "claude-sonnet-4-5", "google": "gemini-2.5-pro"}


# ---------------- model call ----------------
def call_model(system, user):
    provider = os.getenv("PROVIDER", "openai").lower()
    key = os.getenv("API_KEY")
    if not key:
        raise SystemExit("API_KEY is missing from .env")
    model = os.getenv("MODEL") or DEFAULT_MODELS[provider]
    if provider == "openai":
        from openai import OpenAI
        r = OpenAI(api_key=key).chat.completions.create(
            model=model, temperature=0.2,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content
    if provider == "anthropic":
        import anthropic
        r = anthropic.Anthropic(api_key=key).messages.create(
            model=model, max_tokens=4000, temperature=0.2, system=system,
            messages=[{"role": "user", "content": user}])
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    if provider == "google":
        from google import genai
        from google.genai import types
        r = genai.Client(api_key=key).models.generate_content(
            model=model, contents=user,
            config=types.GenerateContentConfig(system_instruction=system, temperature=0.2))
        return r.text
    raise SystemExit(f"Unknown PROVIDER {provider}")


# ---------------- role instructions (no company names) ----------------
RESEARCH_ANALYST = """You are the Research Analyst on an equity-research desk.
Use ONLY the filing text in the context. Cover: business model, competitive position,
catalysts, recent developments. Every claim quotes the line it comes from, in quotation
marks, followed by the source in brackets: [10-K], [10-Q] or [Release].
If the text does not support a claim, do not make it. Do not state any financial figure
that is not in a quoted line. Return Markdown with two sections:
'## Overview' and '## Market Positioning and Growth Outlook'."""

FINANCIAL_ANALYST = """You are the Financial Analyst on an equity-research desk.
You receive facts and ratios already computed by code. You NEVER compute in your head:
use only the numbers given, exactly as given. Every number carries its source: the XBRL
tag and period end and accession number, or the release line quoted. Every ratio shows
the arithmetic string you were given. Wherever a filing offers two definitions (e.g. net
sales vs total revenue, equity at year end vs average), say which one is used.
Cover growth, margins, returns, leverage, cash flow, the latest quarter and the peer
comparison (peer margins are on the same definition). If you need another ratio, list it
under 'Calculator requests' instead of computing it.
Return Markdown with one section: '## Valuation Insights'. Include a table of the eleven
core claims: total revenue, revenue growth, operating income and margin, net income,
diluted EPS, return on average equity, debt to equity, free cash flow, quarter revenue,
quarter growth vs same quarter last year, quarter diluted EPS (GAAP)."""

INVESTMENT_ADVISOR = """You are the Investment Advisor on an equity-research desk.
Use ONLY the two analysts' outputs in the context, nothing else. Write two sections:
'## Future Developments and Strategic Recommendations' and '## Investment Recommendation'.
The recommendation is exactly one of Buy, Hold or Sell, stated on its own line as
'Recommendation: <Buy|Hold|Sell>', followed by 'Deciding number: <the one number from the
Financial Analyst's output that decides it, with its source>' and a short thesis that uses
only numbers from the analysts' outputs."""


def _task(task, context, expected):
    return json.dumps({"task": task, "context": context, "expected_output": expected}, indent=2, default=str)


def _has(md, part):
    return f"## {part}".lower() in (md or "").lower()


# ---------------- Strategy Manager ----------------
def run_roles(company, ticker, texts, fx, ratios, quarter, peers, price):
    def trim(t, n=60000):
        return t[:n]

    # Research Analyst
    print("[role] Research Analyst")
    ra_ctx = {"company": company, "ticker": ticker,
              "10-K_text": trim(texts.get("10-K", "")), "release_text": trim(texts.get("8-K", ""), 30000)}
    ra_task = _task("Describe business model, competitive position, catalysts, recent developments.",
                    ra_ctx, "Markdown: ## Overview, ## Market Positioning and Growth Outlook; every claim quotes its line")
    ra = call_model(RESEARCH_ANALYST, ra_task)

    # Financial Analyst
    print("[role] Financial Analyst")
    fa_ctx = {"company": company, "ticker": ticker, "price": price, "facts": fx, "ratios": ratios,
              "quarter_release_lines": quarter, "peers": peers}
    fa_task = _task("Statement analysis and valuation from the facts and ratios given.", fa_ctx,
                    "Markdown: ## Valuation Insights with the eleven core claims table, each sourced")
    fa = call_model(FINANCIAL_ANALYST, fa_task)

    # Investment Advisor
    print("[role] Investment Advisor")
    ia_task = _task("Thesis and Buy/Hold/Sell from the two analysts' outputs only.",
                    {"research_analyst": ra, "financial_analyst": fa},
                    "Markdown: ## Future Developments and Strategic Recommendations, ## Investment Recommendation")
    ia = call_model(INVESTMENT_ADVISOR, ia_task)

    # Manager checks, sends each failing part back once
    print("[role] Strategy Manager")
    owners = {PARTS[0]: ("ra", RESEARCH_ANALYST, ra_task), PARTS[1]: ("ra", RESEARCH_ANALYST, ra_task),
              PARTS[2]: ("fa", FINANCIAL_ANALYST, fa_task),
              PARTS[3]: ("ia", INVESTMENT_ADVISOR, ia_task), PARTS[4]: ("ia", INVESTMENT_ADVISOR, ia_task)}
    outputs = {"ra": ra, "fa": fa, "ia": ia}
    sent_back = set()
    for part in PARTS:
        key, system, task = owners[part]
        if not _has(outputs[key], part) and key not in sent_back:
            print(f"[manager] '{part}' missing -> sent back to role once")
            outputs[key] = call_model(system, task + f"\n\nYour previous answer was missing the section '## {part}'. Return all your sections.")
            sent_back.add(key)
    rec_ok = any(w in outputs["ia"] for w in ("Recommendation: Buy", "Recommendation: Hold", "Recommendation: Sell"))
    problems = [p for p in PARTS if not _has(outputs[owners[p][0]], p)]
    if not rec_ok:
        problems.append("Recommendation line not one of Buy/Hold/Sell")
    return outputs["ra"] + "\n\n" + outputs["fa"] + "\n\n" + outputs["ia"], problems
