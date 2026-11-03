"""Redraw the two Phase 1 charts (channel split, age x channel) on the full transaction data.

The originals were drawn from the first 1,048,575 rows (Excel's sheet limit, 2018-09-20 to
2018-10-12). Layout and colours follow the originals so the images can be swapped in place.
Run: py analysis/hm_phase1_charts.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import hm_eda_common as common

OUT = common.ROOT / "analysis"
BLUE, GREEN, ORANGE, TEAL, STEEL = "#3575a8", "#52b788", "#e76f51", "#2a9d8f", "#467a9c"
BAND_NAMES = {"16-24": "16-24 (Gen Z)", "25-34": "25-34 (Millennials)", "35-44": "35-44 (Gen X Early)",
              "45-54": "45-54 (Gen X Late)", "55-64": "55-64 (Boomers)", "65+": "65+ (Seniors)"}


def channel_chart(tx):
    online = tx["sales_channel_id"] == common.ONLINE
    rows = [(~online).sum(), online.sum()]
    value = [tx.loc[~online, "price"].sum(), tx.loc[online, "price"].sum()]
    labels = ["In-Store (Channel 1)", "Online (Channel 2)"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(20.48, 9.53), dpi=100)
    a.pie(rows, labels=labels, colors=[BLUE, GREEN], autopct="%1.1f%%", startangle=140,
          explode=(0.05, 0), pctdistance=0.8, wedgeprops={"width": 0.4}, textprops={"fontsize": 15})
    a.set_title("Transaction Volume Share", fontsize=22)
    bars = b.bar(labels, value, color=[BLUE, GREEN], width=0.5)
    for bar, v in zip(bars, value):
        b.text(bar.get_x() + bar.get_width() / 2, v / 2, f"{v:,.1f}\n({v / sum(value) * 100:.1f}%)",
               ha="center", va="center", color="white", fontsize=16, fontweight="bold")
    b.set_title("Total Sales Value Share", fontsize=22)
    b.set_ylabel("Aggregate Normalized Value (sum of price)", fontsize=17)
    b.tick_params(labelsize=14)
    fig.suptitle("H&M Sales Channel Distribution: Online vs. In-Store (Sept 2018 – Sept 2020, all 31.8M rows)", fontsize=24)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT / "hm_phase1_channel_split.png")
    plt.close(fig)
    return rows, value


def age_chart(tx, cust):
    age = cust.set_index("c")["age_band"].reindex(tx["c"]).to_numpy()
    t = pd.DataFrame({"band": age, "store": tx["sales_channel_id"].to_numpy() != common.ONLINE,
                      "price": tx["price"].to_numpy()}).dropna(subset=["band"])
    g = t.groupby("band", observed=True).agg(store=("store", "mean"), price=("price", "mean"))
    g["store"] *= 100
    g.index = [BAND_NAMES[str(i)] for i in g.index]
    fig, (a, b) = plt.subplots(1, 2, figsize=(20.48, 7.58), dpi=100)
    a.bar(g.index, g["store"], color=ORANGE, width=0.5, label="In-Store %")
    a.bar(g.index, 100 - g["store"], bottom=g["store"], color=TEAL, width=0.5, label="Online %")
    for i, v in enumerate(g["store"]):
        a.text(i, v / 2, f"{v:.1f}%", ha="center", va="center", color="white", fontsize=12, fontweight="bold")
    a.set_title("Channel Share (%) Across Age Cohorts", fontsize=17)
    a.set_ylabel("Share of Transactions (%)", fontsize=14)
    a.set_xlabel("Age Cohort", fontsize=14)
    a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.36), ncol=2, fontsize=13)
    bars = b.bar(g.index, g["price"], color=STEEL, width=0.5)
    for bar, v in zip(bars, g["price"]):
        b.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.4f}", ha="center", va="bottom", fontsize=11, fontweight="bold")
    b.set_title("Average Item Price by Age Cohort", fontsize=17)
    b.set_ylabel("Normalized Average Price per Item", fontsize=14)
    b.set_xlabel("Age Cohort", fontsize=14)
    for ax in (a, b):
        ax.tick_params(axis="x", rotation=30, labelsize=12)
        for lab in ax.get_xticklabels():
            lab.set_ha("right")
    fig.suptitle("Demographic Engagement: Purchasing Power & Channel Adoption by Age Group (all 31.8M rows)", fontsize=19)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "hm_phase1_age_channel.png")
    plt.close(fig)
    return g


def main():
    sns.set_theme(style="whitegrid")
    tx, cust, art = common.load()
    rows, value = channel_chart(tx)
    print(f"online rows {rows[1] / sum(rows) * 100:.1f}%, online value {value[1] / sum(value) * 100:.1f}%")
    print(age_chart(tx, cust).round(4).to_string())


if __name__ == "__main__":
    main()
