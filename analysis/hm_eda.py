"""H&M exploratory data analysis: distributions and outliers.

Complements hm_phase1.py. Reads the same Kaggle CSVs from data/hm/ (run
hm_phase1.py first if they are missing).

Run from anywhere:
    python analysis/hm_eda.py

Output: analysis/hm_eda_results.json (all numbers, used for the charts in the
exploration docs) and analysis/hm_eda_results.md (readable summary).
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "hm"
OUT_JSON = ROOT / "analysis" / "hm_eda_results.json"
OUT_MD = ROOT / "analysis" / "hm_eda_results.md"
CHARTS = ROOT / "analysis" / "eda_charts"

QUANTILES = [0.5, 0.75, 0.9, 0.99, 0.999]
ITEM_BINS = [1, 2, 6, 11, 21, 51, 101, 201, 501, np.inf]
ITEM_LABELS = ["1", "2-5", "6-10", "11-20", "21-50", "51-100", "101-200", "201-500", "501+"]
BASKET_BINS = [1, 2, 3, 4, 5, 6, 11, 21, 51, np.inf]
BASKET_LABELS = ["1", "2", "3", "4", "5", "6-10", "11-20", "21-50", "51+"]
ONLINE = 2  # assumption: sales_channel_id 2 = online


def load():
    tx = pd.read_csv(
        DATA / "transactions_train.csv",
        dtype={"t_dat": "category", "customer_id": "category", "article_id": "int32",
               "price": "float32", "sales_channel_id": "int8"},
    )
    tx["t_dat"] = tx["t_dat"].cat.rename_categories(pd.to_datetime(tx["t_dat"].cat.categories))
    tx["t_dat"] = tx["t_dat"].astype("datetime64[ns]")
    cust = pd.read_csv(DATA / "customers.csv", dtype={"customer_id": "string"})
    art = pd.read_csv(DATA / "articles.csv", dtype={"article_id": "int32"},
                      usecols=["article_id", "product_type_name", "product_group_name",
                               "index_name", "index_group_name", "garment_group_name"])
    return tx, cust, art


def quantiles(s):
    q = s.quantile(QUANTILES)
    out = {f"p{int(k * 1000) / 10:g}": float(v) for k, v in q.items()}
    out.update(min=float(s.min()), max=float(s.max()), mean=float(s.mean()))
    return out


def binned(s, bins, labels):
    counts = pd.cut(s, bins, right=False, labels=labels).value_counts().reindex(labels)
    return [{"bin": b, "count": int(c), "share": float(c / counts.sum() * 100)} for b, c in counts.items()]


# ---------------------------------------------------------------- daily volume

def daily(tx):
    d = tx.groupby("t_dat").size().rename("n").to_frame()
    # Outlier days: far from the median of the surrounding 4 weeks.
    med = d["n"].rolling(29, center=True, min_periods=8).median()
    d["ratio"] = d["n"] / med
    d["weekday"] = d.index.dayofweek
    top = d.sort_values("n", ascending=False).head(10)
    spikes = d[d["ratio"] >= 1.8].sort_values("ratio", ascending=False)
    dips = d[d["ratio"] <= 0.5].sort_values("ratio")
    full = pd.date_range(d.index.min(), d.index.max())
    weekday = d.groupby("weekday")["n"].mean()

    def rows(frame):
        return [{"date": str(i.date()), "n": int(r.n), "ratio": round(float(r.ratio), 2)} for i, r in frame.iterrows()]

    return {
        "series": [{"date": str(i.date()), "n": int(r.n)} for i, r in d.iterrows()],
        "days_with_data": len(d),
        "calendar_days": len(full),
        "missing_days": [str(x.date()) for x in full.difference(d.index)],
        "mean": float(d["n"].mean()),
        "median": float(d["n"].median()),
        "top10": rows(top),
        "spikes": rows(spikes),
        "dips": rows(dips),
        "weekday_mean": [{"weekday": int(k), "n": float(v)} for k, v in weekday.items()],
    }


# ---------------------------------------------------------------- customers

def per_customer(tx, cust):
    items = tx.groupby("customer_id", observed=True).size()
    top = items.sort_values(ascending=False).head(10)
    q99 = items.quantile(0.99)
    heavy = items[items > q99]
    return {
        "items": quantiles(items),
        "items_bins": binned(items, ITEM_BINS, ITEM_LABELS),
        "top10_items": [int(v) for v in top.values],
        "heavy_p99_threshold": float(q99),
        "heavy_customers": len(heavy),
        "heavy_share_of_rows": float(heavy.sum() / len(tx) * 100),
        "registered_without_purchase": int(len(cust) - len(items)),
    }


def baskets(tx):
    # A basket = one customer on one day; rows are single items.
    b = tx.groupby(["customer_id", "t_dat"], observed=True).size()
    b = b[b > 0]
    same = tx.duplicated(["customer_id", "t_dat", "article_id"]).sum()
    return {
        "basket_items": quantiles(b),
        "basket_bins": binned(b, BASKET_BINS, BASKET_LABELS),
        "baskets": len(b),
        "duplicate_item_rows": int(same),
        "duplicate_item_share": float(same / len(tx) * 100),
    }


def price(tx):
    p = tx["price"]
    q1, q3 = p.quantile([0.25, 0.75])
    upper = q3 + 1.5 * (q3 - q1)
    # Log-spaced histogram so the long right tail stays visible.
    edges = np.logspace(np.log10(p.min()), np.log10(p.max()), 31)
    counts, _ = np.histogram(p, bins=edges)
    by_channel = tx.groupby("sales_channel_id")["price"].median()
    return {
        "price": quantiles(p),
        "iqr_upper": float(upper),
        "above_iqr_upper": int((p > upper).sum()),
        "above_iqr_upper_share": float((p > upper).mean() * 100),
        "max_over_median": float(p.max() / p.median()),
        "hist": [{"lo": float(a), "hi": float(b), "count": int(c)}
                 for a, b, c in zip(edges[:-1], edges[1:], counts)],
        "median_by_channel": {int(k): float(v) for k, v in by_channel.items()},
    }


def customer_fields(cust):
    age = cust["age"]
    hist = age.value_counts().sort_index()

    def counts(col):
        v = cust[col].fillna("(missing)").astype(str).value_counts()
        return [{"value": k, "count": int(c), "share": float(c / len(cust) * 100)} for k, c in v.items()]

    return {
        "age": quantiles(age.dropna()),
        "age_hist": [{"age": int(a), "count": int(c)} for a, c in hist.items()],
        "age_missing": int(age.isna().sum()),
        "age_90_plus": int((age >= 90).sum()),
        "age_peaks": [int(age[age < 35].mode().iloc[0]), int(age[age >= 35].mode().iloc[0])],
        "club_member_status": counts("club_member_status"),
        "fashion_news_frequency": counts("fashion_news_frequency"),
        "FN": counts("FN"),
        "Active": counts("Active"),
        "postal_code_top_count": int(cust["postal_code"].value_counts().iloc[0]),
        "postal_codes": int(cust["postal_code"].nunique()),
    }


# ---------------------------------------------------------------- articles

def articles(tx, art):
    sold = tx.groupby("article_id").size().rename("n")
    a = art.set_index("article_id").join(sold).fillna({"n": 0})
    by_index = a.groupby("index_name")["n"].sum().sort_values(ascending=False)
    by_group = a.groupby("product_group_name")["n"].sum().sort_values(ascending=False)
    by_type = a.groupby("product_type_name")["n"].sum().sort_values(ascending=False).head(10)
    ranked = a["n"].sort_values(ascending=False)
    total = ranked.sum()
    top1 = ranked.head(int(len(ranked) * 0.01)).sum() / total * 100
    top10 = ranked.head(int(len(ranked) * 0.10)).sum() / total * 100
    # Channel mix by product line: does the online share differ?
    t = tx[["article_id", "sales_channel_id"]].merge(art[["article_id", "index_name"]], on="article_id")
    online_by_index = t.groupby("index_name")["sales_channel_id"].apply(lambda s: (s == ONLINE).mean() * 100)

    def share(series):
        return [{"name": k, "n": int(v), "share": float(v / total * 100)} for k, v in series.items()]

    return {
        "articles": len(a),
        "never_sold": int((a["n"] == 0).sum()),
        "sold_once": int((a["n"] == 1).sum()),
        "top1pct_share": float(top1),
        "top10pct_share": float(top10),
        "max_sold": int(ranked.iloc[0]),
        "by_index": share(by_index),
        "by_product_group": share(by_group),
        "top_product_types": share(by_type),
        "online_share_by_index": {k: float(v) for k, v in online_by_index.items()},
    }


# ---------------------------------------------------------------- chart data

def write_chart_csvs(r):
    """CSVs uploaded to the exploration docs for the daily, age and price charts."""
    CHARTS.mkdir(parents=True, exist_ok=True)
    d = pd.DataFrame(r["daily"]["series"])
    med = d["n"].rolling(29, center=True, min_periods=8).median()
    d["ratio"] = (d["n"] / med).round(2)
    d.to_csv(CHARTS / "daily.csv", index=False)
    pd.DataFrame(r["customer_fields"]["age_hist"]).to_csv(CHARTS / "age_hist.csv", index=False)
    pd.DataFrame(r["price"]["hist"]).to_csv(CHARTS / "price_hist.csv", index=False)


# ---------------------------------------------------------------- report

def report(r):
    L = ["# H&M exploratory analysis: distributions and outliers\n",
         "Generated by `analysis/hm_eda.py`. All numbers are also in `hm_eda_results.json`.\n"]
    w = L.append
    d = r["daily"]
    w("## Daily volume\n")
    w(f"- {d['days_with_data']} days with data out of {d['calendar_days']} calendar days; missing: {', '.join(d['missing_days']) or 'none'}.")
    w(f"- Mean {d['mean']:,.0f} rows a day, median {d['median']:,.0f}.")
    w("- Spike days (at least 1.8x the 4-week median): " + ", ".join(f"{x['date']} ({x['n']:,}, {x['ratio']}x)" for x in d["spikes"]))
    w("- Dip days (at most 0.5x): " + (", ".join(f"{x['date']} ({x['n']:,}, {x['ratio']}x)" for x in d["dips"]) or "none") + "\n")

    c = r["customers"]
    w("## Items per customer (2 years)\n")
    w("| Stat | Value |\n|---|---|")
    for k, v in c["items"].items():
        w(f"| {k} | {v:,.1f} |")
    w(f"\nTop 10 customers by rows: {', '.join(f'{x:,}' for x in c['top10_items'])}. "
      f"The top 1% (over {c['heavy_p99_threshold']:.0f} rows) account for {c['heavy_share_of_rows']:.1f}% of all rows. "
      f"{c['registered_without_purchase']:,} registered customers never bought.\n")

    b = r["baskets"]
    w("## Items per basket (customer x day)\n")
    w("| Stat | Value |\n|---|---|")
    for k, v in b["basket_items"].items():
        w(f"| {k} | {v:,.1f} |")
    w(f"\n{b['duplicate_item_rows']:,} rows ({b['duplicate_item_share']:.1f}%) repeat the same article for the same customer on the same day, i.e. quantity above 1.\n")

    p = r["price"]
    w("## Price (transformed units)\n")
    w("| Stat | Value |\n|---|---|")
    for k, v in p["price"].items():
        w(f"| {k} | {v:.4f} |")
    w(f"\nIQR rule upper fence {p['iqr_upper']:.4f}: {p['above_iqr_upper']:,} rows ({p['above_iqr_upper_share']:.1f}%) above it. "
      f"Max is {p['max_over_median']:.0f}x the median. Median by channel: {p['median_by_channel']}.\n")

    f = r["customer_fields"]
    w("## Customer fields\n")
    w(f"- Age: missing {f['age_missing']:,}; peaks at {f['age_peaks'][0]} and {f['age_peaks'][1]}; {f['age_90_plus']:,} customers aged 90 or more; max {f['age']['max']:.0f}.")
    for col in ["club_member_status", "fashion_news_frequency", "FN", "Active"]:
        w(f"- {col}: " + ", ".join(f"{x['value']} {x['share']:.1f}%" for x in f[col]))
    w(f"- Postal codes: {f['postal_codes']:,} distinct; the most common one is shared by {f['postal_code_top_count']:,} customers (likely a placeholder).\n")

    a = r["articles"]
    w("## Articles\n")
    w(f"- {a['articles']:,} articles; {a['never_sold']:,} never sold in the window, {a['sold_once']:,} sold once; best seller {a['max_sold']:,} rows.")
    w(f"- Top 1% of articles = {a['top1pct_share']:.1f}% of rows; top 10% = {a['top10pct_share']:.1f}%.")
    w("- Rows by product line: " + ", ".join(f"{x['name']} {x['share']:.1f}%" for x in a["by_index"]))
    w("- Online share by product line: " + ", ".join(f"{k} {v:.1f}%" for k, v in sorted(a["online_share_by_index"].items(), key=lambda kv: -kv[1])))
    text = "\n".join(L) + "\n"
    print(text)
    OUT_MD.write_text(text, encoding="utf-8")


def main():
    tx, cust, art = load()
    print(f"loaded {len(tx):,} transactions, {len(cust):,} customers, {len(art):,} articles")
    r = {
        "daily": daily(tx),
        "customers": per_customer(tx, cust),
        "baskets": baskets(tx),
        "price": price(tx),
        "customer_fields": customer_fields(cust),
        "articles": articles(tx, art),
    }
    OUT_JSON.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    write_chart_csvs(r)
    report(r)
    print(f"saved {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
