"""Lab 04 V: the seeded-error tests. Copies a saved run (the original is never touched),
plants an error in the copy's report, and runs the Verifier on the copy.

    python tools/seed_tests.py runs/<saved run folder>

Test 1 (seeded EPS): diluted EPS one dollar higher, its source line changed to match.
        Expect: marked wrong, corrected to the 10-K's figure, the 10-K's per-share line beside it.
Test 2 (invented number): a revenue growth rate four points too high, with its two inputs quoted.
        Expect: marked wrong (or unsupported), with the arithmetic from the quoted inputs.
Test 3 (clean report): the original run verified as it is. Expect: no correct number flagged.
Nothing here names a company.
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_team.verifier import CLAIM_RE, verify  # noqa: E402


def copy_run(src, suffix):
    dst = src.rstrip("/") + suffix
    n = 2
    while os.path.exists(dst):
        dst = src.rstrip("/") + f"{suffix}_{n}"
        n += 1
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("verified_report.md", "verifier_marks.json"))
    return dst


def seed_eps(folder):
    p = os.path.join(folder, "report.md")
    rep = open(p, encoding="utf-8").read()
    for m in CLAIM_RE.finditer(rep):
        body = m.group("body")
        is_eps = (m.group("kind") == "line" and re.match(r'\s*10-K\s+"Diluted\s*\$', body)) or \
                 (m.group("kind") == "xbrl" and body.startswith("EarningsPerShareDiluted"))
        if is_eps:
            old = m.group("num").strip()
            v = float(old.replace("$", "").replace(",", ""))
            new = f"${v + 1:.2f}"
            new_body = body.replace(old.replace("$", "").strip(), new.replace("$", ""), 1) if m.group("kind") == "line" else body
            seeded = f"{new} {{{m.group('kind')}: {new_body}}}"
            rep = rep.replace(m.group(0), seeded, 1)
            open(p, "w", encoding="utf-8").write(rep)
            return old, seeded
    raise SystemExit("no diluted EPS claim found to seed")


def seed_growth(folder):
    data = json.load(open(os.path.join(folder, "facts.json"), encoding="utf-8"))
    it = data["facts"]["items"]["total_revenue"]
    cur, pri = it["current"]["value"] / 1e6, it["prior"]["value"] / 1e6
    true = (cur / pri - 1) * 100
    tag, fy, py = it["tag"], it["current"]["end"], it["prior"]["end"]
    planted = (f"Revenue grew {true + 4:.2f}% {{calc: {cur:,.0f} / {pri:,.0f} - 1}}, "
               f"from ${pri:,.0f}M {{xbrl: {tag} {py}}} to ${cur:,.0f}M {{xbrl: {tag} {fy}}}.")
    p = os.path.join(folder, "report.md")
    rep = open(p, encoding="utf-8").read()
    rep = re.sub(r"(?m)^(## Valuation Insights\s*\n)", r"\1\n" + planted.replace("\\", "\\\\") + "\n", rep, count=1)
    open(p, "w", encoding="utf-8").write(rep)
    return planted


def main(src):
    src = src.rstrip("/")
    results = {}

    t1 = copy_run(src, "_seeded_eps")
    old, seeded = seed_eps(t1)
    print(f"\n== Test 1, seeded EPS in {t1}\n   was: {old}\n   now: {seeded}")
    _, claims = verify(t1)
    hit = [c for c in claims if c["raw"] == seeded]
    results["test1_seeded_eps"] = {"folder": t1, "seeded": seeded, "marks": hit}
    for c in hit:
        print(f"   -> {c['mark']}: {c['note']} | correction: {c.get('fix')}")

    t2 = copy_run(src, "_invented_growth")
    planted = seed_growth(t2)
    print(f"\n== Test 2, invented growth in {t2}\n   planted: {planted}")
    _, claims = verify(t2)
    hit = [c for c in claims if c["raw"] in planted]
    results["test2_invented_growth"] = {"folder": t2, "planted": planted, "marks": hit}
    for c in hit:
        print(f"   -> {c['num']}: {c['mark']}: {c['note']} | correction: {c.get('fix')}")

    print(f"\n== Test 3, clean report: {src}")
    counts, _ = verify(src)
    results["test3_clean"] = {"folder": src, "counts": counts}

    out = os.path.join(src + "_seeded_eps", "seeded_test_results.json")
    json.dump(results, open(out, "w", encoding="utf-8"), indent=2, default=str)
    print(f"\nRESULTS: {out}")


if __name__ == "__main__":
    main(sys.argv[1])
