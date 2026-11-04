"""Step 6: from the earnings release text, find the lines that state the
quarter's total revenue and GAAP diluted EPS. Lines are returned word for word.
"""
import re

REVENUE_PATTERNS = [
    r"^(total )?net (operating )?revenues?\b.*\$?\s*[\d,]+",
    r"^(total )?revenues?\b.*\$?\s*[\d,]+",
    r"^net sales\b.*\$?\s*[\d,]+",
    r"^total net sales\b.*\$?\s*[\d,]+",
]
EPS_PATTERNS = [
    r"^diluted (net income|earnings) per (common )?share",
    r"^diluted\b.*per share",
    r"^(net income|earnings) per (common )?share.*diluted",
    r"^diluted$",
]


def _find(lines, patterns, limit=3):
    hits = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        low = s.lower()
        if "non-gaap" in low or "comparable" in low or "adjusted" in low:
            continue
        for p in patterns:
            if re.search(p, low):
                # if the label sits alone on its line, join the next line with the numbers
                joined = s
                if not re.search(r"\$\s*[\d,]+|\d+\.\d+|\d{1,3}(,\d{3})+", s) and i + 1 < len(lines):
                    joined = s + " " + lines[i + 1].strip()
                hits.append(joined)
                break
        if len(hits) >= limit:
            break
    return hits


def quarter_lines(release_text):
    lines = [ln for ln in release_text.splitlines() if ln.strip()]
    return {"revenue_lines": _find(lines, REVENUE_PATTERNS), "eps_lines": _find(lines, EPS_PATTERNS)}
