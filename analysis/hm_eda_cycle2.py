"""H&M EDA cycle 2: targeted analysis of the union of cycle-1 question
candidates and the proposal's issue list (Issue 1-3).

Reuses the occasion and per-customer tables from cycle 1. run() returns a dict
of tables keyed by id; hm_eda_workbook.py maps them to union items U1-U9.
"""

import numpy as np
import pandas as pd

# Two comparable 12-month years inside the window.
Y1 = (pd.Timestamp("2018-09-20"), pd.Timestamp("2019-09-20"))
Y2 = (pd.Timestamp("2019-09-20"), pd.Timestamp("2020-09-23"))
# First purchases from this date have at least ~5 months of history before them,
# so most are genuinely new customers rather than returning ones seen late.
NEW_FROM = pd.Timestamp("2019-03-01")
LAST = pd.Timestamp("2020-09-22")


def in_year(s, y):
    return (s >= y[0]) & (s < y[1])


def chan_kind(on, store):
    return np.select([on & store, on], ["both", "online"], "store")


# ---------------------------------------------------------------- U1 sales decomposition

def sales_decomposition(occ):
    """Same month vs a year earlier: value = customers x occasions/customer x value/occasion."""
    m = occ["t_dat"].dt.to_period("M")
    g = occ.groupby(m)
    t = pd.DataFrame({"customers": g["c"].nunique(), "occasions": g.size(), "value": g["value"].sum(),
                      "items": g["items"].sum()})
    t["occ_per_customer"] = t["occasions"] / t["customers"]
    t["items_per_occ"] = t["items"] / t["occasions"]
    t["price_per_item"] = t["value"] / t["items"]
    rows = []
    for p in pd.period_range("2019-10", "2020-08", freq="M"):
        cur, prev = t.loc[p], t.loc[p - 12]
        r = {"month": str(p), "value_yoy_pct": (cur.value / prev.value - 1) * 100}
        for k in ["customers", "occ_per_customer", "items_per_occ", "price_per_item"]:
            r[f"{k}_yoy_pct"] = (cur[k] / prev[k] - 1) * 100
        rows.append(r)
    out = pd.DataFrame(rows)
    # Totals for the two halves: before COVID (Oct-Feb) and during/after (Mar-Aug).
    for name, months in [("Oct-Feb total", ["2019-10", "2019-11", "2019-12", "2020-01", "2020-02"]),
                         ("Mar-Aug total", ["2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08"])]:
        cur = occ[m.astype(str).isin(months)]
        prev = occ[(m + 12).astype(str).isin(months)]
        r = {"month": name}

        def parts(o):
            c = o["c"].nunique()
            return {"value": o["value"].sum(), "customers": c, "occ_per_customer": len(o) / c,
                    "items_per_occ": o["items"].sum() / len(o), "price_per_item": o["value"].sum() / o["items"].sum()}
        a, b = parts(cur), parts(prev)
        r["value_yoy_pct"] = (a["value"] / b["value"] - 1) * 100
        for k in ["customers", "occ_per_customer", "items_per_occ", "price_per_item"]:
            r[f"{k}_yoy_pct"] = (a[k] / b[k] - 1) * 100
        rows.append(r)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- U2/U3 first purchase and repurchase

def first_purchase(tx, occ, cust, art):
    """One row per customer whose first purchase is on/after NEW_FROM, with what they bought first."""
    first = occ.groupby("c")["t_dat"].min()
    first = first[first >= NEW_FROM]
    f_occ = occ.set_index("c").loc[first.index]
    f_occ = f_occ[f_occ["t_dat"] == first.reindex(f_occ.index)]
    df = pd.DataFrame({"first": first})
    df["channel"] = pd.Series(chan_kind(f_occ["on"].to_numpy(), f_occ["store"].to_numpy()), index=f_occ.index)
    df["items"] = f_occ["items"]
    # Main product line of the first basket: the index group with the most items.
    sel = tx["c"].isin(first.index).to_numpy()
    t = tx.loc[sel, ["c", "t_dat", "article_id"]]
    t = t[t["t_dat"].to_numpy() == first.reindex(t["c"]).to_numpy()]
    grp = art.set_index("article_id")["index_group_name"].reindex(t["article_id"]).to_numpy()
    main = pd.DataFrame({"c": t["c"].to_numpy(), "g": grp}).groupby(["c", "g"]).size()
    main = main.reset_index().sort_values(0, ascending=False).drop_duplicates("c").set_index("c")["g"]
    df["first_line"] = main
    c = cust.set_index("c")
    df["age_band"] = c["age_band"]
    df["club"] = c["club_member_status"].fillna("(missing)")
    df["news"] = c["fashion_news_frequency"].fillna("(missing)")
    # Days to the next purchase occasion.
    later = occ[occ["c"].isin(first.index) & (occ["t_dat"] > first.reindex(occ["c"]).to_numpy())]
    nxt = later.groupby("c")["t_dat"].min()
    df["days_to_2nd"] = (nxt - df["first"]).dt.days
    df["horizon"] = (LAST - df["first"]).dt.days
    return df


def repurchase_rate(df, by, days=(30, 90, 365)):
    out = None
    for d in days:
        sub = df[df["horizon"] >= d]
        r = sub.groupby(by, observed=True).apply(lambda x: (x["days_to_2nd"] <= d).mean() * 100)
        r.name = f"repurchase_{d}d_pct"
        n = sub.groupby(by, observed=True).size().rename(f"n_{d}d")
        part = pd.concat([n, r], axis=1)
        out = part if out is None else out.join(part, how="outer")
    return out.reset_index()


def repurchase_tables(df):
    df = df.assign(first_month=df["first"].dt.to_period("M").astype(str),
                   basket=pd.cut(df["items"], [1, 2, 4, 7, np.inf], right=False, labels=["1", "2-3", "4-6", "7+"]))
    out = {}
    for key, col in [("by_month", "first_month"), ("by_channel", "channel"), ("by_age", "age_band"),
                     ("by_basket", "basket"), ("by_line", "first_line"), ("by_club", "club"), ("by_news", "news")]:
        out[key] = repurchase_rate(df, col).rename(columns={col: "segment"})
    gap = df["days_to_2nd"].dropna()
    bins = [1, 8, 15, 31, 61, 91, 181, 366, np.inf]
    labels = ["1-7", "8-14", "15-30", "31-60", "61-90", "91-180", "181-365", "366+"]
    g = gap.groupby(pd.cut(gap, bins, right=False, labels=labels), observed=False).size().to_frame("customers")
    g["share_pct"] = g["customers"] / g["customers"].sum() * 100
    g["cum_pct"] = g["share_pct"].cumsum()
    out["gap"] = g.reset_index(names="days_to_2nd")
    return out


def new_customer_mix(df):
    """Monthly new customers and their age / channel mix."""
    m = df["first"].dt.to_period("M").astype(str)
    n = df.groupby(m).size().rename("new_customers")
    age = pd.crosstab(m, df["age_band"], normalize="index") * 100
    ch = pd.crosstab(m, df["channel"], normalize="index") * 100
    ch.columns = [f"{c}_pct" for c in ch.columns]
    out = pd.concat([n, age.round(2), ch.round(2)], axis=1)
    out["median_age_band_16_34_pct"] = age[["16-24", "25-34"]].sum(axis=1)
    return out.reset_index(names="first_month")


# ---------------------------------------------------------------- U4 channel migration

def year_profile(occ, y):
    o = occ[in_year(occ["t_dat"], y)]
    g = o.groupby("c").agg(on=("on", "max"), store=("store", "max"), occ=("t_dat", "size"), value=("value", "sum"))
    g["type"] = np.select([g["on"] & g["store"], g["on"]], ["omni", "online only"], "store only")
    return g


def channel_migration(occ):
    a, b = year_profile(occ, Y1), year_profile(occ, Y2)
    j = a[["type", "value", "occ"]].join(b[["type", "value", "occ"]], rsuffix="_y2", how="left")
    j["type_y2"] = j["type_y2"].fillna("no purchase")
    mat = pd.crosstab(j["type"], j["type_y2"], normalize="index") * 100
    mat = mat[["omni", "online only", "store only", "no purchase"]]
    mat.insert(0, "customers_y1", j.groupby("type").size())
    v = j.groupby("type").agg(value_y1=("value", "sum"), value_y2=("value_y2", "sum"))
    mat["value_y2_vs_y1_pct"] = (v["value_y2"] / v["value_y1"] - 1) * 100
    mat = mat.reset_index(names="y1_type")
    # Same Y1 type, split by Y2 type: does turning omni go with higher spend?
    s = j[j["type_y2"] != "no purchase"].groupby(["type", "type_y2"]).agg(
        customers=("value", "size"), value_y1=("value", "mean"), value_y2=("value_y2", "mean"))
    s["change_pct"] = (s["value_y2"] / s["value_y1"] - 1) * 100
    s = s.reset_index().rename(columns={"type": "y1_type"})
    s.insert(0, "path", s["y1_type"] + " → " + s["type_y2"])
    return mat, s


def channel_groups(occ, start, end):
    pre = occ[(occ["t_dat"] >= start) & (occ["t_dat"] < end)]
    g = pre.groupby("c").agg(on=("on", "max"), store=("store", "max"))
    return {"store only before": g.index[~g["on"] & g["store"]],
            "online only before": g.index[g["on"] & ~g["store"]],
            "omni before": g.index[g["on"] & g["store"]]}


def covid_store_customers(occ):
    """Customers who used only stores before the closures: what did they do during and after?

    The baseline repeats the same windows one year earlier (groups from 2018-09-20 to 2019-02-28,
    buying in 2019-06-01 to 09-22), so the reopening rate can be read against a normal summer."""
    groups = channel_groups(occ, "2019-09-20", "2020-03-01")
    base = channel_groups(occ, "2018-09-20", "2019-03-01")
    clo = occ[(occ["t_dat"] >= "2020-03-15") & (occ["t_dat"] < "2020-06-01")]
    aft = occ[(occ["t_dat"] >= "2020-06-01")]
    aft19 = occ[(occ["t_dat"] >= "2019-06-01") & (occ["t_dat"] <= "2019-09-22")]
    rows = []
    for name, ids in groups.items():
        c1 = clo[clo["c"].isin(ids)]
        c2 = aft[aft["c"].isin(ids)]
        rows.append({
            "group": name, "customers": len(ids),
            "bought_during_closure_pct": c1["c"].nunique() / len(ids) * 100,
            "bought_online_during_closure_pct": c1.loc[c1["on"], "c"].nunique() / len(ids) * 100,
            "bought_after_reopen_pct": c2["c"].nunique() / len(ids) * 100,
            "same_months_2019_pct": aft19.loc[aft19["c"].isin(base[name]), "c"].nunique() / len(base[name]) * 100,
            "after_reopen_online_occ_share_pct": c2["on"].mean() * 100 if len(c2) else np.nan,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- U5 age

def age_deep(tx, occ, cust, art):
    c = cust.set_index("c")["age_band"]
    occ = occ.assign(age=c.reindex(occ["c"]).to_numpy())
    rows = []
    for name, y in [("Y1", Y1), ("Y2", Y2)]:
        o = occ[in_year(occ["t_dat"], y)]
        v = o.groupby("age", observed=True)["value"].sum()
        n = o.groupby("age", observed=True)["c"].nunique()
        rows.append(pd.DataFrame({"year": name, "value_share_pct": v / v.sum() * 100,
                                  "customer_share_pct": n / n.sum() * 100, "customers": n}))
    yr = pd.concat(rows).reset_index(names="age_band")
    wide = yr.pivot(index="age_band", columns="year", values=["customers", "value_share_pct", "customer_share_pct"])
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    wide["customers_change_pct"] = (wide["customers_Y2"] / wide["customers_Y1"] - 1) * 100
    wide["value_share_change_pp"] = wide["value_share_pct_Y2"] - wide["value_share_pct_Y1"]
    # Product line mix by age band (share of each band's value).
    grp = art.set_index("article_id")["index_group_name"].reindex(tx["article_id"]).to_numpy()
    t = pd.DataFrame({"age": c.reindex(tx["c"]).to_numpy(), "g": grp, "p": tx["price"].to_numpy()})
    mix = t.groupby(["age", "g"], observed=True)["p"].sum().unstack()
    mix = mix.div(mix.sum(axis=1), axis=0) * 100
    return wide.reset_index(), mix.reset_index(names="age_band")


# ---------------------------------------------------------------- U6 heavy customers

def heavy_customers(occ):
    a, b = year_profile(occ, Y1), year_profile(occ, Y2)
    a = a.sort_values("value", ascending=False)
    a["decile"] = pd.qcut(np.arange(len(a)), 10, labels=[f"D{i}" for i in range(1, 11)])
    a = a.join(b[["value", "occ"]], rsuffix="_y2")
    g = a.groupby("decile", observed=True)
    out = pd.DataFrame({
        "customers": g.size(),
        "share_of_y1_value_pct": g["value"].sum() / a["value"].sum() * 100,
        "avg_occasions_y1": g["occ"].mean(),
        "active_in_y2_pct": g["value_y2"].apply(lambda s: s.notna().mean() * 100),
        "value_y2_vs_y1_pct": (g["value_y2"].sum() / g["value"].sum() - 1) * 100,
    })
    # Where Y2 value comes from: customers already buying in Y1 vs customers new in Y2.
    old = b.index.isin(a.index)
    split = pd.DataFrame([
        {"part": "Y1 total", "customers": len(a), "value": a["value"].sum()},
        {"part": "Y2 from Y1 customers", "customers": int(old.sum()), "value": b.loc[old, "value"].sum()},
        {"part": "Y2 from customers new in Y2", "customers": int((~old).sum()), "value": b.loc[~old, "value"].sum()},
        {"part": "Y2 total", "customers": len(b), "value": b["value"].sum()},
    ])
    split["vs_y1_total_pct"] = split["value"] / a["value"].sum() * 100
    return out.reset_index(), split


# ---------------------------------------------------------------- U7 product lines supply vs demand

def line_supply(tx, art):
    grp = art.set_index("article_id")["index_group_name"].reindex(tx["article_id"]).to_numpy()
    t = pd.DataFrame({"m": tx["t_dat"].dt.to_period("M").astype(str), "g": grp, "a": tx["article_id"].to_numpy()})
    g = t.groupby(["m", "g"])
    out = pd.DataFrame({"active_articles": g["a"].nunique(), "rows": g.size()})
    out["rows_per_article"] = out["rows"] / out["active_articles"]
    out = out.reset_index()
    wide = out.pivot(index="m", columns="g", values=["active_articles", "rows_per_article"])
    wide.columns = [f"{b} | {a}" for a, b in wide.columns]
    return wide.reset_index(names="month")


# ---------------------------------------------------------------- U8 membership and newsletter

def member_by_age(per):
    p = per[per["age_band"].notna()]
    rows = []
    for col, keep in [("fashion_news_frequency", ["NONE", "Regularly"]), ("club_member_status", ["ACTIVE", "PRE-CREATE"])]:
        t = p[p[col].isin(keep)].groupby(["age_band", col], observed=True)["rows"].mean().unstack()
        t.columns = [f"{col} = {c}" for c in t.columns]
        rows.append(t)
    out = pd.concat(rows, axis=1)
    return out.reset_index()


# ---------------------------------------------------------------- U9 markdown

def markdown(tx):
    """Price relative to the article's own launch price (median of its first 28 days)."""
    first = tx.groupby("article_id")["t_dat"].transform("min")
    since = (tx["t_dat"] - first).dt.days
    launch = tx["price"].where(since < 28).groupby(tx["article_id"]).transform("median")
    ok = (first >= "2018-10-20") & launch.notna()
    r = (tx["price"] / launch)[ok]
    t = pd.DataFrame({"m": tx.loc[ok, "t_dat"].dt.to_period("M").astype(str), "r": r,
                      "on": tx.loc[ok, "sales_channel_id"].eq(2), "w": (since[ok] // 28).clip(upper=12)})
    t["cut30"] = t["r"] < 0.7
    by_m = t.groupby("m").agg(rows=("r", "size"), median_ratio=("r", "median"), rows_30pct_below_pct=("cut30", "mean"))
    by_m["rows_30pct_below_pct"] *= 100
    by_m.loc["all months"] = [len(t), t["r"].median(), t["cut30"].mean() * 100]
    by_age = t.groupby("w").agg(rows=("r", "size"), median_ratio=("r", "median"), rows_30pct_below_pct=("cut30", "mean"))
    by_age["rows_30pct_below_pct"] *= 100
    by_age.index = [f"{i * 4}-{i * 4 + 3}w" if i < 12 else "48w+" for i in by_age.index]
    return by_m.reset_index(names="month"), by_age.reset_index(names="weeks_since_launch")


def run(tx, cust, art, extra):
    occ, per = extra["occ"], extra["per"]
    fp = first_purchase(tx, occ, cust, art)
    rep = repurchase_tables(fp)
    mig, mig_value = channel_migration(occ)
    age_years, age_mix = age_deep(tx, occ, cust, art)
    md_month, md_age = markdown(tx)
    heavy, y_split = heavy_customers(occ)
    out = {
        "decomp": sales_decomposition(occ),
        "new_mix": new_customer_mix(fp),
        "migration": mig,
        "migration_value": mig_value,
        "covid_store": covid_store_customers(occ),
        "age_years": age_years,
        "age_mix": age_mix,
        "heavy": heavy,
        "y_split": y_split,
        "line_supply": line_supply(tx, art),
        "member_age": member_by_age(per),
        "md_month": md_month,
        "md_age": md_age,
    }
    out.update({f"rep_{k}": v for k, v in rep.items()})
    return out
