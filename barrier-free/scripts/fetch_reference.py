"""Download primary-source reference tables used to verify the barrier-free dataset.

Usage: python3 barrier-free/scripts/fetch_reference.py
Outputs (barrier-free/reference/):
  un_crpd_status.csv        UN Treaty Collection: CRPD (IV-15) and Optional Protocol (IV-15-a)
  eurostat_employment_gap.csv  Eurostat tepsr_sp200, disability employment gap (pp), some or severe, total
  eurostat_gali.csv         Eurostat hlth_silc_12, share of 16+ with activity limitation (some or severe)
  worldbank_age65.csv       World Bank SP.POP.65UP.TO.ZS, latest year per country
  ddi_estimates.csv         Disability Data Initiative (Fordham) cross-country estimates,
                            adults 15+: prevalence and employment by disability status
"""
import csv
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

import pycountry

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "reference")
UA = {"User-Agent": "Mozilla/5.0"}

DDI_NAMES = {"Congo, Rep.": "COG", "Guinea Bissau": "GNB", "Palestine": "PSE",
             "Cote d'Ivoire": "CIV", "Bolivia": "BOL", "Tanzania": "TZA", "Vietnam": "VNM"}

# UN participant names that pycountry's fuzzy lookup gets wrong or misses.
UN_NAMES = {
    "Republic of Korea": "KOR", "Democratic People's Republic of Korea": "PRK",
    "Türkiye": "TUR", "Russian Federation": "RUS", "Republic of Moldova": "MDA",
    "Bolivia (Plurinational State of)": "BOL", "Venezuela (Bolivarian Republic of)": "VEN",
    "Iran (Islamic Republic of)": "IRN", "Lao People's Democratic Republic": "LAO",
    "United Republic of Tanzania": "TZA", "Democratic Republic of the Congo": "COD",
    "Congo": "COG", "State of Palestine": "PSE", "Holy See": "VAT",
    "Micronesia (Federated States of)": "FSM", "European Union": "EU",
    "Côte d'Ivoire": "CIV", "Netherlands (Kingdom of the)": "NLD", "Niger": "NER",
    "United Kingdom of Great Britain and Northern Ireland": "GBR",
    "United States of America": "USA", "Syrian Arab Republic": "SYR",
    "Bahamas (The)": "BHS", "Naoero": "NRU", "St. Kitts and Nevis": "KNA",
    "St. Lucia": "LCA", "St. Vincent and the Grenadines": "VCT",
}


def get(url, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8")
        except urllib.error.URLError:
            if attempt == tries - 1:
                raise
            time.sleep(2 ** (attempt + 1))


def iso3(name):
    name = re.sub(r"\s*\d+(,\s*\d+)*$", "", name).strip()  # drop footnote numbers
    if name in UN_NAMES:
        return UN_NAMES[name]
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        print(f"  no ISO3 for UN name {name!r} - add it to UN_NAMES")
        return ""


def parse_date(cell):
    cell = " ".join(cell.split())
    m = re.match(r"(\d{1,2} \w{3} \d{4})\s*([a-z]?)", cell)
    return (m.group(1), m.group(2)) if m else ("", "")


def un_table(no):
    url = f"https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no={no}&chapter=4&clang=_en"
    t = get(url)
    tb = re.search(r'<table[^>]*id="[^"]*tblgrid[^"]*"[^>]*>(.*?)</table>', t, re.S).group(1)
    out = {}
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", tb, re.S)[1:]:
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
        # Key by ISO3: the two treaty tables spell some participants differently.
        out[iso3(cells[0])] = (cells[0], parse_date(cells[1])[0], *parse_date(cells[2]))
    return url, out


def crpd():
    url, conv = un_table("IV-15")
    _, op = un_table("IV-15-a")
    rows = []
    for code in sorted(set(conv) | set(op)):
        c, o = conv.get(code, ("", "", "", "")), op.get(code, ("", "", "", ""))
        status = "비준" if c[2] else ("서명만" if c[1] else "미참여")
        rows.append({"iso3": code, "un_name": c[0] or o[0], "crpd_signature": c[1],
                     "crpd_ratification": c[2], "crpd_action": {"a": "가입", "c": "공식확인"}.get(c[3], "비준" if c[2] else ""),
                     "crpd_status": status, "op_signature": o[1], "op_ratification": o[2],
                     "op_status": "비준" if o[2] else ("서명만" if o[1] else "미참여"),
                     "source_url": url})
    write("un_crpd_status.csv", rows)


def eurostat(ds, fixed, value_name):
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{ds}?format=JSON&lang=en"
    d = json.loads(get(url))
    dims, size = d["id"], d["size"]
    cat = {k: d["dimension"][k]["category"] for k in dims}
    geo_label, rows = cat["geo"]["label"], []
    for geo, gi in cat["geo"]["index"].items():
        for year, ti in sorted(cat["time"]["index"].items()):
            pos = {**{k: cat[k]["index"][v] for k, v in fixed.items()}, "geo": gi, "time": ti}
            flat = 0
            for k, n in zip(dims, size):
                flat = flat * n + pos.get(k, 0)
            v = d["value"].get(str(flat))
            if v is not None:
                rows.append({"geo": geo, "geo_label": geo_label[geo], "year": year, value_name: v,
                             "flag": d.get("status", {}).get(str(flat), ""), "source_url": url})
    write(f"eurostat_{value_name}.csv", rows)


def worldbank():
    url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.65UP.TO.ZS?format=json&per_page=20000&mrnev=1"
    data = json.loads(get(url))[1]
    rows = [{"iso3": r["countryiso3code"], "country": r["country"]["value"], "year": r["date"],
             "age65_pct": round(r["value"], 2), "source_url": url}
            for r in data if r["value"] is not None and r["countryiso3code"]]
    write("worldbank_age65.csv", rows)


def ddi():
    api = "https://www.disabilitydatainitiative.org/api"
    countries = [c["value"] for c in json.loads(get(api + "/cos"))]
    queries = [("Adults with disabilities", ["Any difficulty", "A lot of difficulty/Cannot do at all"]),
               ("Employment", ["No difficulty", "Any difficulty"])]
    rows = []
    for ind, dis in queries:
        qs = urllib.parse.urlencode([("cos", c) for c in countries] + [("ind", ind),
                                    ("pop", "All adults (ages 15 and older)")] + [("dis", d) for d in dis])
        for r in json.loads(get(f"{api}/cross?{qs}")):
            if r["Value"] in (None, "", "NA"):
                continue
            rows.append({"iso3": DDI_NAMES.get(r["Country"]) or iso3(r["Country"]), "country": r["Country"],
                         "indicator": ind, "difficulty": r["DifficultyName"],
                         "pct": round(float(r["Value"]) * 100, 2),
                         "source_url": "https://www.disabilitydatainitiative.org/DS-E"})
    write("ddi_estimates.csv", rows)


def write(name, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    crpd()
    eurostat("tepsr_sp200", {"freq": "A", "sex": "T", "lev_limit": "SM_SEV", "unit": "PC_PNT"}, "employment_gap")
    eurostat("hlth_silc_12", {"freq": "A", "unit": "PC", "quant_inc": "TOTAL", "age": "Y_GE16",
                              "sex": "T", "lev_limit": "SM_SEV"}, "gali")
    worldbank()
    ddi()
