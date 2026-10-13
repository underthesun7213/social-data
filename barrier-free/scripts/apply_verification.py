"""Attach verification results to every indicator row.

Usage: python3 barrier-free/scripts/apply_verification.py
Reads all_indicators.csv plus verification/{source_check,result_*,result2_*}.csv
Writes all_indicators_verified.csv and prints a reliability summary.

Status precedence per row:
  1. result2_* (primary-source check by reading the original)  -> as recorded
  2. source_check match == 전부 (every number found in the cited page) -> 원문확인(자동)
  3. result_* (search-snippet check) -> 검색확인 / 검색수정 / ... (weaker)
  4. otherwise -> 미검증
"""
import csv
import glob
import os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(BASE, "verification")


def load(pattern):
    out = {}
    for path in sorted(glob.glob(os.path.join(V, pattern))):
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            out[r["row_id"]] = r
    return out


def main():
    rows = list(csv.DictReader(open(os.path.join(BASE, "all_indicators.csv"), encoding="utf-8")))
    auto = load("source_check.csv")
    snippet = load("result_[ABC].csv")
    primary = load("result2_*.csv")
    counter = {}
    for r in rows:
        counter[r["source_file"]] = counter.get(r["source_file"], 0) + 1
        rid = f"{r['source_file'].replace('_indicators.csv', '')}:{counter[r['source_file']]}"
        r["row_id"] = rid
        p, a, s = primary.get(rid), auto.get(rid), snippet.get(rid)
        status, conf, cval, cyear, url, note = "미검증", "", "", "", "", ""
        if p:
            status, conf = p["status"], p["confidence"]
            cval, cyear, url = p["corrected_value"], p["corrected_year"], p["verified_url"]
            note = p["comment"]
        elif a and a["match"] == "전부":
            status, conf, url = "원문확인(자동)", "중", r["source_url"]
            note = "인용 페이지 원문에서 수치 자동 일치 (의미 일치는 미확인)"
        elif s:
            status = {"확인": "검색확인", "수정": "검색수정"}.get(s["status"], "검색" + s["status"])
            conf, cval, cyear, url, note = s["confidence"], s["corrected_value"], s["corrected_year"], s["verify_url"], s["comment"]
        corrected = status in ("원문수정", "검색수정")
        r.update({
            "verify_status": status, "verify_confidence": conf,
            "value_final": cval if corrected and cval else r["value"],
            "year_final": cyear if corrected and cyear else r["year"],
            "verify_url": url, "verify_note": note,
        })
    out = os.path.join(BASE, "all_indicators_verified.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"all_indicators_verified.csv: {len(rows)} rows")
    for k, v in Counter(r["verify_status"] for r in rows).most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
