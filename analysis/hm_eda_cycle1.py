"""H&M EDA cycle 1: broad, hypothesis-free pass to find question candidates.

Each function returns one table (a DataFrame). run() returns them all in a dict
keyed by a short table id, which hm_eda_workbook.py writes to the results file.
"""

import numpy as np
import pandas as pd

from hm_eda_common import ONLINE

FREQ_BINS = [1, 2, 3, 5, 10, 20, 50, np.inf]
FREQ_LABELS = ["1", "2", "3-4", "5-9", "10-19", "20-49", "50+"]


def add_keys(tx):
    tx["m"] = tx["t_dat"].dt.to_period("M")
    tx["on"] = tx["sales_channel_id"].eq(ONLINE)


def monthly(tx):
    g = tx.groupby("m")
    out = pd.DataFrame({
        "rows": g.size(),
        "value": g["price"].sum(),
        "customers": g["c"].nunique(),
        "avg_price": g["price"].mean(),
        "online_row_share": g["on"].mean() * 100,
    })
    out["rows_per_customer"] = out["rows"] / out["customers"]
    out["value_yoy_pct"] = (out["value"] / out["value"].shift(12) - 1) * 100
    out["customers_yoy_pct"] = (out["customers"] / out["customers"].shift(12) - 1) * 100
    out.index = out.index.astype(str)
    return out.reset_index(names="month")


def weekday(tx):
    d = tx.groupby("t_dat").agg(rows=("price", "size"), online=("on", "mean"))
    d["weekday"] = d.index.dayofweek
    out = d.groupby("weekday").agg(avg_rows=("rows", "mean"), online_row_share=("online", "mean"))
    out["online_row_share"] *= 100
    out.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return out.reset_index(names="weekday")


def occasions(tx):
    """One row per customer x day with its channel mix and value."""
    occ = tx.groupby(["c", "t_dat"], sort=False).agg(
        items=("price", "size"), value=("price", "sum"), on=("on", "max"), off=("on", "min"))
    occ = occ.reset_index()
    occ["store"] = ~occ["off"]  # at least one store row that day
    return occ.drop(columns="off")


def new_vs_returning(occ):
    first = occ.groupby("c")["t_dat"].transform("min")
    occ = occ.assign(m=occ["t_dat"].dt.to_period("M"), new=occ["t_dat"].eq(first))
    g = occ.groupby("m")
    out = pd.DataFrame({
        "active_customers": g["c"].nunique(),
        "new_customers": occ[occ["new"]].groupby("m")["c"].nunique(),
        "occasions": g.size(),
    })
    out["new_share_pct"] = out["new_customers"] / out["active_customers"] * 100
    out.index = out.index.astype(str)
    return out.reset_index(names="month")


def cohort_matrix(occ):
    """Share of each first-purchase-month cohort that buys again in month k."""
    m = occ["t_dat"].dt.to_period("M")
    first = m.groupby(occ["c"]).transform("min")
    k = (m - first).apply(lambda x: x.n)
    df = pd.DataFrame({"cohort": first, "k": k, "c": occ["c"]}).drop_duplicates()
    size = df[df["k"] == 0].groupby("cohort")["c"].nunique()
    active = df.groupby(["cohort", "k"])["c"].nunique().unstack()
    pct = active.div(size, axis=0) * 100
    pct = pct[[c for c in pct.columns if 0 < c <= 12]]
    pct.columns = [f"M+{c}" for c in pct.columns]
    pct.insert(0, "cohort_size", size)
    pct.index = pct.index.astype(str)
    return pct.reset_index(names="cohort")


def frequency(occ):
    n = occ.groupby("c").size()
    v = occ.groupby("c")["value"].sum()
    band = pd.cut(n, FREQ_BINS, right=False, labels=FREQ_LABELS)
    out = pd.DataFrame({"customers": n.groupby(band, observed=False).size(),
                        "value": v.groupby(band, observed=False).sum()})
    out["customer_share_pct"] = out["customers"] / out["customers"].sum() * 100
    out["value_share_pct"] = out["value"] / out["value"].sum() * 100
    return out.reset_index(names="purchase_occasions")


def channel_mix(occ):
    """Customers by the channels they ever used."""
    g = occ.groupby("c").agg(on=("on", "max"), store=("store", "max"),
                             occ=("t_dat", "size"), value=("value", "sum"), items=("items", "sum"))
    g["type"] = np.select([g["on"] & g["store"], g["on"]], ["omni", "online only"], "store only")
    out = g.groupby("type").agg(customers=("occ", "size"), avg_occasions=("occ", "mean"),
                                avg_value=("value", "mean"), median_value=("value", "median"),
                                value=("value", "sum"), items=("items", "sum"), occasions=("occ", "sum"))
    out["items_per_occasion"] = out["items"] / out["occasions"]
    out = out.drop(columns=["items", "occasions"])
    out["customer_share_pct"] = out["customers"] / out["customers"].sum() * 100
    out["value_share_pct"] = out["value"] / out["value"].sum() * 100
    return out.reset_index(names="channel_type"), g["type"]


def basket_by_channel(occ):
    occ = occ.assign(kind=np.select([occ["on"] & occ["store"], occ["on"]], ["both", "online"], "store"))
    out = occ.groupby("kind").agg(occasions=("items", "size"), avg_items=("items", "mean"),
                                  median_items=("items", "median"), avg_value=("value", "mean"))
    return out.reset_index(names="day_channel")


def age_profile(tx, cust, ctype):
    c = cust.set_index("c")
    per = tx.groupby("c").agg(rows=("price", "size"), value=("price", "sum"), on=("on", "mean"),
                              avg_price=("price", "mean"))
    per = per.join(c[["age_band", "club_member_status", "fashion_news_frequency"]]).join(ctype)
    g = per.groupby("age_band", observed=True)
    out = pd.DataFrame({
        "customers": g.size(),
        "rows_per_customer": g["rows"].mean(),
        "value_per_customer": g["value"].mean(),
        "avg_price": g["value"].sum() / g["rows"].sum(),
        "online_row_share_pct": g["on"].mean() * 100,
        "omni_share_pct": g["type"].apply(lambda s: (s == "omni").mean() * 100),
    })
    return out.reset_index(names="age_band"), per


def member_profile(per):
    rows = []
    for col, short in [("club_member_status", "club"), ("fashion_news_frequency", "news")]:
        g = per.groupby(per[col].fillna("(missing)"))
        t = pd.DataFrame({"customers": g.size(), "rows_per_customer": g["rows"].mean(),
                          "value_per_customer": g["value"].mean(), "online_row_share_pct": g["on"].mean() * 100})
        t = t.reset_index(names="value_label")
        t.insert(0, "field", col)
        t.insert(0, "segment", short + ": " + t["value_label"].astype(str))
        rows.append(t)
    return pd.concat(rows, ignore_index=True)


def product_line_trend(tx, art):
    a = art.set_index("article_id")["index_group_name"]
    grp = a.reindex(tx["article_id"]).to_numpy()
    t = pd.DataFrame({"m": tx["m"], "g": grp, "p": tx["price"]})
    v = t.groupby(["m", "g"])["p"].sum().unstack()
    share = v.div(v.sum(axis=1), axis=0) * 100
    share.index = share.index.astype(str)
    return share.reset_index(names="month")


def seasonality(tx, art):
    """Calendar-month share of each product group's rows (higher = more seasonal)."""
    a = art.set_index("article_id")["product_group_name"]
    t = pd.DataFrame({"mon": tx["t_dat"].dt.month, "g": a.reindex(tx["article_id"]).to_numpy()})
    # Exactly one of each calendar month, before COVID: 2018-10 to 2019-09.
    keep = (tx["t_dat"] >= "2018-10-01") & (tx["t_dat"] < "2019-10-01")
    c = t[keep.to_numpy()].groupby(["g", "mon"]).size().unstack(fill_value=0)
    c = c[c.sum(axis=1) > 100_000]
    pct = c.div(c.sum(axis=1), axis=0) * 100
    pct["peak_to_trough"] = pct.max(axis=1) / pct.min(axis=1)
    pct.columns = [f"M{x:02d}" if isinstance(x, (int, np.integer)) else x for x in pct.columns]
    return pct.sort_values("peak_to_trough", ascending=False).reset_index(names="product_group")


def article_lifecycle(tx, art):
    g = tx.groupby("article_id")
    a = g.agg(first=("t_dat", "min"), last=("t_dat", "max"), rows=("price", "size"), pmed=("price", "median"))
    # 5th/95th percentiles rather than min/max so one odd row does not set the range.
    a["pmax"] = g["price"].quantile(0.95)
    a["pmin"] = g["price"].quantile(0.05)
    a["days_on_sale"] = (a["last"] - a["first"]).dt.days + 1
    a["launch_m"] = a["first"].dt.to_period("M")
    launched = a[a["first"] > tx["t_dat"].min() + pd.Timedelta(days=30)]
    by_m = launched.groupby("launch_m").agg(new_articles=("rows", "size"), avg_rows=("rows", "mean"),
                                           median_days_on_sale=("days_on_sale", "median"))
    by_m.index = by_m.index.astype(str)
    return by_m.reset_index(names="launch_month"), a


def price_dispersion(a):
    """How far the same article's price drops below its own maximum (markdown signal)."""
    s = a[a["rows"] >= 50]
    drop = (1 - s["pmin"] / s["pmax"]) * 100
    bins = [0, 10, 20, 30, 40, 50, 60, 101]
    labels = ["0-9%", "10-19%", "20-29%", "30-39%", "40-49%", "50-59%", "60%+"]
    out = drop.groupby(pd.cut(drop, bins, right=False, labels=labels), observed=False).size()
    out = out.to_frame("articles")
    out["share_pct"] = out["articles"] / out["articles"].sum() * 100
    return out.reset_index(names="max_price_drop")


def concentration(tx):
    s = tx.groupby("article_id").size().sort_values(ascending=False)
    cum = s.cumsum() / s.sum() * 100
    n = len(s)
    rows = [{"top_pct_of_articles": f"top {p:g}%", "articles": int(n * p / 100),
             "share_of_rows_pct": float(cum.iloc[max(int(n * p / 100) - 1, 0)])}
            for p in (0.1, 1, 5, 10, 20, 50)]
    return pd.DataFrame(rows)


def run(tx, cust, art):
    add_keys(tx)
    occ = occasions(tx)
    chan, ctype = channel_mix(occ)
    age, per = age_profile(tx, cust, ctype)
    life, a = article_lifecycle(tx, art)
    return {
        "monthly": monthly(tx),
        "weekday": weekday(tx),
        "new_vs_returning": new_vs_returning(occ),
        "cohort": cohort_matrix(occ),
        "frequency": frequency(occ),
        "channel_mix": chan,
        "basket_channel": basket_by_channel(occ),
        "age_profile": age,
        "member_profile": member_profile(per),
        "line_trend": product_line_trend(tx, art),
        "seasonality": seasonality(tx, art),
        "launches": life,
        "price_drop": price_dispersion(a),
        "concentration": concentration(tx),
    }, {"occ": occ, "per": per, "articles": a}
