"""Score the 47 countries from two independent rubric codings (VALIDITY.md 4.2-4.3).

Usage: python3 barrier-free/scripts/score.py
Reads rescoring/coding_A.csv and rescoring/coding_B.csv.
Writes rescoring/scores_by_coder.csv, rescoring/consensus.csv and prints
Krippendorff's alpha per dimension.

Rules
- Checklist dimensions (LAW 0-6, BUILT 0-4, DIGI 0-4): blank items are unknown.
  A grade is assigned only if every way of filling the blanks gives the same grade.
- TRANS: sub-grades for metro (A), bus (B), rail (C); TRANS = lowest available.
- EMP: employment gap in pp, or the disability/no-disability employment ratio.
- Overall: needs >= 4 of the 5 dimensions and at least one of TRANS/EMP.
  overall = 0.6 * mean(TRANS, EMP) + 0.4 * mean(LAW, BUILT, DIGI), 상 >= 2.5, 중 >= 1.75.
- Consensus: a dimension grade is kept only when both coders give the same grade,
  or when one coder leaves it ungraded and the other's grade rests on official
  data (TRANS/EMP numbers, LAW1-2 from the UN table are shared by both).
"""
import csv
import os

import krippendorff
import numpy as np

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rescoring")
GRADE = {3: "상", 2: "중", 1: "하"}
CHECKLISTS = {"LAW": (6, lambda s: 3 if s >= 5 else 2 if s >= 3 else 1),
              "BUILT": (4, lambda s: 3 if s == 4 else 2 if s >= 2 else 1),
              "DIGI": (4, lambda s: 3 if s == 4 else 2 if s >= 2 else 1)}
DIMS = ["LAW", "BUILT", "DIGI", "TRANS", "EMP"]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def checklist(row, dim):
    n, rule = CHECKLISTS[dim]
    vals = [num(row.get(f"{dim}{i}")) for i in range(1, n + 1)]
    known = sum(v for v in vals if v is not None)
    blanks = sum(v is None for v in vals)
    lo, hi = rule(known), rule(known + blanks)
    return lo if lo == hi else None


def band(v, hi, mid):
    return None if v is None else 3 if v >= hi else 2 if v >= mid else 1


def trans(row):
    subs = [band(num(row["TRANS_A"]), 90, 60), band(num(row["TRANS_B"]), 90, 50),
            band(num(row["TRANS_C"]), 80, 50)]
    subs = [s for s in subs if s is not None]
    return min(subs) if subs else None


def emp(row):
    gap, ratio = num(row["EMP_GAP"]), num(row["EMP_RATIO"])
    if gap is not None:
        return 3 if gap < 15 else 2 if gap <= 30 else 1
    return band(ratio, 0.75, 0.50)


def overall(g):
    graded = [d for d in DIMS if g.get(d)]
    if len(graded) < 4 or not (g.get("TRANS") or g.get("EMP")):
        return None
    out = np.mean([g[d] for d in ("TRANS", "EMP") if g.get(d)])
    inp = np.mean([g[d] for d in ("LAW", "BUILT", "DIGI") if g.get(d)])
    s = 0.6 * out + 0.4 * inp
    return 3 if s >= 2.5 else 2 if s >= 1.75 else 1


def grades(row):
    g = {d: checklist(row, d) for d in CHECKLISTS}
    g["TRANS"], g["EMP"] = trans(row), emp(row)
    g["overall"] = overall(g)
    return g


def load(name):
    return {r["iso3"]: r for r in csv.DictReader(open(os.path.join(BASE, name), encoding="utf-8-sig"))}


def main():
    a, b = load("coding_A.csv"), load("coding_B.csv")
    isos = sorted(set(a) & set(b))
    ga, gb = {i: grades(a[i]) for i in isos}, {i: grades(b[i]) for i in isos}

    print("Krippendorff alpha (ordinal), pairs where both coders graded")
    for d in DIMS + ["overall"]:
        data = np.array([[ga[i][d] or np.nan for i in isos], [gb[i][d] or np.nan for i in isos]], dtype=float)
        both = int(np.sum(~np.isnan(data).any(axis=0)))
        agree = int(np.sum((data[0] == data[1]) & ~np.isnan(data).any(axis=0)))
        alpha = krippendorff.alpha(reliability_data=data, level_of_measurement="ordinal") if both > 1 else float("nan")
        print(f"  {d:8s} alpha={alpha:5.2f}  both graded={both:2d}  exact agree={agree:2d}")

    with open(os.path.join(BASE, "scores_by_coder.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["iso3", "country"] + [f"{d}_{c}" for d in DIMS + ["overall"] for c in "AB"])
        for i in isos:
            w.writerow([i, a[i]["country"]] + [GRADE.get(g[i][d], "") for d in DIMS + ["overall"] for g in (ga, gb)])

    rows = []
    for i in isos:
        cons, notes = {}, []
        for d in DIMS:
            x, y = ga[i][d], gb[i][d]
            if x and y and x == y:
                cons[d] = x
            elif x and y:
                notes.append(f"{d} 불일치(A {GRADE[x]}, B {GRADE[y]})")
            elif (x or y) and d in ("TRANS", "EMP"):
                cons[d] = x or y
                notes.append(f"{d} 한 명만 수치 확보")
        cons["overall"] = overall(cons)
        rows.append({"iso3": i, "country": a[i]["country"],
                     **{d: GRADE.get(cons.get(d), "") for d in DIMS},
                     "dims_graded": sum(1 for d in DIMS if cons.get(d)),
                     "overall": GRADE.get(cons["overall"], "자료부족"),
                     "notes": "; ".join(notes)})
    with open(os.path.join(BASE, "consensus.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print("consensus overall:", dict(Counter(r["overall"] for r in rows)))


if __name__ == "__main__":
    main()
