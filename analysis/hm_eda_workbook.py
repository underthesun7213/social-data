"""Build the H&M EDA results workbook (one .xlsx, results only, no raw data).

Flow recorded in the workbook:
  cycle 1 (broad EDA) -> question candidates Q1-Q11
  -> union with the proposal's Issue 1-3 -> union items U1-U9
  -> cycle 2 (targeted EDA per union item) -> findings and solution directions.

Run from anywhere (first run builds a parquet cache in data/hm/, ~1 min):
    python analysis/hm_eda_workbook.py

Output: analysis/hm_eda_results.xlsx (Korean) and analysis/hm_eda_results_en.xlsx
(English), same tables; the text comes from hm_eda_text.py / hm_eda_text_en.py.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hm_eda_common as common  # noqa: E402
import hm_eda_cycle1 as cycle1  # noqa: E402
import hm_eda_cycle2 as cycle2  # noqa: E402
from hm_eda_charts import CHARTS  # noqa: E402
import hm_eda_lineage as lineage  # noqa: E402
import hm_eda_text as text_ko  # noqa: E402
import hm_eda_text_en as text_en  # noqa: E402

REPORT_CSV = common.ROOT / "analysis" / "hm_report_quarterly.csv"
# Fiscal quarters that overlap the Kaggle data (2018-09-20 to 2020-09-22).
KAGGLE_QUARTERS = ["FY2018 Q4", "FY2019 Q1", "FY2019 Q2", "FY2019 Q3", "FY2019 Q4",
                   "FY2020 Q1", "FY2020 Q2", "FY2020 Q3", "FY2020 Q4"]
OUTPUTS = [(common.ROOT / "analysis" / "hm_eda_results.xlsx", text_ko),
           (common.ROOT / "analysis" / "hm_eda_results_en.xlsx", text_en)]
# Categorical order from the dataviz reference palette (validated for adjacent pairs).
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
CHART_W, CHART_H, CHART_ROWS = 640, 320, 17  # px, px, sheet rows one chart takes
STORY_WIDTHS = [18, 62, 62, 30]  # main-question sheet column widths (characters)


def text_width(s):
    """Approximate width in Excel character units: Hangul and other wide glyphs count about 1.8."""
    return sum(1.8 if ord(ch) > 0x1100 else 1 for ch in s)


def row_height(cells):
    """Row height (points) that shows every wrapped (text, column width) cell in full.
    Word wrapping wastes part of each line, hence the 1.2 factor and the spare line."""
    lines = max(-(-int(text_width(t) * 1.2) // w) for t, w in cells)
    return 15 * (lines + 1)


class Book:
    def __init__(self, path, labels, lang):
        self.labels = labels
        self.lang = lang
        self.wb = pd.ExcelWriter(path, engine="xlsxwriter")
        b = self.wb.book
        self.f = {
            "title": b.add_format({"bold": True, "font_size": 14}),
            "h": b.add_format({"bold": True, "bg_color": "#DCE6F1", "border": 1, "text_wrap": True, "valign": "top"}),
            "label": b.add_format({"bold": True, "valign": "top"}),
            "wrap": b.add_format({"text_wrap": True, "valign": "top"}),
            "cell": b.add_format({"border": 1, "text_wrap": True, "valign": "top"}),
            "num": b.add_format({"num_format": "#,##0.00"}),
            "int": b.add_format({"num_format": "#,##0"}),
        }

    def text_sheet(self, name, title, header, rows, widths):
        ws = self.wb.book.add_worksheet(name)
        ws.write(0, 0, title, self.f["title"])
        for j, h in enumerate(header):
            ws.write(2, j, h, self.f["h"])
            ws.set_column(j, j, widths[j])
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                ws.write(3 + i, j, v, self.f["cell"])
        ws.freeze_panes(3, 0)

    def table_sheet(self, spec, tables):
        name = spec["sheet"]
        ws = self.wb.book.add_worksheet(name)
        ws.write(0, 0, spec["title"], self.f["title"])
        for r, (label, key) in enumerate(zip(self.labels, ["link", "what", "obs"]), start=1):
            ws.write(r, 0, label, self.f["label"])
            ws.merge_range(r, 1, r, 12, spec.get(key, ""), self.f["wrap"])
            ws.set_row(r, 15 * max(2, len(spec.get(key, "")) // 110 + 1))
        ws.set_column(0, 0, 18)
        ws.set_column(1, 30, 13)
        # Charts first, two per row, right under the description; tables below them.
        charts = CHARTS.get(name[:5], [])
        top = 5 + CHART_ROWS * ((len(charts) + 1) // 2) + (1 if charts else 0)
        placed = []
        for i, (sub, df) in enumerate(tables):
            df = df.copy()
            for c in df.columns:
                if df[c].dtype.kind in "OSUb" or isinstance(df[c].dtype, pd.CategoricalDtype):
                    df[c] = df[c].astype(str)
            ws.write(top, 0, sub, self.f["label"])
            top += 1
            for j, c in enumerate(df.columns):
                ws.write(top, j, str(c), self.f["h"])
            for r, row in enumerate(df.itertuples(index=False), start=top + 1):
                for j, v in enumerate(row):
                    if isinstance(v, (float, np.floating)) and np.isnan(v):
                        continue
                    if isinstance(v, (int, np.integer)):
                        ws.write_number(r, j, int(v), self.f["int"])
                    elif isinstance(v, (float, np.floating)):
                        ws.write_number(r, j, float(v), self.f["int"] if abs(v) >= 1000 else self.f["num"])
                    else:
                        ws.write(r, j, v)
            if i == 0 and spec.get("heat"):
                j0 = df.columns.get_loc(spec["heat"][0])
                j1 = df.columns.get_loc(spec["heat"][1])
                ws.conditional_format(top + 1, j0, top + len(df), j1, {
                    "type": "3_color_scale", "min_color": "#F8696B", "mid_color": "#FFEB84", "max_color": "#63BE7B"})
            placed.append((top, df))
            top += len(df) + 2
        ws.freeze_panes(5, 1)
        for k, c in enumerate(charts):
            head, df = placed[c.get("table", 0)]
            row, col = 5 + CHART_ROWS * (k // 2), 0 if k % 2 == 0 else 7
            ws.insert_chart(row, col, self.chart(name, c, df, head), {"x_offset": 4, "y_offset": 6})

    def chart(self, name, c, df, head):
        lo, hi = c.get("only", (0, len(df)))
        first, last = head + 1 + lo, head + hi
        ch = self.wb.book.add_chart({"type": c["type"], **({"subtype": c["subtype"]} if "subtype" in c else {})})
        cats = c.get("cats", 1)
        if "rows" in c:
            j0, j1 = df.columns.get_loc(c["cols"][0]), df.columns.get_loc(c["cols"][-1])
            labels = list(df.iloc[:, 0])
            series = [(head + 1 + labels.index(r), [name, head + 1 + labels.index(r), 0],
                       [name, head, j0, head, j1], [name, head + 1 + labels.index(r), j0, head + 1 + labels.index(r), j1])
                      for r in c["rows"]]
        else:
            series = []
            for col in c["cols"]:
                j = df.columns.get_loc(col)
                series.append((None, [name, head, j], [name, first, 0, last, cats - 1], [name, first, j, last, j]))
        for i, (_, sname, scats, svals) in enumerate(series):
            color = PALETTE[i % len(PALETTE)]
            s = {"name": sname, "categories": scats, "values": svals}
            if c["type"] == "line":
                s["line"] = {"color": color, "width": 2}
                s["marker"] = {"type": "none"}
            else:
                s["fill"] = {"color": color}
                s["border"] = {"none": True}
                s["gap"] = 60
                if c.get("overlap"):
                    s["overlap"] = 100
            ch.add_series(s)
        ch.set_title({"name": c["title"][self.lang], "name_font": {"size": 11, "bold": True}})
        vals = df.loc[:, c["cols"]].iloc[lo:hi] if "rows" not in c else df.loc[:, c["cols"]]
        vals = pd.to_numeric(vals.stack(), errors="coerce")
        font = {"size": 9, "color": "#52514e"}
        grid = {"visible": True, "line": {"color": "#E5E5E5", "width": 0.75}}
        value_axis = {"line": {"none": True}, "num_font": font, "major_gridlines": grid,
                      "num_format": "#,##0" if vals.abs().max() >= 10 else "0.0"}
        if "ymax" in c:
            value_axis["max"] = c["ymax"]
        if c["type"] in ("column", "bar") and vals.min() >= 0:
            value_axis["min"] = 0  # bars encode length, so they start at zero
        if c.get("subtype") == "percent_stacked":
            value_axis["num_format"] = "0%"
        # Category labels sit below the plot even when values go negative.
        cat_axis = {"line": {"color": "#BFBFBF"}, "num_font": font, "label_position": "low"}
        if c["type"] == "bar":
            ch.set_x_axis(value_axis)
            ch.set_y_axis({**cat_axis, "reverse": True})
        else:
            if (hi - lo if "rows" not in c else len(c["cols"])) > 8:
                cat_axis["num_font"] = {**font, "rotation": -45}
            ch.set_x_axis(cat_axis)
            ch.set_y_axis(value_axis)
        ch.set_legend({"position": "bottom"} if len(series) > 1 else {"none": True})
        ch.set_chartarea({"border": {"none": True}})
        ch.set_size({"width": CHART_W, "height": CHART_H})
        return ch

    def story_sheet(self, main, tables):
        """The main-question sheet: sections of labelled rows, and chart sections whose
        source tables (cycle-2 tables or report figures) are written at the bottom."""
        name = main["sheet"]
        ws = self.wb.book.add_worksheet(name)
        for j, w in enumerate(STORY_WIDTHS):
            ws.set_column(j, j, w)
        ws.write(0, 0, main["title"], self.f["title"])
        ws.merge_range(1, 0, 1, 3, main["lead"], self.f["wrap"])
        ws.set_row(1, row_height([(main["lead"], sum(STORY_WIDTHS))]))
        r = 3
        chart_rows = []
        for sec in main["sections"]:
            ws.write(r, 0, sec["heading"], self.f["label"])
            r += 1
            if sec.get("charts"):
                chart_rows.append((r, sec["charts"]))
                r += CHART_ROWS + 1
                continue
            # "order" picks which column of the rows goes where (e.g. a short verdict first).
            order = sec.get("order", range(len(sec["header"])))
            for j, h in enumerate([sec["header"][k] for k in order]):
                ws.write(r, j, h, self.f["h"])
            r += 1
            for row in ([row[k] for k in order] for row in sec["rows"]):
                for j, v in enumerate(row):
                    ws.write(r, j, v, self.f["cell"])
                # Excel does not grow wrapped rows written by xlsxwriter, so size them here.
                ws.set_row(r, row_height([(str(v), STORY_WIDTHS[j]) for j, v in enumerate(row)]))
                r += 1
            r += 1
        # Chart source tables go below everything else on the same sheet.
        ws.write(r, 0, main["data_label"], self.f["label"])
        r += 1
        for row_at, charts in chart_rows:
            for k, c in enumerate(charts):
                df = tables[c["table"]].copy()
                lo, hi = c.get("only", (0, len(df)))
                df = df.iloc[lo:hi].reset_index(drop=True)
                for j, col in enumerate(df.columns):
                    ws.write(r, j, str(col), self.f["h"])
                for i, row in enumerate(df.itertuples(index=False), start=r + 1):
                    for j, v in enumerate(row):
                        if isinstance(v, (int, float, np.integer, np.floating)) and not pd.isna(v):
                            ws.write_number(i, j, float(v), self.f["int"] if float(v).is_integer() else self.f["num"])
                        elif not (isinstance(v, float) and pd.isna(v)):
                            ws.write(i, j, str(v))
                chart = self.chart(name, {**c, "only": (0, len(df))}, df, r)
                ws.insert_chart(row_at, 0 if k == 0 else 2, chart, {"x_offset": 4 if k == 0 else 64, "y_offset": 6})
                r += len(df) + 2

    def close(self):
        self.wb.close()


def report_tables(names):
    """H&M report figures (hm_report_quarterly.csv) shaped for the main-question charts."""
    q = pd.read_csv(REPORT_CSV)
    inside = q["fiscal_quarter"].isin(KAGGLE_QUARTERS)
    sales = pd.DataFrame({
        "fiscal_quarter": q["fiscal_quarter"],
        names["sales"]: q["sales_lc_pct"],
        names["kaggle"]: q["sales_lc_pct"].where(inside),
    })
    stores = q[["fiscal_quarter", "stores_end"]].rename(columns={"stores_end": names["stores"]})
    members = q.loc[q["loyalty_members_million"].notna(), ["fiscal_quarter", "loyalty_members_million"]]
    members = members.rename(columns={"loyalty_members_million": names["members"]})
    return {"rp.sales": sales, "rp.stores": stores, "rp.members": members}


def build(path, T, tables):
    tables = {**tables, **report_tables(T.MAIN["columns"])}
    T.fill(tables)
    book = Book(path, T.FIELD_LABELS, T.LANG)
    pages = T.PAGES

    def text(key, rows):
        p = pages[key]
        book.text_sheet(p["sheet"], p["title"], p["header"], rows, p["widths"])

    def sheets(cycle):
        for spec in T.SHEETS:
            if spec["cycle"] == cycle:
                book.table_sheet(spec, [(sub, tables[key]) for sub, key in spec["tables"]])

    text("overview", T.OVERVIEW)
    sheets(1)
    text("questions", T.QUESTIONS)
    text("union", T.UNION)
    sheets(2)
    book.story_sheet(T.MAIN, tables)
    text("findings", T.FINDINGS)
    text("lineage", lineage.rows(T))
    text("limits", T.LIMITS)
    book.close()
    print(f"saved {path}")


def main():
    tx, cust, art = common.load()
    print(f"loaded {len(tx):,} transactions")
    t1, extra = cycle1.run(tx, cust, art)
    print("cycle 1 done")
    t2 = cycle2.run(tx, cust, art, extra)
    print("cycle 2 done")
    tables = {**{f"c1.{k}": v for k, v in t1.items()}, **{f"c2.{k}": v for k, v in t2.items()}}
    for path, T in OUTPUTS:
        build(path, T, tables)


if __name__ == "__main__":
    main()
