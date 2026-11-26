"""Formal tests for the presentation findings, in the course's method-selection style.

For each finding: one row = ?, dependent variable, predictors and controls with reference
categories, expectations stated before fitting, the starting method from the course guide,
effect sizes with 95% confidence intervals, diagnostics and one interpretation trap.

  M1  Binary logistic regression: 90-day repurchase of new customers (findings 1 and 3)
  M2  Binary logistic regression: no purchase in year 2 (supporting A)
  T1  Chi-square: first-purchase month x 90-day repurchase (finding 1)
  T2  Chi-square: pre-closure channel type x bought online in closures (finding 4)
  T3  Two-proportion comparison: store-only customers buying after reopening vs a year earlier
  T4  One-way ANOVA (+ Kruskal-Wallis): per-customer in-store share by age band (supporting B)

Writes analysis/hm_tests_results.md and analysis/hm_tests_results.json (aggregates only).
Run: py -I analysis/hm_tests.py   (uses the parquet cache in data/hm/)
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hm_eda_common as common  # noqa: E402
import hm_eda_cycle1 as c1  # noqa: E402
import hm_eda_cycle2 as c2  # noqa: E402

OUT = Path(__file__).resolve().parent
T0 = time.time()
RES = {}


def log(*a):
    print(f"[{time.time() - T0:6.0f}s]", *a, flush=True)


def ci_prop_diff(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p1 - p2
    return d * 100, (d - 1.96 * se) * 100, (d + 1.96 * se) * 100


def cramers_v(tab):
    chi2, p, dof, _ = stats.chi2_contingency(tab, correction=False)
    n = tab.to_numpy().sum()
    k = min(tab.shape) - 1
    return chi2, p, dof, float(np.sqrt(chi2 / (n * k)))


def auc(y, p):
    # Mann-Whitney form of the area under the ROC curve
    r = stats.rankdata(p)
    n1 = y.sum()
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def or_table(fit, keep):
    ci = fit.conf_int()
    rows = []
    for term in fit.params.index:
        if not any(k in term for k in keep):
            continue
        rows.append({"term": term, "coef": float(fit.params[term]), "odds_ratio": float(np.exp(fit.params[term])),
                     "ci_low": float(np.exp(ci.loc[term, 0])), "ci_high": float(np.exp(ci.loc[term, 1])),
                     "p": float(fit.pvalues[term])})
    return rows


def adjusted_prob(fit, df, var, levels):
    """Average predicted probability with `var` set to each level for everyone (g-computation)."""
    out = {}
    for lv in levels:
        d = df.copy()
        d[var] = pd.Categorical([lv] * len(d), categories=df[var].cat.categories)
        out[str(lv)] = float(fit.predict(d).mean() * 100)
    return out


def vif_from_fit(fit):
    X = fit.model.exog
    names = fit.model.exog_names
    rows = []
    for i, nm in enumerate(names):
        if nm == "Intercept":
            continue
        rows.append((nm, float(variance_inflation_factor(X, i))))
    return max(rows, key=lambda r: r[1])


def main():
    tx, cust, art = common.load()
    c1.add_keys(tx)
    log("loaded", len(tx))
    occ = c1.occasions(tx)
    log("occasions", len(occ))
    fp = c2.first_purchase(tx, occ, cust, art)
    log("first purchases", len(fp))

    # ---------------- M1: 90-day repurchase (findings 1 and 3) ----------------
    d = fp[fp["horizon"] >= 90].copy()
    d["first_month"] = d["first"].dt.to_period("M").astype(str)
    d = d[d["first_month"] <= "2020-02"]  # pre-COVID cohorts, the comparison on the slide
    d["y"] = (d["days_to_2nd"] <= 90).astype(int)
    d["basket"] = pd.Categorical(pd.cut(d["items"], [1, 2, 4, 7, np.inf], right=False,
                                        labels=["1", "2-3", "4-6", "7+"]).astype(str), categories=["1", "2-3", "4-6", "7+"])
    d["channel"] = pd.Categorical(d["channel"], categories=["online", "store", "both"])
    d["age"] = pd.Categorical(d["age_band"].astype(object).fillna("unknown").astype(str),
                              categories=["25-34", "16-24", "35-44", "45-54", "55-64", "65+", "unknown"])
    d["line"] = d["first_line"].fillna("unknown")
    d["first_month"] = pd.Categorical(d["first_month"], categories=sorted(d["first_month"].unique()))
    f1 = "y ~ C(first_month) + C(basket) + C(channel) + C(age) + C(line, Treatment('Ladieswear'))"
    log("M1 fitting", len(d))
    m1 = smf.logit(f1, data=d).fit(disp=0, maxiter=100)
    m1r = smf.logit(f1, data=d).fit(disp=0, maxiter=100, cov_type="HC1")
    pred = m1.predict(d)
    RES["M1"] = {
        "row": "one new customer (first purchase 2019-03-01 to 2020-02-29, observable for 90 days)",
        "dependent": "repurchased within 90 days (1/0)",
        "predictors": "first-purchase month (ref 2019-03), first-basket size (ref 1 item), first channel (ref online), age band (ref 25-34), main line of first basket (ref Ladieswear)",
        "fit": {"n": int(m1.nobs), "events": int(d["y"].sum()), "event_rate_pct": float(d["y"].mean() * 100),
                "mcfadden_r2": float(m1.prsquared), "lr_chi2": float(m1.llr), "lr_df": int(m1.df_model),
                "lr_p": float(m1.llr_pvalue), "auc": auc(d["y"].to_numpy(), pred.to_numpy())},
        "odds_ratios": or_table(m1, ["basket", "channel", "first_month)[T.2020-02]", "first_month)[T.2019-09]"]),
        "adjusted_pct_basket": adjusted_prob(m1, d, "basket", ["1", "2-3", "4-6", "7+"]),
        "adjusted_pct_channel": adjusted_prob(m1, d, "channel", ["online", "store"]),
        "adjusted_pct_month": adjusted_prob(m1, d, "first_month", ["2019-03", "2020-02"]),
        "raw_pct_month": {m: float(d.loc[d["first_month"] == m, "y"].mean() * 100) for m in ["2019-03", "2020-02"]},
        "max_vif": vif_from_fit(m1),
        "robust_se_max_ratio": float((m1r.bse / m1.bse).max()),
    }
    log("M1 done")

    # T1: chi-square month x repurchase
    tab = pd.crosstab(d["first_month"], d["y"])
    chi2, p, dof, v = cramers_v(tab)
    a = d[d["first_month"] == "2019-03"]["y"]
    b = d[d["first_month"] == "2020-02"]["y"]
    diff = ci_prop_diff(a.sum(), len(a), b.sum(), len(b))
    RES["T1"] = {"chi2": chi2, "dof": dof, "p": p, "cramers_v": v,
                 "diff_2019_03_minus_2020_02_pp": diff}

    # ---------------- M2: no purchase in year 2 (supporting A) ----------------
    y1 = c2.year_profile(occ, c2.Y1)
    y2 = c2.year_profile(occ, c2.Y2)
    e = y1[["type", "occ"]].copy()
    e["y"] = (~e.index.isin(y2.index)).astype(int)
    cu = cust.set_index("c")
    e["age"] = pd.Categorical(cu["age_band"].astype(object).reindex(e.index).fillna("unknown").astype(str),
                              categories=["25-34", "16-24", "35-44", "45-54", "55-64", "65+", "unknown"])
    e["type"] = pd.Categorical(e["type"], categories=["omni", "online only", "store only"])
    e["log_occ"] = np.log(e["occ"])
    first_y1 = occ[c2.in_year(occ["t_dat"], c2.Y1)].groupby("c")["t_dat"].min()
    e["months_in_y1"] = ((c2.Y1[1] - first_y1.reindex(e.index)).dt.days / 30.44).clip(upper=12)
    log("M2 fitting", len(e))
    f_raw = "y ~ C(type)"
    f2 = "y ~ C(type) + log_occ + months_in_y1 + C(age)"
    m2a = smf.logit(f_raw, data=e).fit(disp=0)
    m2 = smf.logit(f2, data=e).fit(disp=0, maxiter=100)
    m2r = smf.logit(f2, data=e).fit(disp=0, maxiter=100, cov_type="HC1")
    pred2 = m2.predict(e)
    RES["M2"] = {
        "row": "one customer who bought in year 1 (2018-09-20 to 2019-09-19)",
        "dependent": "no purchase in year 2 (1/0)",
        "predictors": "year-1 channel type (ref omni); controls: log year-1 purchase occasions, months observed in year 1, age band (ref 25-34)",
        "fit": {"n": int(m2.nobs), "events": int(e["y"].sum()), "event_rate_pct": float(e["y"].mean() * 100),
                "mcfadden_r2": float(m2.prsquared), "lr_chi2": float(m2.llr), "lr_df": int(m2.df_model),
                "lr_p": float(m2.llr_pvalue), "auc": auc(e["y"].to_numpy(), pred2.to_numpy())},
        "odds_ratios_unadjusted": or_table(m2a, ["type"]),
        "odds_ratios": or_table(m2, ["type", "log_occ", "months_in_y1"]),
        "raw_pct_type": {t: float(e.loc[e["type"] == t, "y"].mean() * 100) for t in ["omni", "online only", "store only"]},
        "adjusted_pct_type": adjusted_prob(m2, e, "type", ["omni", "online only", "store only"]),
        "max_vif": vif_from_fit(m2),
        "robust_se_max_ratio": float((m2r.bse / m2.bse).max()),
        "occ_median_by_type": e.groupby("type", observed=True)["occ"].median().to_dict(),
    }
    log("M2 done")

    # ---------------- T2 / T3: closures (finding 4) ----------------
    groups = c2.channel_groups(occ, "2019-09-20", "2020-03-01")
    base = c2.channel_groups(occ, "2018-09-20", "2019-03-01")
    clo = occ[(occ["t_dat"] >= "2020-03-15") & (occ["t_dat"] < "2020-06-01")]
    on_buyers = set(clo.loc[clo["on"], "c"])
    rows = {g: [sum(i in on_buyers for i in ids), len(ids)] for g, ids in groups.items()}
    tab2 = pd.DataFrame({g: [r[0], r[1] - r[0]] for g, r in rows.items()}, index=["online", "not"]).T
    chi2, p, dof, v = cramers_v(tab2)
    RES["T2"] = {"table": {g: {"bought_online": int(r[0]), "n": int(r[1]), "pct": r[0] / r[1] * 100} for g, r in rows.items()},
                 "chi2": chi2, "dof": dof, "p": p, "cramers_v": v}
    aft = set(occ.loc[occ["t_dat"] >= "2020-06-01", "c"])
    aft19 = set(occ.loc[(occ["t_dat"] >= "2019-06-01") & (occ["t_dat"] <= "2019-09-22"), "c"])
    s20 = groups["store only before"]
    s19 = base["store only before"]
    x20 = sum(i in aft for i in s20)
    x19 = sum(i in aft19 for i in s19)
    overlap = len(set(s20) & set(s19))
    RES["T3"] = {"after_reopen_pct": x20 / len(s20) * 100, "n2020": len(s20),
                 "same_months_2019_pct": x19 / len(s19) * 100, "n2019": len(s19),
                 "diff_pp_ci": ci_prop_diff(x20, len(s20), x19, len(s19)),
                 "customers_in_both_groups": overlap}
    log("T2/T3 done")

    # ---------------- T4: per-customer store share by age band (supporting B) ----------------
    per = tx.groupby("c").agg(rows=("on", "size"), online=("on", "sum"))
    per["store_share"] = (1 - per["online"] / per["rows"]) * 100
    per["age"] = cu["age_band"].astype(str).reindex(per.index).values
    per = per[per["age"].isin(common.AGE_LABELS)]
    grp = [per.loc[per["age"] == a, "store_share"].to_numpy() for a in common.AGE_LABELS]
    F, pF = stats.f_oneway(*grp)
    H, pH = stats.kruskal(*grp)
    grand = per["store_share"].mean()
    ss_b = sum(len(g) * (g.mean() - grand) ** 2 for g in grp)
    ss_t = ((per["store_share"] - grand) ** 2).sum()
    lev = stats.levene(*[g[:200000] for g in grp])
    RES["T4"] = {"n_customers": int(len(per)), "F": float(F), "p_anova": float(pF), "eta_squared": float(ss_b / ss_t),
                 "H": float(H), "p_kruskal": float(pH), "levene_p": float(lev.pvalue),
                 "mean_store_share_by_age": {a: float(g.mean()) for a, g in zip(common.AGE_LABELS, grp)},
                 "median_store_share_by_age": {a: float(np.median(g)) for a, g in zip(common.AGE_LABELS, grp)},
                 "skew": float(stats.skew(per["store_share"]))}
    log("T4 done")

    with open(OUT / "hm_tests_results.json", "w", encoding="utf-8") as f:
        json.dump(RES, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    log("wrote json")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
