"""Column profile of the H&M Kaggle files, in two forms.

Writes to data/profile/ (gitignored, like the rest of data/):
  hm_profile.html        local report, includes sample raw rows -- keep it local
  profile_columns.json   one row per column: missing, distinct, numeric stats (aggregates only)
  profile_bins.json      histogram / top-value / per-month bars (aggregates only, no hashed ids)
  analysis_*.json        aggregate tables from analysis/hm_eda_results_en.xlsx plus a few
                         recomputed ones, for the data-browser artifact

Run: py -I analysis/hm_profile.py   (uses the parquet cache from hm_eda_common)
"""

import html
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hm_eda_common as common  # noqa: E402

ROOT = common.ROOT
RAW = common.DATA
OUT = ROOT / "data" / "profile"
DICT = ROOT / "analysis" / "hm_data_dictionary.csv"
WB = ROOT / "analysis" / "hm_eda_results_en.xlsx"

# Columns whose values are hashes: never export their top values
HASHED = {"customer_id", "postal_code"}
TEXT = {"detail_desc"}
QS = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]


def r(x, n=4):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    return round(float(x), n)


def per_id_bins(counts):
    edges = [(1, 1, "1"), (2, 2, "2"), (3, 4, "3-4"), (5, 9, "5-9"), (10, 19, "10-19"),
             (20, 49, "20-49"), (50, 99, "50-99"), (100, np.inf, "100+")]
    out = []
    for lo, hi, lab in edges:
        n = int(((counts >= lo) & (counts <= hi)).sum())
        out.append((lab, n))
    return out


def profile(file, col, s, n_rows, rows_per_id=None):
    """Return (column row, list of bin rows, local extras)."""
    miss = int(s.isna().sum())
    nn = s.dropna()
    distinct = int(nn.nunique())
    row = {"file": file, "column": col, "rows": n_rows, "missing": miss,
           "missing_pct": r(100 * miss / n_rows, 3), "distinct": distinct}
    bins, top_local = [], []
    key = f"{file}:{col}"

    if pd.api.types.is_datetime64_any_dtype(nn):
        row["kind"] = "date"
        row["min"] = str(nn.min().date())
        row["max"] = str(nn.max().date())
        m = nn.dt.to_period("M").value_counts().sort_index()
        for i, (p, c) in enumerate(m.items()):
            bins.append({"key": key, "kind": "month", "order": i, "label": str(p), "count": int(c),
                         "pct": r(100 * c / len(nn), 3)})
        return row, bins, top_local

    if col in TEXT:
        row["kind"] = "text"
        ln = nn.astype(str).str.len()
        row.update(mean=r(ln.mean(), 1), p50=r(ln.median(), 1), max=r(ln.max(), 0), note="text length (characters)")
        return row, bins, nn.sample(min(5, len(nn)), random_state=1).astype(str).tolist()

    if rows_per_id is not None:
        # identifier column: describe how many rows each id has
        row["kind"] = "id"
        q = np.quantile(rows_per_id, [0.5, 0.9, 0.99])
        row.update(id_rows_mean=r(rows_per_id.mean(), 2), id_rows_p50=r(q[0], 1), id_rows_p90=r(q[1], 1),
                   id_rows_p99=r(q[2], 1), id_rows_max=int(rows_per_id.max()))
        for i, (lab, c) in enumerate(per_id_bins(rows_per_id)):
            bins.append({"key": key, "kind": "perid", "order": i, "label": lab, "count": c,
                         "pct": r(100 * c / len(rows_per_id), 3)})
        top_local = nn.value_counts().head(10).items()
        return row, bins, list(top_local)

    numeric = pd.api.types.is_numeric_dtype(nn) and col not in {"sales_channel_id", "FN", "Active"} \
        and not col.endswith(("_no", "_code", "_id")) and col != "product_code"
    if numeric:
        row["kind"] = "numeric"
        x = nn.astype("float64").to_numpy()
        qv = np.quantile(x, QS)
        row.update(mean=r(x.mean(), 5), std=r(x.std(), 5), min=r(x.min(), 5), max=r(x.max(), 5),
                   **{f"p{int(q * 100):02d}": r(v, 5) for q, v in zip(QS, qv)}, zeros=int((x == 0).sum()))
        hi = qv[-1]
        lo = x.min()
        edges = np.linspace(lo, hi, 31)
        cnt, _ = np.histogram(x[x <= hi], bins=edges)
        for i, c in enumerate(cnt):
            bins.append({"key": key, "kind": "hist", "order": i,
                         "label": f"{edges[i]:.4g}–{edges[i + 1]:.4g}", "lo": r(edges[i], 6),
                         "hi": r(edges[i + 1], 6), "count": int(c), "pct": r(100 * c / len(x), 3)})
        over = int((x > hi).sum())
        bins.append({"key": key, "kind": "hist", "order": 30, "label": f">{hi:.4g} (top 1%)", "lo": r(hi, 6),
                     "hi": r(x.max(), 6), "count": over, "pct": r(100 * over / len(x), 3)})
        return row, bins, top_local

    row["kind"] = "category"
    vc = nn.astype(str).value_counts()
    top = vc.head(12)
    for i, (v, c) in enumerate(top.items()):
        bins.append({"key": key, "kind": "top", "order": i, "label": v, "count": int(c),
                     "pct": r(100 * c / len(nn), 3)})
    rest = int(vc.iloc[12:].sum())
    if rest:
        bins.append({"key": key, "kind": "top", "order": 12, "label": f"other ({len(vc) - 12:,} values)",
                     "count": rest, "pct": r(100 * rest / len(nn), 3)})
    row["top1"] = str(top.index[0])
    row["top1_pct"] = r(100 * top.iloc[0] / len(nn), 2)
    return row, bins, list(top.items())


def sheet_table(ws_rows, title):
    """Find the table under a row whose first cell is `title`; return a DataFrame."""
    for i, rr in enumerate(ws_rows):
        if rr and rr[0] == title:
            head = [h for h in ws_rows[i + 1] if h is not None]
            data = []
            for rr2 in ws_rows[i + 2:]:
                if not rr2 or rr2[0] is None:
                    break
                data.append(list(rr2[:len(head)]))
            return pd.DataFrame(data, columns=head)
    raise KeyError(title)


def records(df, nd=3):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].round(nd)
    return json.loads(df.to_json(orient="records"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tx, cust_cache, _ = common.load()
    cust = pd.read_csv(RAW / "customers.csv", dtype={"age": "float32"})
    art = pd.read_csv(RAW / "articles.csv", dtype={"article_id": "string"})
    dic = pd.read_csv(DICT, encoding="utf-8-sig")

    cols, bins, local = [], [], {}

    def add(file, col, s, n, per=None):
        row, b, extra = profile(file, col, s, n, per)
        cols.append(row)
        bins.extend(b)
        local[(file, col)] = extra
        print("profiled", file, col, flush=True)

    n_tx = len(tx)
    add("transactions_train.csv", "t_dat", tx["t_dat"], n_tx)
    per_c = np.bincount(tx["c"].to_numpy())
    per_c = per_c[per_c > 0]
    add("transactions_train.csv", "customer_id", tx["c"], n_tx, per_c)
    per_a = tx["article_id"].value_counts().to_numpy()
    add("transactions_train.csv", "article_id", tx["article_id"], n_tx, per_a)
    add("transactions_train.csv", "price", tx["price"], n_tx)
    add("transactions_train.csv", "sales_channel_id", tx["sales_channel_id"], n_tx)

    n_c = len(cust)
    for col in cust.columns:
        per = None
        if col == "customer_id":
            per = np.ones(n_c, dtype=int)
        elif col == "postal_code":
            per = cust["postal_code"].value_counts().to_numpy()
        add("customers.csv", col, cust[col], n_c, per)

    n_a = len(art)
    for col in art.columns:
        per = None
        if col == "article_id":
            per = np.ones(n_a, dtype=int)
        add("articles.csv", col, art[col], n_a, per)

    # join dictionary text
    d = dic.set_index(["file", "column"])
    for row in cols:
        k = (row["file"], row["column"])
        if k in d.index:
            e = d.loc[k]
            row.update(type=e["type"], description_en=e["description_en"], description_ko=e["description_ko"],
                       row_unit=e["row_unit"], used_in_analysis=None if pd.isna(e["used_in_analysis"]) else e["used_in_analysis"])
        row["in_dictionary"] = k in d.index

    # ---- recomputed aggregates for the artifact ----
    cust_cache = cust_cache.reset_index(drop=True)
    age_band = cust_cache["age_band"].astype("object").to_numpy()
    band = pd.Series(age_band[tx["c"].to_numpy()])
    store = (tx["sales_channel_id"].to_numpy() != common.ONLINE)
    age_tbl = pd.DataFrame({"age_band": band, "store": store}).groupby("age_band", dropna=False).agg(
        rows=("store", "size"), store_rows=("store", "sum")).reset_index()
    age_tbl["age_band"] = age_tbl["age_band"].fillna("unknown")
    age_tbl["store_share_pct"] = 100 * age_tbl["store_rows"] / age_tbl["rows"]
    age_tbl["row_share_pct"] = 100 * age_tbl["rows"] / age_tbl["rows"].sum()
    order = common.AGE_LABELS + ["unknown"]
    age_tbl = age_tbl.set_index("age_band").reindex(order).reset_index()

    overview = [
        {"file": "transactions_train.csv", "grain": "one item bought", "rows": n_tx, "columns": 5,
         "first": str(tx["t_dat"].min().date()), "last": str(tx["t_dat"].max().date()),
         "customers": int(len(per_c)), "articles": int(len(per_a)),
         "online_row_share_pct": r(100 * (~store).mean(), 2)},
        {"file": "customers.csv", "grain": "one registered customer", "rows": n_c, "columns": cust.shape[1]},
        {"file": "articles.csv", "grain": "one article (product variant)", "rows": n_a, "columns": art.shape[1]},
    ]

    # ---- workbook tables ----
    wb = openpyxl.load_workbook(WB, read_only=True, data_only=True)
    rows_of = {ws.title: [list(x) for x in ws.iter_rows(values_only=True)] for ws in wb.worksheets}
    an = {
        "monthly": sheet_table(rows_of["C1_01_Monthly"], "By month"),
        "newcust": sheet_table(rows_of["C1_03_NewCustomers"], "By month"),
        "frequency": sheet_table(rows_of["C1_05_Frequency"], "Purchase occasion bands"),
        "chantype": sheet_table(rows_of["C1_06_ChannelType"], "Channel type"),
        "basket": sheet_table(rows_of["C1_07_Basket"], "Channel used that day"),
        "cohort": sheet_table(rows_of["C2_U2_Repurchase"], "30-, 90- and 365-day repurchase rate by first-purchase month"),
        "km": sheet_table(rows_of["C2_U2_Repurchase"],
                          "Survival curve (Kaplan–Meier): share returned by day d, and chance of returning in the next 30 days"),
        "firstbasket": sheet_table(rows_of["C2_U2_Repurchase"], "By items in the first basket"),
        "firstchannel": sheet_table(rows_of["C2_U2_Repurchase"], "By first-purchase channel"),
        "lapse": sheet_table(rows_of["C2_U4_ChannelShift"], "Y2 type distribution by Y1 channel type (%)"),
        "closure": sheet_table(rows_of["C2_U4_ChannelShift"],
                               "By channel type in 2019-09-20 to 2020-02: behaviour during closures (2020-03-15 to 05-31) and after reopening (2020-06 on)"),
    }
    an["agestore"] = age_tbl
    an["overview"] = pd.DataFrame(overview)

    with open(OUT / "profile_columns.json", "w", encoding="utf-8") as f:
        json.dump(cols, f, ensure_ascii=False)
    with open(OUT / "profile_bins.json", "w", encoding="utf-8") as f:
        json.dump(bins, f, ensure_ascii=False)
    for k, df in an.items():
        with open(OUT / f"analysis_{k}.json", "w", encoding="utf-8") as f:
            json.dump(records(df), f, ensure_ascii=False)

    write_local_html(cols, bins, local, overview)
    print("wrote", OUT)


def bar_rows(rows):
    if not rows:
        return ""
    m = max(b["count"] for b in rows) or 1
    out = ['<table class="bars">']
    for b in rows:
        w = 100 * b["count"] / m
        out.append(f'<tr><td class="l">{html.escape(str(b["label"]))}</td><td class="b"><span style="width:{w:.1f}%"></span></td>'
                   f'<td class="n">{b["count"]:,}</td><td class="n">{b["pct"]:.2f}%</td></tr>')
    out.append("</table>")
    return "".join(out)


def write_local_html(cols, bins, local, overview):
    by_key = {}
    for b in bins:
        by_key.setdefault(b["key"], []).append(b)
    samples = {
        "transactions_train.csv": pd.read_csv(RAW / "transactions_train.csv", nrows=8, dtype=str),
        "customers.csv": pd.read_csv(RAW / "customers.csv", dtype=str).sample(8, random_state=7),
        "articles.csv": pd.read_csv(RAW / "articles.csv", dtype=str).sample(6, random_state=7),
    }
    css = """
    :root{--bg:#f6f7f9;--fg:#1b2230;--mut:#5b6678;--line:#d9dee7;--acc:#2f5d8c;--panel:#fff}
    @media (prefers-color-scheme:dark){:root{--bg:#12161d;--fg:#e6e9ef;--mut:#9aa4b4;--line:#2a313d;--acc:#7fa8d6;--panel:#1a2029}}
    body{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,-apple-system,"Segoe UI","Malgun Gothic",sans-serif;margin:0;padding:24px max(16px,4vw)}
    h1{font-size:24px;margin:0 0 4px} h2{font-size:19px;margin:32px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
    h3{font-size:15px;margin:0 0 6px} .mut{color:var(--mut)} .warn{background:#fff3cd;color:#5c4400;padding:8px 12px;border-radius:6px}
    .col{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;margin:10px 0}
    .grid{display:grid;grid-template-columns:minmax(220px,1fr) 2fr;gap:16px} @media(max-width:800px){.grid{grid-template-columns:1fr}}
    table{border-collapse:collapse;font-variant-numeric:tabular-nums} td,th{padding:2px 8px;text-align:left;border-bottom:1px solid var(--line)}
    .scroll{overflow-x:auto} .bars td{border:0;padding:1px 6px} .bars .l{max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .bars .b{width:220px} .bars .b span{display:block;height:10px;background:var(--acc);border-radius:2px} .n{text-align:right}
    code{font-size:12px}
    """
    h = [f"<!doctype html><meta charset='utf-8'><title>H&M data profile (local)</title><style>{css}</style>",
         "<h1>H&amp;M Kaggle data profile</h1>",
         "<p class='warn'>Local file. It includes raw sample rows from the Kaggle data, whose licence allows no redistribution. "
         "Keep it in data/ (gitignored) and do not upload or share it.</p>",
         "<h2>Files</h2><div class='scroll'><table><tr><th>file</th><th>grain</th><th>rows</th><th>columns</th></tr>"]
    for o in overview:
        h.append(f"<tr><td>{html.escape(o['file'])}</td><td>{html.escape(o['grain'])}</td><td class='n'>{o['rows']:,}</td><td class='n'>{o['columns']}</td></tr>")
    h.append("</table></div>")
    for file, df in samples.items():
        h.append(f"<h2>{html.escape(file)}</h2><h3>Sample rows</h3><div class='scroll'>{df.to_html(index=False, border=0, escape=True)}</div>")
        for c in [c for c in cols if c["file"] == file]:
            stats = {k: v for k, v in c.items() if k not in ("file", "column", "description_en", "description_ko",
                                                               "row_unit", "used_in_analysis", "in_dictionary", "type")}
            st = "".join(f"<tr><td>{html.escape(str(k))}</td><td class='n'>{html.escape(f'{v:,}' if isinstance(v, int) else str(v))}</td></tr>"
                         for k, v in stats.items())
            extra = local.get((file, c["column"]))
            ex = ""
            if extra and c["kind"] in ("id", "category"):
                ex = "<h3>Most frequent values</h3><table>" + "".join(
                    f"<tr><td><code>{html.escape(str(v))}</code></td><td class='n'>{n:,}</td></tr>" for v, n in extra) + "</table>"
            elif extra and c["kind"] == "text":
                ex = "<h3>Random examples</h3>" + "".join(f"<p class='mut'>{html.escape(t)}</p>" for t in extra)
            desc = html.escape(str(c.get("description_en") or ""))
            h.append(f"<div class='col'><h3><code>{html.escape(c['column'])}</code> <span class='mut'>{html.escape(c['kind'])} · {desc}</span></h3>"
                     f"<div class='grid'><div><table>{st}</table>{ex}</div><div>{bar_rows(by_key.get(file + ':' + c['column'], []))}</div></div></div>")
    with open(OUT / "hm_profile.html", "w", encoding="utf-8") as f:
        f.write("".join(h))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
