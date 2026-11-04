"""The Verifier node. Runs after the Manager on every run; nothing turns it off.

It receives ONLY: the compiled report, the saved filing texts and the saved facts.
It never sees the roles' instructions and never reruns them.
It skips the Investment Advisor's thesis (the '## Investment Recommendation' section).

For every sourced number, in code:
  {xbrl: Tag period}      -> compared with the saved facts, exactly (after rounding to what the report shows)
  {line: Doc "quoted"}    -> the quoted line must appear in that filing's text (spacing/format ignored),
                             and must contain the number
  {calc: a / b}           -> recomputed from its quoted inputs
Then, with the model (when API_KEY is set): does the line state that number, for that period,
in that definition?
A number with no source is unsupported; so is a return on equity with no stated definition.
Marks: correct / wrong / unsupported. Wrong and unsupported numbers are corrected from the
filings where the filings allow, with the real line or tag beside each.
"""
import ast
import json
import operator
import os
import re

from agent_team.runfolder import DOC_FILES, load_json, load_texts, save_json, save_text

CLAIM_RE = re.compile(
    r"(?P<num>[-−]?\$?\d[\d,]*(?:\.\d+)?\s?(?:%|x|M|B)?)\s*\{(?P<kind>xbrl|line|calc):\s*(?P<body>[^{}]*)\}")
BARE_NUM_RE = re.compile(r"(?<![\w.$])(\$\d[\d,]*(?:\.\d+)?[MB]?|\d[\d,]*(?:\.\d+)?%|\d+(?:\.\d+)?x)(?![\w])")
LINE_NUM_RE = re.compile(r"\(?-?\$?\s?\d[\d,]*(?:\.\d+)?\)?")
SKIP_SECTION = "investment recommendation"


# ---------- parsing ----------
def parse_value(tok):
    t = tok.strip().replace("−", "-")
    unit = ""
    for u in ("%", "x", "M", "B"):
        if t.endswith(u):
            unit, t = u, t[:-1].strip()
            break
    per_share = t.startswith("$") and unit == ""
    t = t.replace("$", "").replace(",", "")
    decimals = len(t.split(".")[1]) if "." in t else 0
    return float(t), unit, decimals, per_share


def fmt_value(v, unit, decimals, per_share):
    if unit == "M":
        return f"${v:,.{decimals}f}M"
    if unit == "B":
        return f"${v:,.{decimals}f}B"
    if unit == "%":
        return f"{v:.{decimals}f}%"
    if unit == "x":
        return f"{v:.{decimals}f}x"
    return f"${v:,.{decimals}f}" if per_share else f"{v:,.{decimals}f}"


def same(reported, true, decimals):
    return abs(round(true, decimals) - reported) < 0.5 * 10 ** (-decimals) + 1e-9


def norm(s):
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("–", "-")
    return re.sub(r"\s+", "", s).lower()


def line_numbers(line):
    out = []
    for m in LINE_NUM_RE.finditer(line):
        raw = m.group(0)
        neg = raw.startswith("(") and raw.endswith(")")
        digits = re.sub(r"[^\d.]", "", raw)
        if not digits or digits == ".":
            continue
        try:
            v = float(digits)
        except ValueError:
            continue
        out.append(-v if neg else v)
    return out


def label_key(line):
    return norm(LINE_NUM_RE.sub(" ", line))


def sections(report):
    """Yield (section_title, text) for each '## ' section; text before the first is 'preamble'."""
    parts = re.split(r"(?m)^## +(.+)$", report)
    yield "preamble", parts[0]
    for i in range(1, len(parts), 2):
        yield parts[i].strip(), parts[i + 1]


# ---------- code checks ----------
def check_xbrl(claim, idx):
    v, unit, d, per_share = parse_value(claim["num"])
    bits = claim["body"].split()
    if len(bits) < 2:
        return "unsupported", "source names no tag and period", None
    tag, period = bits[0], bits[1]
    val = idx.get(tag, {}).get(period)
    if val is None:
        return "unsupported", f"{tag} {period} is not in the saved facts", None
    scale = {"M": 1e6, "B": 1e9}.get(unit, 1)
    true = val / scale
    if same(v, true, d):
        return "correct", f"facts: {tag} {period} = {val:,.2f}".rstrip("0").rstrip("."), None
    return "wrong", f"facts: {tag} {period} = {val:,}", f"{fmt_value(true, unit, d, per_share)} {{xbrl: {tag} {period}}}"


def check_line(claim, texts):
    v, unit, d, per_share = parse_value(claim["num"])
    m = re.match(r'\s*(10-K|10-Q|Release|8-K)\s+"(.+)"\s*$', claim["body"])
    if not m:
        return "unsupported", "line source not in the form Doc \"quoted line\"", None
    doc, quoted = m.group(1), m.group(2)
    text = texts.get(doc)
    if text is None:
        return "unsupported", f"no saved text for {doc}", None
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    qnums = line_numbers(quoted)
    hits_at = [i for i, x in enumerate(qnums) if same(v, abs(x), d)]
    found = norm(quoted) in norm(text)
    if found and hits_at:
        return "correct", f"line found in {doc}", None
    if found and not hits_at:
        return "unsupported", f"line found in {doc}, but it does not state {claim['num']}", None
    # line not in the filing: find the real line by its label and the other numbers on it
    key = label_key(quoted)
    best = None
    for ln in lines:
        if label_key(ln) != key:
            continue
        lnums = line_numbers(ln)
        if len(lnums) != len(qnums):
            continue
        others = sum(1 for i, (a, b) in enumerate(zip(qnums, lnums)) if a == b)
        if best is None or others > best[0]:
            best = (others, ln, lnums)
    if best and hits_at:
        i = hits_at[0]
        true = abs(best[2][i])
        corrected = f"{fmt_value(true, unit, d, per_share)} {{line: {doc} \"{best[1]}\"}}"
        return "wrong", f"quoted line is not in {doc}; real line: \"{best[1]}\"", corrected
    return "unsupported", f"quoted line is not in {doc}, and no line with that label was found", None


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.USub: operator.neg}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("not arithmetic")


def check_calc(claim, context):
    v, unit, d, per_share = parse_value(claim["num"])
    expr = claim["body"].split("=")[0]
    expr = expr.replace(",", "").replace("$", "").replace("×", "*").replace("−", "-").replace("M", "").replace("B", "")
    expr = re.sub(r"(\d)\s*%", r"\1", expr)
    try:
        r = _eval(ast.parse(expr.strip(), mode="eval"))
    except Exception:
        return "unsupported", f"calc not recomputable: {claim['body']}", None
    true = r * 100 if unit == "%" else r
    low = context.lower()
    if re.search(r"return on (common |shareholders'? |stockholders'? )?equity|\broe\b", low) and "average" not in low and "year-end" not in low:
        return "unsupported", "return on equity with no stated definition (average or year-end equity)", None
    if same(v, true, d):
        return "correct", f"recomputed {claim['body'].strip()} = {fmt_value(true, unit, d, per_share)}", None
    return "wrong", f"recomputed {claim['body'].strip()} = {fmt_value(true, unit, d, per_share)}", \
        f"{fmt_value(true, unit, d, per_share)} {{calc: {claim['body'].strip()}}}"


# ---------- model check ----------
def model_check(claims):
    """Ask the model whether each code-correct line states that number for that period and definition."""
    if not os.getenv("API_KEY"):
        for c in claims:
            c["model"] = "not run (no API_KEY in .env)"
        return
    todo = [c for c in claims if c["kind"] == "line" and c["code"] == "correct"]
    for c in claims:
        c.setdefault("model", "n/a (code check only)" if c["kind"] != "line" else "not needed")
    if not todo:
        return
    from desk.roles import call_model
    ask = [{"id": c["id"], "report_context": c["context"][-300:], "number": c["num"], "line": c["body"]} for c in todo]
    system = ("You verify an equity-research report against filing lines. For each item, answer whether the quoted "
              "line states that number for the period and in the definition the report's context claims. "
              "Return ONLY a JSON list: [{\"id\": n, \"ok\": true|false, \"reason\": \"...\"}].")
    try:
        raw = call_model(system, json.dumps(ask, indent=1))
        raw = raw[raw.find("["): raw.rfind("]") + 1]
        res = {r["id"]: r for r in json.loads(raw)}
    except Exception as e:  # the Verifier still runs; record why the model half did not
        for c in todo:
            c["model"] = f"model check failed: {e.__class__.__name__}"
        return
    for c in todo:
        r = res.get(c["id"])
        if r is None:
            c["model"] = "no answer"
        elif r.get("ok"):
            c["model"] = "agrees"
        else:
            c["model"] = f"disagrees: {r.get('reason', '')}"
            c["mark"], c["note"] = "unsupported", f"model: {r.get('reason', '')}"


# ---------- the node ----------
def verify(run_folder, report_name="report.md"):
    print("[node] verifier")
    with open(os.path.join(run_folder, report_name), encoding="utf-8") as f:
        report = f.read()
    data = load_json(run_folder, "facts.json")
    idx = data.get("xbrl_index", {})
    texts = load_texts(run_folder)

    claims, n = [], 0
    for title, body in sections(report):
        if title.lower() == SKIP_SECTION:
            continue
        for ln in body.splitlines():
            for m in CLAIM_RE.finditer(ln):
                n += 1
                c = {"id": n, "section": title, "num": m.group("num").strip(), "kind": m.group("kind"),
                     "body": m.group("body").strip(), "raw": m.group(0), "context": ln[: m.start()]}
                if c["kind"] == "xbrl":
                    c["code"], c["note"], c["fix"] = check_xbrl(c, idx)
                elif c["kind"] == "line":
                    c["code"], c["note"], c["fix"] = check_line(c, texts)
                else:
                    c["code"], c["note"], c["fix"] = check_calc(c, ln[: m.start()])
                c["mark"] = c["code"]
                claims.append(c)
            # numbers with no source (only in the Financial Analyst's part)
            if title.lower() == "valuation insights" and not ln.lstrip().startswith("|---"):
                stripped = CLAIM_RE.sub(" ", ln)
                stripped = re.sub(r"\{[^{}]*\}", " ", stripped)
                stripped = re.sub(r'"[^"]*"', " ", stripped)
                for m in BARE_NUM_RE.finditer(stripped):
                    n += 1
                    claims.append({"id": n, "section": title, "num": m.group(0), "kind": "none", "body": "",
                                   "raw": m.group(0), "context": ln.strip()[:120], "code": "unsupported",
                                   "mark": "unsupported", "note": "no source", "fix": None})
    model_check(claims)

    # build the verified report: corrections inline, marks table under the first line
    fixed = report
    for c in claims:
        if c["mark"] in ("wrong", "unsupported") and c["kind"] != "none" and c["raw"] in fixed:
            repl = f"~~{c['num']}~~ **{c['fix']}** [verifier: {c['mark']}]" if c.get("fix") else \
                f"{c['raw']} **[verifier: {c['mark']} — {c['note']}]**"
            fixed = fixed.replace(c["raw"], repl, 1)
    first, _, rest = fixed.partition("\n")
    counts = {k: sum(1 for c in claims if c["mark"] == k) for k in ("correct", "wrong", "unsupported")}
    table = ["", "## Verifier marks", "",
             f"Correct: {counts['correct']} · Wrong: {counts['wrong']} · Unsupported: {counts['unsupported']} "
             f"· Skipped: the Investment Recommendation (thesis)", "",
             "| # | Part | Report said | Source | Code check | Model check | Mark | Correction / real line |",
             "|---|---|---|---|---|---|---|---|"]
    for c in claims:
        src = f"{c['kind']}: {c['body']}" if c["kind"] != "none" else "none"
        table.append("| {} | {} | {} | {} | {} | {} | **{}** | {} |".format(
            c["id"], c["section"], c["num"], src.replace("|", "/"), c["note"].replace("|", "/"),
            c.get("model", ""), c["mark"], (c.get("fix") or "").replace("|", "/")))
    verified = first + "\n" + "\n".join(table) + "\n\n---\n" + rest
    save_text(run_folder, "verified_report.md", verified)
    save_json(run_folder, "verifier_marks.json", claims)
    print(f"   marks: {counts}")
    print(f"VERIFIED REPORT: {os.path.join(run_folder, 'verified_report.md')}")
    return counts, claims
