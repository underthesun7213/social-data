"""Build the datasets behind the two world maps.

Usage: python3 barrier-free/scripts/build_map_data.py
Inputs: reference/*.csv, rescoring/coding_[AB].csv, all_indicators_verified.csv,
        all_ratings.csv, maps/world_50m_raw.json, maps/transport_curated.csv
Outputs (barrier-free/maps/):
  world_geo.json        country shapes (Natural Earth 1:50m via world-atlas 2.0.2) with ISO3
  crpd.csv              CRPD / Optional Protocol status for every mapped country
  emp_gap.csv           disability employment gap, official definitions (Eurostat + national)
  ddi_emp.csv           Disability Data Initiative employment by disability (WG definition)
  legal_access.csv      accessibility legal duties agreed by both coders (case countries)
  case_countries.csv    the 47 case-study countries with verification counts
  indicators_panel.csv  verified indicators for the click-through panel
"""
import csv
import json
import os
from collections import Counter, defaultdict

import pycountry

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(BASE, "maps")
EUROSTAT_GEO = {"EL": "GRC", "UK": "GBR", "XK": "XKX"}
NUMERIC_EXTRA = {"-99": "", "": ""}


def rows(path):
    return list(csv.DictReader(open(os.path.join(BASE, path), encoding="utf-8-sig")))


def write_csv(name, data):
    with open(os.path.join(MAPS, name), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)
    print(f"{name}: {len(data)} rows")


def iso3_from_numeric(code):
    if code in NUMERIC_EXTRA:
        return NUMERIC_EXTRA[code]
    c = pycountry.countries.get(numeric=code)
    return c.alpha_3 if c else ""


def geo():
    raw = json.load(open(os.path.join(MAPS, "world_50m_raw.json")))
    out = [{"iso3": iso3_from_numeric(r["id"]), "name": r["name"], "geometry": r["geometry"]}
           for r in raw]
    out = [r for r in out if r["name"] != "Antarctica"]
    json.dump(out, open(os.path.join(MAPS, "world_geo.json"), "w"), ensure_ascii=False)
    print(f"world_geo.json: {len(out)} shapes, {sum(1 for r in out if not r['iso3'])} without ISO3")
    return {r["iso3"]: r["name"] for r in out if r["iso3"]}


def crpd(geo_names):
    ref = {r["iso3"]: r for r in rows("reference/un_crpd_status.csv")}
    out = []
    for iso, name in sorted(geo_names.items()):
        r = ref.get(iso)
        if r and r["crpd_status"] == "비준" and r["op_status"] == "비준":
            status, rank = "협약 + 선택의정서", 3
        elif r and r["crpd_status"] == "비준":
            status, rank = "협약만 비준", 2
        elif r and r["crpd_status"] == "서명만":
            status, rank = "서명만 (미비준)", 1
        else:
            status, rank = "미참여", 0
        out.append({"iso3": iso, "name": name, "status": status, "rank": rank,
                    "crpd_ratification": r["crpd_ratification"] if r else "",
                    "op_ratification": r["op_ratification"] if r else "",
                    "source": "UN Treaty Collection IV-15, IV-15-a"})
    write_csv("crpd.csv", out)


def emp_gap():
    latest = {}
    for r in rows("reference/eurostat_employment_gap.csv"):
        # Aggregates are not countries; values before 2020 are outside the rubric's year window.
        if r["geo"].startswith("EU") or r["geo"].startswith("EA") or r["year"] < "2020":
            continue
        if r["geo"] not in latest or r["year"] > latest[r["geo"]]["year"]:
            latest[r["geo"]] = r
    out = []
    for g, r in sorted(latest.items()):
        iso = EUROSTAT_GEO.get(g) or pycountry.countries.get(alpha_2=g).alpha_3
        out.append({"iso3": iso, "gap_pp": r["employment_gap"], "year": r["year"],
                    "source": "Eurostat tepsr_sp200 (EU-SILC)",
                    "definition": "20–64세, 활동 제약(GALI) 있음 vs 없음"})
    have = {r["iso3"] for r in out}
    coded = {r["iso3"]: r for r in rows("rescoring/coding_A.csv")}
    coded_b = {r["iso3"]: r for r in rows("rescoring/coding_B.csv")}
    notes = {"GBR": ("ONS Labour Force Survey", "16–64세, 평등법 기준 장애"),
             "USA": ("ACS (Cornell 집계)", "21–64세, ACS 장애 문항"),
             "CAN": ("Statistics Canada CSD", "25–64세"),
             "NZL": ("Stats NZ HLFS", "15–64세, WG 문항"),
             "AUS": ("ABS SDAC 2022 (계산값)", "15–64세, 경제활동참가·실업률로 계산")}
    for iso, (src, definition) in notes.items():
        a, b = coded.get(iso, {}), coded_b.get(iso, {})
        if iso in have or not a.get("EMP_GAP"):
            continue
        out.append({"iso3": iso, "gap_pp": a["EMP_GAP"], "year": a.get("EMP_YEAR") or b.get("EMP_YEAR", ""),
                    "source": src, "definition": definition})
    write_csv("emp_gap.csv", out)


def ddi():
    by = defaultdict(dict)
    for r in rows("reference/ddi_estimates.csv"):
        if r["indicator"] == "Employment":
            by[r["iso3"]][r["difficulty"]] = float(r["pct"])
            by[r["iso3"]]["country"] = r["country"]
    out = [{"iso3": iso, "country": v["country"], "emp_disability": v["Any difficulty"],
            "emp_no_disability": v["No difficulty"],
            "gap_pp": round(v["No difficulty"] - v["Any difficulty"], 1),
            "source": "Disability Data Initiative DS-E", "definition": "15세 이상, WG 문항 '어려움 있음' vs '없음'"}
           for iso, v in sorted(by.items()) if "Any difficulty" in v and "No difficulty" in v]
    write_csv("ddi_emp.csv", out)


def legal_and_cases():
    a = {r["iso3"]: r for r in rows("rescoring/coding_A.csv")}
    b = {r["iso3"]: r for r in rows("rescoring/coding_B.csv")}
    items = {"LAW4": "구속력 있는 접근성 기술기준 법", "BUILT1": "신축 건물 접근성 의무",
             "DIGI1": "공공 웹 접근성(WCAG) 법적 의무", "DIGI2": "민간 디지털 접근성 법적 의무"}
    ind = rows("all_indicators_verified.csv")
    stat = defaultdict(Counter)
    for r in ind:
        if r["iso3"]:
            stat[r["iso3"]][r["verify_status"]] += 1
    ratings = {r["iso3"]: r for r in rows("all_ratings.csv") if not r["sub_unit"]}
    legal, cases = [], []
    for iso in sorted(a):
        agreed = {k: a[iso][k] for k in items if a[iso][k] != "" and a[iso][k] == b[iso][k]}
        ones = [items[k] for k, v in agreed.items() if v == "1"]
        legal.append({"iso3": iso, "country": a[iso]["country"],
                      "duties_confirmed": len(ones), "items_agreed": len(agreed),
                      "duties": " · ".join(ones) or "없음",
                      "unresolved": " · ".join(items[k] for k in items if k not in agreed) or "없음"})
        s = stat[iso]
        n = sum(s.values())
        primary = s["원문확인"] + s["원문확인(자동)"] + s["원문수정"]
        cases.append({"iso3": iso, "country": a[iso]["country"],
                      "cluster": ratings.get(iso, {}).get("cluster", ""),
                      "indicators": n, "primary_verified_pct": round(100 * primary / n) if n else 0})
    write_csv("legal_access.csv", legal)
    write_csv("case_countries.csv", cases)


def panel():
    out = [{"iso3": r["iso3"], "dimension": r["dimension"], "indicator": r["indicator"],
            "value": r["value_final"], "unit": r["unit"], "year": r["year_final"],
            "status": r["verify_status"], "url": r["verify_url"] or r["source_url"]}
           for r in rows("all_indicators_verified.csv")
           if r["iso3"] and r["verify_status"] not in ("미확인", "불일치")]
    write_csv("indicators_panel.csv", out)


if __name__ == "__main__":
    names = geo()
    crpd(names)
    emp_gap()
    ddi()
    legal_and_cases()
    panel()
