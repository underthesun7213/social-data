"""Merge regional barrier-free CSVs into combined files with ISO3 codes.

Usage: python3 barrier-free/scripts/merge.py
Outputs: barrier-free/all_ratings.csv, barrier-free/all_indicators.csv
"""
import csv
import glob
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGIONS = os.path.join(BASE, "regions")

# Korean display name and ISO3 code for each country label used in the regional files.
COUNTRIES = {
    "일본": ("일본", "JPN"), "한국": ("한국", "KOR"),
    "싱가포르": ("싱가포르", "SGP"), "호주": ("호주", "AUS"),
    "USA": ("미국", "USA"),
    "영국": ("영국", "GBR"), "프랑스": ("프랑스", "FRA"), "네덜란드": ("네덜란드", "NLD"),
    "벨기에": ("벨기에", "BEL"), "룩셈부르크": ("룩셈부르크", "LUX"), "아일랜드": ("아일랜드", "IRL"),
    "스웨덴": ("스웨덴", "SWE"), "노르웨이": ("노르웨이", "NOR"), "덴마크": ("덴마크", "DNK"),
    "핀란드": ("핀란드", "FIN"),
    "독일": ("독일", "DEU"), "오스트리아": ("오스트리아", "AUT"), "스위스": ("스위스", "CHE"),
    "폴란드": ("폴란드", "POL"), "체코": ("체코", "CZE"), "헝가리": ("헝가리", "HUN"),
    "루마니아": ("루마니아", "ROU"), "불가리아": ("불가리아", "BGR"), "에스토니아": ("에스토니아", "EST"),
    "라트비아": ("라트비아", "LVA"), "리투아니아": ("리투아니아", "LTU"), "우크라이나": ("우크라이나", "UKR"),
    "세르비아": ("세르비아", "SRB"), "러시아": ("러시아", "RUS"),
    "Spain": ("스페인", "ESP"), "Italy": ("이탈리아", "ITA"), "Portugal": ("포르투갈", "PRT"),
    "Greece": ("그리스", "GRC"), "Malta": ("몰타", "MLT"), "Cyprus": ("키프로스", "CYP"),
    "사우디아라비아": ("사우디아라비아", "SAU"), "아랍에미리트(UAE)": ("아랍에미리트", "ARE"),
    "카타르": ("카타르", "QAT"),
    "캐나다": ("캐나다", "CAN"), "뉴질랜드": ("뉴질랜드", "NZL"), "중국": ("중국", "CHN"),
    "인도": ("인도", "IND"), "브라질": ("브라질", "BRA"), "멕시코": ("멕시코", "MEX"),
    "이스라엘": ("이스라엘", "ISR"), "남아프리카공화국": ("남아프리카공화국", "ZAF"),
    "이집트": ("이집트", "EGY"),
}
DIMS = ["LAW", "TRANS", "BUILT", "DIGI", "EMP", "TOUR"]
SCORE = {"상": 3, "중": 2, "하": 1}


def resolve(label):
    """Return (country_ko, iso3, sub_unit) for a country label; US sub-units share USA."""
    if label.startswith("USA - "):
        return "미국", "USA", label[len("USA - "):]
    if label not in COUNTRIES:
        raise SystemExit(f"Unknown country label: {label!r} - add it to COUNTRIES")
    ko, iso = COUNTRIES[label]
    return ko, iso, ""


def read(pattern):
    for path in sorted(glob.glob(os.path.join(REGIONS, pattern))):
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                row["source_file"] = os.path.basename(path)
                yield row


def merge_ratings():
    out, seen = [], set()
    for row in read("*_ratings.csv"):
        ko, iso, sub = resolve(row["country"].strip())
        key = (iso, sub)
        if key in seen:  # e.g. Russia appears in two regional files; keep the first
            continue
        seen.add(key)
        known = [SCORE[row[d]] for d in DIMS if row[d] in SCORE]
        out.append({
            "iso3": iso, "country": ko, "sub_unit": sub, "cluster": row["cluster"],
            **{d: row[d] for d in DIMS}, "overall": row["overall"],
            "dims_rated": len(known),
            "mean_score": f"{sum(known) / len(known):.2f}" if known else "",
            "rationale": row["rationale"], "source_file": row["source_file"],
        })
    write("all_ratings.csv", out)
    return out


def merge_indicators():
    out = []
    for row in read("*_indicators.csv"):
        label = row["country"].strip()
        ko, iso, sub = resolve(label) if (label in COUNTRIES or label.startswith("USA - ")) else (label, "", "")
        row = {"iso3": iso, "country_ko": ko, **row}
        if sub and not row.get("sub_unit"):
            row["sub_unit"] = sub
        out.append(row)
    write("all_indicators.csv", out)
    return out


def write(name, rows):
    with open(os.path.join(BASE, name), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    merge_ratings()
    ind = merge_indicators()
    unmapped = sorted({r["country"] for r in ind if not r["iso3"]})
    if unmapped:
        print("Indicator country labels without ISO3:", unmapped)
