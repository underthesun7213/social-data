"""H&M Phase 1 evidence: retention, channel mix and age concentration.

Data: Kaggle competition h-and-m-personalized-fashion-recommendations
(transactions_train.csv, customers.csv, articles.csv only; no images).

Run from anywhere:
    python analysis/hm_phase1.py

If the CSVs are not in data/hm/, the script downloads them with the Kaggle CLI.
Authentication comes from the KAGGLE_API_TOKEN environment variable, which you
set yourself; no token is read or written by this script.

Output: analysis/hm_phase1_results.md
"""

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "hm"
OUT = ROOT / "analysis" / "hm_phase1_results.md"

COMPETITION = "h-and-m-personalized-fashion-recommendations"
FILES = ["transactions_train.csv", "customers.csv", "articles.csv"]

# Customers whose first purchase is before this date can be observed for a year or more.
COHORT_CUTOFF = pd.Timestamp("2019-09-22")
AGE_BINS = [16, 25, 35, 45, 55, 65, np.inf]
AGE_LABELS = ["16-24", "25-34", "35-44", "45-54", "55-64", "65+"]
ONLINE = 2  # assumption: sales_channel_id 2 = online


# ---------------------------------------------------------------- data download

def ensure_data():
    DATA.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        target = DATA / name
        if target.exists():
            continue
        # Reuse a copy downloaded earlier into data/ instead of downloading again.
        legacy = ROOT / "data" / name
        if legacy.exists():
            shutil.move(str(legacy), str(target))
            print(f"moved {legacy} -> {target}")
            continue
        print(f"downloading {name} ...")
        result = subprocess.run(
            ["kaggle", "competitions", "download", "-c", COMPETITION, "-f", name, "-p", str(DATA)],
            capture_output=True, text=True,
        )
        print(result.stdout + result.stderr)
        archive = DATA / f"{name}.zip"
        if archive.exists():
            with zipfile.ZipFile(archive) as z:
                z.extractall(DATA)
            archive.unlink()
        if not target.exists():
            sys.exit(
                f"Kaggle download of {name} failed (see the message above). A 403 means the "
                "competition rules have not been accepted for this account; an authentication "
                "error means KAGGLE_API_TOKEN is not set in this shell."
            )


# ---------------------------------------------------------------- loading

def load():
    tx = pd.read_csv(
        DATA / "transactions_train.csv",
        usecols=["t_dat", "customer_id", "price", "sales_channel_id"],
        dtype={"t_dat": "category", "customer_id": "category",
               "price": "float32", "sales_channel_id": "int8"},
    )
    # Only ~730 distinct dates, so parse the categories rather than 31M strings.
    tx["t_dat"] = tx["t_dat"].cat.rename_categories(pd.to_datetime(tx["t_dat"].cat.categories))
    tx["t_dat"] = tx["t_dat"].astype("datetime64[ns]")

    cust = pd.read_csv(DATA / "customers.csv", usecols=["customer_id", "age"],
                       dtype={"customer_id": "string", "age": "float32"})
    return tx, cust


# ---------------------------------------------------------------- [1] retention

def retention(tx):
    # One purchase occasion = one customer on one day.
    occ = pd.DataFrame({
        "c": tx["customer_id"].cat.codes.to_numpy(),
        "d": (tx["t_dat"] - tx["t_dat"].min()).dt.days.to_numpy().astype(np.int32),
    }).drop_duplicates()
    occ.sort_values(["c", "d"], inplace=True)

    n_occ = occ.groupby("c").size()
    first_day = occ.groupby("c")["d"].min()
    cutoff_day = (COHORT_CUTOFF - tx["t_dat"].min()).days
    cohort = first_day < cutoff_day

    gaps = occ["d"].diff()
    gaps = gaps[occ["c"].eq(occ["c"].shift())]

    return {
        "customers": len(n_occ),
        "occasions": len(occ),
        "one_time_share": (n_occ == 1).mean() * 100,
        "cohort_customers": int(cohort.sum()),
        "cohort_one_time_share": (n_occ[cohort] == 1).mean() * 100,
        "gap_median": float(gaps.median()),
        "gap_mean": float(gaps.mean()),
        "gap_count": len(gaps),
    }


# ---------------------------------------------------------------- [2] channel

def channel(tx):
    month = tx["t_dat"].dt.to_period("M")
    online = tx["sales_channel_id"].eq(ONLINE)
    g = pd.DataFrame({"m": month, "on": online, "p": tx["price"],
                      "pon": tx["price"].where(online, 0)}).groupby("m")
    monthly = pd.DataFrame({
        "transactions": g.size(),
        "online_tx_share": g["on"].mean() * 100,
        "online_value_share": g["pon"].sum() / g["p"].sum() * 100,
    })

    def window(year):
        months = [pd.Period(f"{year}-{m:02d}", "M") for m in (3, 4, 5)]
        sel = month.isin(months)
        return online[sel].mean() * 100

    covid = {
        "by_month": [(f"{m:02d}",
                      monthly.loc[pd.Period(f"2019-{m:02d}", "M"), "online_tx_share"],
                      monthly.loc[pd.Period(f"2020-{m:02d}", "M"), "online_tx_share"])
                     for m in (3, 4, 5)],
        "mar_may_2019": window(2019),
        "mar_may_2020": window(2020),
    }
    return monthly, covid


# ---------------------------------------------------------------- [3] age

def age(tx, cust):
    cust = cust.copy()
    cust["band"] = pd.cut(cust["age"], AGE_BINS, right=False, labels=AGE_LABELS)
    band_of = dict(zip(cust["customer_id"], cust["band"]))

    # Per purchasing customer: transaction rows and value.
    per = pd.DataFrame({"c": tx["customer_id"], "p": tx["price"]}).groupby("c", observed=True)["p"]
    per = pd.DataFrame({"n": per.size(), "v": per.sum()})
    per["band"] = pd.Categorical([band_of.get(c) for c in per.index.astype(str)],
                                 categories=AGE_LABELS)

    registered = cust["band"].value_counts().reindex(AGE_LABELS)
    by = per.groupby("band", observed=False).agg(buyers=("n", "size"), tx=("n", "sum"), value=("v", "sum"))
    table = pd.DataFrame({
        "registered_share": registered / registered.sum() * 100,
        "buyer_share": by["buyers"] / by["buyers"].sum() * 100,
        "tx_share": by["tx"] / by["tx"].sum() * 100,
        "value_share": by["value"] / by["value"].sum() * 100,
        "tx_per_buyer": by["tx"] / by["buyers"],
    })
    meta = {
        "registered": len(cust),
        "age_missing": int(cust["age"].isna().sum()),
        "age_missing_share": cust["age"].isna().mean() * 100,
        "buyers_missing_age": int(per["band"].isna().sum()),
        "median_age_registered": float(cust["age"].median()),
    }
    return table, meta


# ---------------------------------------------------------------- report

def pct(x):
    return f"{x:.1f}%"


def report(tx, r, monthly, covid, a, am):
    start, end = tx["t_dat"].min().date(), tx["t_dat"].max().date()
    L = []
    w = L.append
    w("# H&M Phase 1: dataset evidence\n")
    w(f"Source: Kaggle `{COMPETITION}`, transactions_train.csv ({len(tx):,} rows, "
      f"{start} to {end}), customers.csv, articles.csv. Generated by `analysis/hm_phase1.py`.\n")

    w("## 1. Numbers\n")
    w("### [1] Retention (same-day purchases counted as one purchase)\n")
    w("| Metric | Value |\n|---|---|")
    w(f"| Purchasing customers | {r['customers']:,} |")
    w(f"| Purchase occasions (customer x day) | {r['occasions']:,} |")
    w(f"| One-time buyers, all customers | {pct(r['one_time_share'])} |")
    w(f"| Customers with first purchase before {COHORT_CUTOFF.date()} (observable 1+ year) | {r['cohort_customers']:,} |")
    w(f"| One-time buyers, that cohort | {pct(r['cohort_one_time_share'])} |")
    w(f"| Repurchase interval, median (days) | {r['gap_median']:.0f} |")
    w(f"| Repurchase interval, mean (days) | {r['gap_mean']:.1f} |")
    w(f"| Repurchase intervals measured | {r['gap_count']:,} |\n")

    w("### [2] Channel (channel 2 assumed online)\n")
    w("| Month | Transactions | Channel 2 share of transactions | Channel 2 share of value |\n|---|---|---|---|")
    for m, row in monthly.iterrows():
        w(f"| {m} | {int(row['transactions']):,} | {pct(row['online_tx_share'])} | {pct(row['online_value_share'])} |")
    w(f"\n2018-09 starts on {start} and 2020-09 ends on {end}, so both are partial months.\n")
    w("COVID store closure period vs the same months a year earlier (channel 2 share of transactions):\n")
    w("| Month | 2019 | 2020 | Change (pp) |\n|---|---|---|---|")
    for m, a19, a20 in covid["by_month"]:
        w(f"| {m} | {pct(a19)} | {pct(a20)} | {a20 - a19:+.1f} |")
    w(f"| Mar-May combined | {pct(covid['mar_may_2019'])} | {pct(covid['mar_may_2020'])} | "
      f"{covid['mar_may_2020'] - covid['mar_may_2019']:+.1f} |\n")

    w("### [3] Age (customers.csv `age`)\n")
    w("| Age band | Share of registered customers | Share of purchasing customers | Share of transactions | Share of value | Transactions per purchasing customer |\n|---|---|---|---|---|---|")
    for band, row in a.iterrows():
        w(f"| {band} | {pct(row['registered_share'])} | {pct(row['buyer_share'])} | {pct(row['tx_share'])} | "
          f"{pct(row['value_share'])} | {row['tx_per_buyer']:.1f} |")
    w(f"\nAge missing for {am['age_missing']:,} of {am['registered']:,} registered customers "
      f"({pct(am['age_missing_share'])}); {am['buyers_missing_age']:,} purchasing customers without age are excluded "
      f"from the shares. Median registered age: {am['median_age_registered']:.0f}.\n")

    young = a.loc[["16-24", "25-34"]].sum()
    on18 = monthly.loc[pd.Period("2018-10", "M"), "online_tx_share"]
    on20 = monthly.loc[pd.Period("2020-08", "M"), "online_tx_share"]

    w("## 2. Evidence sentences for the proposal\n")
    w("**Issue 1. Stagnant Sales and Weak Customer Retention**\n")
    w(f"- In H&M's transaction data (Sept 2018 to Sept 2020), {pct(r['one_time_share'])} of "
      f"{r['customers']:,} customers made only one purchase (same-day purchases counted as one).")
    w(f"- Among customers whose first purchase was before Sept 22, 2019, and who could therefore be observed "
      f"for at least one year, {pct(r['cohort_one_time_share'])} never returned for a second purchase; for "
      f"customers who did return, the median time between purchases was {r['gap_median']:.0f} days.\n")
    w("**Issue 2. Shrinking Store Network and Shift to Online**\n")
    w(f"- In H&M's transaction data, the share of transactions made through the online channel was "
      f"{pct(covid['mar_may_2020'])} in March to May 2020, compared with {pct(covid['mar_may_2019'])} in "
      f"the same months of 2019.")
    w(f"- The online share of monthly transactions moved from {pct(on18)} in October 2018 to {pct(on20)} in "
      f"August 2020.\n")
    w("**Issue 3. Customer Age Concentration**\n")
    w(f"- In H&M's customer data, customers aged 16 to 34 account for {pct(young['buyer_share'])} of "
      f"purchasing customers and {pct(young['value_share'])} of purchase value.")
    top = a["tx_per_buyer"].idxmax()
    w(f"- The {top} age group has the highest purchase frequency, at {a.loc[top, 'tx_per_buyer']:.1f} "
      f"transactions per customer over the two years.\n")

    w("## 3. Limitations\n")
    w("- **Channel:** `sales_channel_id` has no official definition. Following the common community "
      "interpretation, channel 2 is assumed to be online and channel 1 to be stores. This is an assumption.")
    w("- **Price:** `price` is a transformed value, not a real currency, so amounts are reported only as shares (%).")
    w(f"- **Observation window:** the data covers {start} to {end} only. Customers who first bought late in the "
      "window have little time to repurchase, which inflates the all-customer one-time share; the "
      "first-purchase-before-2019-09-22 cohort is reported to reduce this bias. The first and last months are partial.")
    w("- **Age:** age comes from customer registration data, not verified at purchase, and is missing for "
      f"about {pct(am['age_missing_share'])} of customers. One account may be used by more than one person.")
    w("- **Transactions:** a transaction is one item row in transactions_train.csv; repurchase metrics use "
      "customer-days instead.")
    w("- The dataset is a sample released for a Kaggle competition and may not represent all H&M markets or sales.")
    text = "\n".join(L) + "\n"
    # Print first so the numbers are not lost if the file cannot be written.
    print(text)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"saved {OUT}")


def main():
    ensure_data()
    tx, cust = load()
    print(f"loaded {len(tx):,} transactions, {len(cust):,} customers")
    r = retention(tx)
    monthly, covid = channel(tx)
    a, am = age(tx, cust)
    report(tx, r, monthly, covid, a, am)


if __name__ == "__main__":
    main()
