"""Figures for the Phase 4 report.

Reads only aggregate outputs (data/profile/analysis_*.json, analysis/hm_tests_results.json,
analysis/hm_report_quarterly.csv), never raw rows, and writes PNGs to report/phase4/fig/.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "fig"
OUT.mkdir(exist_ok=True)
RED, INK, G1, G2, G3, LIGHT = "#E30415", "#111111", "#58585B", "#808284", "#B8B8BA", "#DEDEDF"
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": G3, "axes.labelcolor": G1, "xtick.color": G1, "ytick.color": G1,
                     "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left"})


def load(name):
    return json.load(open(ROOT / "data" / "profile" / f"analysis_{name}.json", encoding="utf-8"))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=200)
    plt.close(fig)


def labels(ax, bars, fmt="{:.1f}", dy=0.6):
    for b in bars:
        h = b.get_height()
        if h:
            ax.text(b.get_x() + b.get_width() / 2, h + dy, fmt.format(h), ha="center", va="bottom", fontsize=7.5, color=INK)


# Fig 1: the business problem (H&M reports)
q = pd.read_csv(ROOT / "analysis" / "hm_report_quarterly.csv")
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.6))
yrs = ["FY21", "FY22", "FY23", "FY24", "FY25"]
g = [12, 6, -1, 1, 2]
bars = a.bar(yrs, g, color=[G3, G3, RED, RED, RED], width=0.6)
for bb, v in zip(bars, g):
    a.text(bb.get_x() + bb.get_width() / 2, (v + 0.4) if v >= 0 else 0.4, f"{v:+d}", ha="center", fontsize=8)
a.axhline(0, color=G3, lw=0.8)
a.set_ylim(-3, 14)
a.set_title("Net sales growth, local currencies (%)")
a.set_yticks([])
st = [4801, 4465, 4369, 4253, 4101]
bars = b.bar(yrs, st, color=G1, width=0.6)
labels(b, bars, "{:,.0f}", 60)
b.set_ylim(0, 5400)
b.set_yticks([])
b.set_title("Stores at year end")
save(fig, "fig1_context.png")

# Fig 2: RQ1.1 cohort 90-day repurchase
c = load("cohort")
c = [r for r in c if "2019-03" <= r["segment"] <= "2020-06"]
m = [r["segment"][2:] for r in c]
v = [r["repurchase_90d_pct"] for r in c]
col = [RED if r["segment"] in ("2019-03", "2019-11") else (G2 if r["segment"] <= "2019-11" else LIGHT) for r in c]
fig, ax = plt.subplots(figsize=(7.2, 2.8))
bars = ax.bar(m, v, color=col, width=0.7)
labels(ax, bars)
ax.set_ylim(0, 50)
ax.set_yticks([])
ax.tick_params(axis="x", labelsize=7.5)
ax.set_title("90-day repurchase rate of new customers, by first-purchase month (%)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=G2, label="window ends before closures"), Patch(color=RED, label="compared endpoints (2019-03, 2019-11)"),
                   Patch(color=LIGHT, label="window overlaps 2020 closures (not compared)")], fontsize=7, frameon=False, loc="upper right")
save(fig, "fig2_cohort.png")

# Fig 3: RQ1.2 Kaplan-Meier
k = pd.DataFrame(load("km"))
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.6))
a.plot(k["day"], k["returned_pct"], color=INK, lw=1.8)
for d in (30, 90, 365):
    r = k[k["day"] == d].iloc[0]
    a.scatter([d], [r["returned_pct"]], color=RED, s=14, zorder=3)
    a.annotate(f"day {d}: {r['returned_pct']:.1f}%", (d, r["returned_pct"]), xytext=(6, -10), textcoords="offset points", fontsize=7.5)
a.set_title("Share returned by day d (%)")
a.set_xlabel("days since first purchase")
a.set_ylim(0, 70)
b.plot(k["day"], k["next_30d_pct"], color=RED, lw=1.8)
for d in (30, 90, 270):
    r = k[k["day"] == d].iloc[0]
    b.scatter([d], [r["next_30d_pct"]], color=RED, s=14, zorder=3)
    b.annotate(f"day {d}: {r['next_30d_pct']:.1f}%", (d, r["next_30d_pct"]), xytext=(6, 4), textcoords="offset points", fontsize=7.5)
b.axvspan(30, 90, color=LIGHT, alpha=0.6, lw=0)
b.set_title("Chance of returning in the next 30 days (%)")
b.set_xlabel("days since first purchase")
b.set_ylim(0, 14)
save(fig, "fig3_km.png")

# Fig 4: RQ1.3 first basket
fb = load("firstbasket")
fig, ax = plt.subplots(figsize=(7.2, 2.5))
x = range(len(fb))
w = 0.38
b1 = ax.bar([i - w / 2 for i in x], [r["repurchase_90d_pct"] for r in fb], w, color=G2, label="within 90 days")
b2 = ax.bar([i + w / 2 for i in x], [r["repurchase_365d_pct"] for r in fb], w, color=RED, label="within 365 days")
labels(ax, b1)
labels(ax, b2)
ax.set_xticks(list(x), [f"{r['segment']} item" + ("" if r["segment"] == "1" else "s") for r in fb])
ax.set_yticks([])
ax.set_ylim(0, 88)
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.set_title("Repurchase rate by number of items in the first purchase (%)")
save(fig, "fig4_basket.png")

# Fig 5: RQ2.1 monthly online share
mo = [r for r in load("monthly") if "2018-10" <= r["month"] <= "2020-08"]
fig, ax = plt.subplots(figsize=(7.2, 2.5))
xs = [r["month"][2:] for r in mo]
ax.plot(xs, [r["online_row_share"] for r in mo], color=INK, lw=1.8, marker="o", ms=2.5)
i0, i1 = xs.index("20-03"), xs.index("20-05")
ax.axvspan(i0 - 0.5, i1 + 0.5, color=LIGHT, lw=0)
ax.text(i0 - 0.6, 92, "2020 closures", fontsize=7.5, color=G1, ha="right")
ax.set_ylim(50, 102)
ax.tick_params(axis="x", labelsize=7, rotation=90)
ax.set_title("Online (channel 2) share of transaction rows, by month (%)")
save(fig, "fig5_online.png")

# Fig 6: RQ2.1 customer view of the shutdown
cl = load("closure")
names = {"store only before": "Store only", "online only before": "Online only", "omni before": "Omni"}
fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.6))
bars = a.bar([names[r["group"]] for r in cl], [r["bought_online_during_closure_pct"] for r in cl], color=[RED, G2, G2], width=0.55)
labels(a, bars)
a.set_ylim(0, 70)
a.set_yticks([])
a.set_title("Bought online during closures (%)")
x = range(len(cl))
b1 = b.bar([i - w / 2 for i in x], [r["same_months_2019_pct"] for r in cl], w, color=G3, label="same months 2019 (baseline)")
b2 = b.bar([i + w / 2 for i in x], [r["bought_after_reopen_pct"] for r in cl], w, color=RED, label="after reopening 2020")
labels(b, b1)
labels(b, b2)
b.set_xticks(list(x), [names[r["group"]] for r in cl])
b.set_ylim(0, 100)
b.set_yticks([])
b.legend(fontsize=7, frameon=False, loc="upper left")
b.set_title("Bought after reopening vs a year earlier (%)")
save(fig, "fig6_shutdown.png")

# Fig 7: RQ2.2 lapse raw vs adjusted
t = json.load(open(ROOT / "analysis" / "hm_tests_results.json", encoding="utf-8"))["M2"]
types = ["omni", "online only", "store only"]
fig, ax = plt.subplots(figsize=(7.2, 2.5))
x = range(3)
b1 = ax.bar([i - w / 2 for i in x], [t["raw_pct_type"][k] for k in types], w, color=G3, label="raw")
b2 = ax.bar([i + w / 2 for i in x], [t["adjusted_pct_type"][k] for k in types], w, color=RED, label="adjusted for year-1 purchases, months observed, age")
labels(ax, b1)
labels(ax, b2)
ax.set_xticks(list(x), ["Omni", "Online only", "Store only"])
ax.set_ylim(0, 75)
ax.set_yticks([])
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.set_title("No purchase in year 2, by year-1 channel type (%)")
save(fig, "fig7_lapse.png")

# Fig 8: RQ2.3 in-store share by age
ag = [r for r in load("agestore") if r["age_band"] != "unknown"]
fig, ax = plt.subplots(figsize=(7.2, 2.4))
bars = ax.bar([r["age_band"] for r in ag], [r["store_share_pct"] for r in ag], color=[RED if r["age_band"] == "65+" else G2 for r in ag], width=0.6)
labels(ax, bars)
ax.set_ylim(0, 42)
ax.set_yticks([])
ax.set_title("In-store (channel 1) share of transaction rows, by age band (%)")
save(fig, "fig8_age.png")
print("figures written to", OUT)
