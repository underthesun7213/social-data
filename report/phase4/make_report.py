"""Build the Phase 4 final report (.docx) from the figures in fig/ and the numbers verified in
analysis/hm_tests_results.json and data/profile/analysis_*.json. Run make_figs.py first."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
FIG = HERE / "fig"
OUT = HERE / "hm_phase4_final_report.docx"
RED = RGBColor(0xE3, 0x04, 0x15)
GREY = RGBColor(0x58, 0x58, 0x5B)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(2.0)
st = doc.styles["Normal"]
st.font.name = "Arial"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 1.15
for name, size in [("Title", 22), ("Heading 1", 15), ("Heading 2", 12), ("Heading 3", 11)]:
    s = doc.styles[name]
    s.font.name = "Arial"
    s.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    s.font.size = Pt(size)
    s.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    s.font.bold = True
doc.styles["Heading 1"].paragraph_format.space_before = Pt(14)
doc.styles["Heading 2"].paragraph_format.space_before = Pt(10)

FIGNO = [0]
TABNO = [0]


def p(text="", bold_lead=None, italic=False, size=None, color=None, align=None, after=None):
    para = doc.add_paragraph()
    if bold_lead:
        r = para.add_run(bold_lead)
        r.bold = True
    r = para.add_run(text)
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    if align:
        para.alignment = align
    if after is not None:
        para.paragraph_format.space_after = Pt(after)
    return para


def bullets(items, style="List Bullet"):
    for it in items:
        para = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            r = para.add_run(it[0])
            r.bold = True
            para.add_run(it[1])
        else:
            para.add_run(it)
        para.paragraph_format.space_after = Pt(2)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def table(rows, widths=None, caption=None, size=9):
    if caption:
        TABNO[0] += 1
        cp = p(f"Table {TABNO[0]}. {caption}", size=9, color=GREY, after=2)
        cp.runs[0].bold = True
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
            r = c.paragraphs[0].add_run(str(val))
            r.font.size = Pt(size)
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
            if i == 0:
                r.bold = True
                shade(c, "F1F1F2")
            if widths:
                c.width = Cm(widths[j])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def figure(fname, caption, width=16.5):
    FIGNO[0] += 1
    doc.add_picture(str(FIG / fname), width=Cm(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp = p(f"Figure {FIGNO[0]}. {caption}", size=8.5, color=GREY, after=8)
    cp.runs[0].italic = True


def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ------------------------------------------------------------------ title
doc.add_paragraph("Are H&M's New Customers Coming Back?", style="Title")
p("Customer retention and channel shifts in H&M transaction data, 2018–2020, read against H&M's reports for 2021–2026", size=12, color=GREY)
p("Phase 4 Final Report · Course 5601 · Team: [team members]", size=10, color=GREY)
p("Data: Kaggle H&M Personalized Fashion Recommendations (non-commercial academic use; raw data not redistributed) and 43 H&M annual, full-year and quarterly reports. "
  "Every number in this report can be reproduced with the scripts listed in Appendix C.", size=8.5, color=GREY)

# ------------------------------------------------------------------ 1 executive summary
doc.add_heading("1. Executive Summary", level=1)
p("H&M's sales have been flat for three years (local-currency growth of −1%, 1% and 2% in FY2023–FY2025) while it has closed 700 stores and plans about 160 more closures in 2026. "
  "Its own reports worry that consumers are \"more price-conscious and inclined to change\", yet none of the 952 statements we extracted from 43 reports gives a repurchase or lapse rate. "
  "We therefore asked the transaction data two questions: do new customers come back, and do store customers move online when stores close?")
p("", bold_lead="Key findings")
bullets([
    ("New customers were already coming back less before COVID. ", "The 90-day repurchase rate fell from 43.4% for customers who first bought in March 2019 to 31.0% for November 2019, the last cohort whose 90-day window closes before the 2020 store closures. "
     "Group sales were still growing 4–8% a quarter. The drop holds after controlling for basket, channel, age and product line (43.0% → 31.6%), but its size is 5–12 points depending on how strictly new customers are defined, and with one clean year we cannot rule out seasonality."),
    ("The window to win a second purchase is the first 90 days. ", "Of customers not yet back, 10.6% return in the next 30 days at day 30, 6.8% at day 90 and about 3.6% by day 270."),
    ("The first basket is the most consistent lever. ", "Repurchase rises steadily with the number of items in the first purchase (32.4% for one item to 40.7% for seven or more at 90 days), at every horizon and after controls; the product group a customer starts with does not hold its ranking."),
    ("Store customers waited rather than moving online in the 2020 shutdown. ", "Only 19.8% of store-only customers bought online during the closures, but 55.4% bought after reopening, 8.1 points more than in the same months a year earlier."),
    ("A second purchase is worth more than the first. ", "New customers who returned within 90 days had a first-year value 2.7 times that of those who did not, with almost the same first purchase."),
])
p("", bold_lead="Recommendations (ranked by impact relative to cost; each starts as an A/B test)")
bullets([
    ("1. Second-purchase prompt between day 30 and day 60 ", "(personalised picks, time-limited offer). Low cost, uses existing CRM. +3 points of 90-day repurchase would add about 3% to new customers' first-year value and about 0.9% to total sample value (upper bound)."),
    ("2. Grow the first basket ", "(outfit bundles, free-shipping threshold). Low to medium cost; the measured gap is a correlation, so the test decides."),
    ("3. Convert store-only customers to two channels before a store closes ", "(app sign-up, click-and-collect, in-store returns), starting with customers aged 65+. Medium cost; sized small because most of the single-channel lapse gap is explained by buying less."),
], style="List Bullet")
p("Scope: the transaction data is a 2018–2020 sample of H&M members that leans online (70% of rows vs about 30% for the group), so our numbers describe direction and relative size inside the sample; company-wide figures come from H&M's reports.", italic=True, size=9.5, color=GREY)
page_break()

# ------------------------------------------------------------------ 2 introduction
doc.add_heading("2. Introduction", level=1)
doc.add_heading("2.1 The business issue", level=2)
p("H&M is one of the world's largest fashion houses: 81 markets, about 4,100 stores, just over 30% of sales online and net sales of SEK 228 billion in FY2025. "
  "After growth of 12% in FY2021 and 6% in FY2022, sales stalled in FY2023–FY2025, and the store count fell from 4,801 to 4,101 (5,076 at the end of FY2019, 4,023 by FY2026 Q3). "
  "H&M's reports name the concern but not its size: consumers are price-conscious and switch easily (Annual Report 2025, p.9); store closures cost short-term sales, with Q2 2025 growth of +1% instead of +3% excluding closures (Six-month Report 2025, p.3); and the physical store is \"becoming more important than ever\" (Annual Report 2025, p.13). "
  "Member counts are reported, repurchase rates are not.")
figure("fig1_context.png", "H&M group net sales growth and store count, FY2021–FY2025. Source: H&M full-year reports.")
doc.add_heading("2.2 Issues and research questions", level=2)
p("We carry forward the two issues and six research questions from Phases 2–3 unchanged. Issue 3 from Phase 1 (age concentration) is answered inside RQ 2.3.")
table([
    ["Issue", "RQ", "Question"],
    ["1. Stagnant sales and weak retention", "1.1", "What share of new customers buy again within 30, 90 and 365 days, and how does it differ by first-purchase month?"],
    ["", "1.2", "How many days pass between the first and second purchase, and when does the chance of returning drop?"],
    ["", "1.3", "Which first purchases turn a customer into a repeat buyer?"],
    ["2. Store closures and channel shifts", "2.1", "How did online buying behave before, during and after the 2020 closures, and did store customers move online?"],
    ["", "2.2", "How do store-only, online-only and omni customers differ in basket, value and lapse?"],
    ["", "2.3", "Which age groups rely most on stores?"],
], widths=[4.2, 1.0, 11.3], caption="Issues and research questions (unchanged from Phase 3)")
p("The questions are unchanged; the answers are not. Section 2.3 summarises what changed since Phase 3, and Section 3.4 lists each method change with its reason.")
doc.add_heading("2.3 What changed since Phase 3", level=2)
p("The questions stayed the same, but the answers and the recommendations moved. Three of the five outcomes we expected in Phase 3 were not supported, and the centre of the recommendations shifted from protecting channels and older shoppers to winning new customers' second purchase.")
bullets([
    ("Not supported. ", "Everyday basics as the best first purchase: product-group rankings change between 90 and 365 days, and only first-basket size keeps its order. Omni customers buying more per trip: online-only customers buy more per trip (3.98 vs 3.45 items); omni value comes from visiting more often, and after controlling purchase frequency only about 5 of the 36 points of the lapse gap stay with the channel. Shoppers aged 55+ relying on stores: 55–64 is below 16–24, only 65+ is higher, and age explains 0.2% of the variation."),
    ("Narrowed. ", "Phases 1–3 described weak retention across H&M's customers (23.5% of customers observed for a year never returned). The all-customer repeat rate held level with the year before; what weakened was new customers' second purchase (43.4% → 31.0%, a drop of 5–12 points), so we present it as an early signal rather than the cause of today's stagnation."),
    ("Confirmed and strengthened. ", "Store customers did not follow the closures online: only 19.8% of store-only customers bought online during the 2020 closures, and they came back after reopening."),
    ("Recommendations. ", "The re-engagement prompt is kept and now timed at days 30–60. Advertising everyday basics is replaced by growing the first basket. The closure response becomes converting store-only customers to two channels before a store closes, sized small. The in-store app pilot is folded into it, and keeping stores in older neighbourhoods is dropped."),
    ("Measurement. ", "All figures were recomputed on the full data, with a six-month new-customer buffer, observable-only denominators, a pre-shutdown cohort endpoint and formal tests (Section 3.4)."),
])

# ------------------------------------------------------------------ 3 methodology
doc.add_heading("3. Methodology", level=1)
doc.add_heading("3.1 Data", level=2)
table([
    ["Source", "Content", "Size and period"],
    ["Kaggle transactions_train.csv", "One row per item bought: date, customer, article, price (transformed), sales channel 1/2", "31,788,324 rows; 2018-09-20 to 2020-09-22"],
    ["Kaggle customers.csv", "Age, club membership, newsletter flags", "1,371,980 registered customers (1,362,281 bought)"],
    ["Kaggle articles.csv", "Product group, line (index group), department, colour", "105,542 articles, 25 columns"],
    ["H&M reports", "Sales growth, store counts, online share, loyalty members; 952 extracted statements", "43 annual, full-year and quarterly reports, FY2018 to FY2026 Q3"],
], widths=[3.8, 7.7, 5.0], caption="Data sources")
p("The three Kaggle tables join on customer and article IDs; every transaction matches a customer and an article. Missing values are rare (transactions 0%, age 1.2%). "
  "The FN and Active flags in customers.csv are 65–66% blank, but their only value is 1, so a blank means 0 (not set), not missing.")
doc.add_heading("3.2 Preparation and definitions", level=2)
bullets([
    ("Purchase occasion: ", "there is no receipt ID, so all items one customer bought on one day form one purchase (31.8 million rows → 9,080,179 occasions)."),
    ("Online: ", "channel 2 is treated as online. This is an assumption with support: channel 2 is 100% of rows in April 2020, when stores were closed."),
    ("Value: ", "the sum of transformed prices. Prices are rescaled by H&M, so we compare only shares, ratios and changes, never currency amounts."),
    ("New customer: ", "first purchase on or after 2019-03-01. Customers first seen earlier may have shopped before the data starts (left censoring), so the first six months act as a buffer; a 12-month buffer is used as a sensitivity check."),
    ("Repurchase within N days: ", "counted only for customers who can be observed for N days after their first purchase, so late joiners are not counted as non-returners (right censoring)."),
    ("Clean cohorts: ", "for comparisons labelled \"before COVID\", only cohorts whose 90-day window ends before the 2020 closures (first purchase up to November 2019)."),
    ("Analysis tables: ", "from the 9.08 million purchases we built one table per question: 646,685 new customers (451,476 observable for 90 days) for RQ 1.1–1.3; 675,387 customers grouped by their channel before the closures for RQ 2.1; 1,005,899 year-1 customers for RQ 2.2; and 1,346,520 buyers with a known age for RQ 2.3."),
])
doc.add_heading("3.3 Methods", level=2)
p("For each question we followed the course's method-selection steps: name the outcome and its type, decide what one row is, pick the starting method, and name the main trap. "
  "With hundreds of thousands of customers almost every p-value is near zero, so results are read by effect size (percentage points, odds ratios, Cramér's V, η²) and confidence intervals. The need for controls shows in the data: under-25s rose from 23.7% to 30.9% of new customers between March and November 2019, so a falling repurchase rate could simply reflect a younger mix. Model checks: the maximum VIF is 2.1 in both logistic models; robust (HC1) standard errors change no standard error by more than 2.3%; the ANOVA's equal-variance assumption fails (Levene p < 0.001), so a Kruskal–Wallis test was run as well; and because the repurchase model's explanatory power is low (AUC 0.59), we read the size of differences, not individual predictions.")
table([
    ["RQ", "Outcome (type) · row", "Method", "Main trap and how we handled it"],
    ["1.1", "Bought again within 90 days (yes/no) · one new customer", "Cohort rates; chi-square; binary logistic regression with first month, basket, channel, age, line", "Left censoring → 6- and 12-month buffers; COVID → clean cohorts only"],
    ["1.2", "Days to second purchase (time, censored) · one new customer", "Kaplan–Meier survival curve; conditional next-30-day return chance 1 − S(t+30)/S(t)", "Customers not yet back are censored, not dropped"],
    ["1.3", "Bought again within 90 days (yes/no) · one new customer", "Segment comparison by first-basket size and product group; same logistic model", "Seasonality and keen customers → consistency check across horizons and controls"],
    ["2.1", "Bought online during / after closures (yes/no) · one customer", "Prior-year baseline comparison (simplified difference-in-differences); chi-square", "No untreated market → compare with the same months a year earlier"],
    ["2.2", "No purchase in year 2 (yes/no) · one year-1 customer", "Customer-flow table; binary logistic regression controlling year-1 purchases, months observed, age", "Heavy buyers use both channels → control purchase frequency"],
    ["2.3", "In-store share (numeric) · one customer", "One-way ANOVA with η²; Kruskal–Wallis because the share is skewed", "Large n makes tiny gaps significant → read η²"],
], widths=[1.0, 4.3, 5.6, 5.6], caption="Analytical methods by research question", size=8.5)
doc.add_heading("3.4 Changes from the Phase 3 plan", level=2)
p("The Phase 4 instructions allow changes to methods if they are documented with a justification. These are ours:")
table([
    ["Change", "Phase 3 plan", "Now", "Why"],
    ["Figures recalculated", "Phase 1–2 figures from a preliminary audit", "All figures from the full 31.8M rows", "The audit read the first 1,000,000 rows, which cover only 20 Sep–11 Oct 2018, not a random sample"],
    ["New-customer definition", "First purchase = earliest date in the data", "First purchase from 2019-03-01; 12-month buffer as a check", "Earlier first purchases include customers who shopped before the data starts"],
    ["RQ 1.1 endpoint", "Compare cohorts across the period", "Endpoint 2019-11", "Later cohorts' 90-day windows overlap the 2020 closures"],
    ["RQ 1.2 measure", "Gaps between all purchases (median 22 days)", "First-to-second gap with Kaplan–Meier", "The question is about the first return; all gaps are dominated by frequent buyers"],
    ["RQ 1.3 outcome", "Ever bought again", "Bought again within 90 days, observable customers; basket size added", "\"Ever\" favours customers who started early"],
    ["RQ 2.1 view", "Monthly online share only", "Plus customer-level comparison with a prior-year baseline", "The share cannot show whether store customers waited, switched or left"],
    ["Formal tests", "Group comparisons", "Chi-square, logistic regression, ANOVA, Kruskal–Wallis", "To check that gaps are not explained by customer mix"],
], widths=[3.0, 3.8, 4.4, 5.3], caption="Changes from the Phase 3 proposal", size=8.5)
doc.add_heading("3.5 Tools", level=2)
p("Python 3 for all transaction work: pandas and numpy (including the Kaplan–Meier estimator, written directly from its product formula), statsmodels and scipy for the tests, matplotlib for figures; an Excel workbook (analysis/hm_eda_results.xlsx) for result tables and data lineage; "
  "the H&M reports were read from the PDFs and every quoted statement was checked against its source page (analysis/hm_report_statements_full.csv).")

# ------------------------------------------------------------------ 4 findings
doc.add_heading("4. Findings", level=1)
p("Each subsection answers one of four questions that the presentation follows in order: how much less new customers return (RQ 1.1), until when there is a chance (RQ 1.2), what separates those who return (RQ 1.3), and whether store customers move online when stores close (RQ 2.1); RQ 2.2 and 2.3 support the recommendations. Before the questions, the descriptive statistics set the scene. Two thirds of transaction rows are womenswear (64.2%), 70.4% are online (channel 2), the median customer is 32 years old, and value peaks in June. A third of customers (32.9%) bought only once in two years and made 4.8% of value, while the 7.8% who bought 20 or more times made 38.5%. "
  "And from October 2019 to February 2020 the sample's value fell 7.5% year on year while group sales grew about 5%: buying customers fell 4.3% and items per visit fell 6.5%, while price per item rose 4.1% and visits per customer barely moved. "
  "Fewer customers and smaller baskets pointed us to the first questions below. New customers per month also appear to halve (from about 51,000 in March 2019 to 25,000 in February 2020), but much of that is left censoring: spring 2019 \"new\" customers can include existing customers returning after a long gap. From September 2019, with more than 12 months of history, next-month repurchase still falls from 16.0% to 12.7% (January 2020), which is why the questions focus on repurchase.")

doc.add_heading("RQ 1.1 New-customer repurchase by first-purchase month", level=2)
p("New customers' 90-day repurchase rate fell from 43.4% (first purchase March 2019) to 31.0% (November 2019). The 30-day rate fell from 24.3% to 19.9%, and the 365-day rate from 66.2% (March 2019) to 57.3% (September 2019, the last cohort with a full year).", bold_lead="Result. ")
figure("fig2_cohort.png", "90-day repurchase rate by first-purchase month. Red bars are the compared endpoints; light bars are cohorts whose window overlaps the 2020 closures. n = 25,060 to 52,127 per cohort.")
p("The nine clean cohorts differ significantly (χ²(8) = 3,143, Cramér's V = 0.09). A logistic regression on 451,476 new customers controlling first-basket size, first channel, age and product line gives 43.0% → 31.6% (November vs March 2019, odds ratio 0.61, 95% CI 0.59–0.63), so the decline is not just a change in who the new customers were.", bold_lead="Test. ")
p("While H&M was still growing 4–8% a quarter, new customers in the sample were becoming less likely to make a second purchase. This is an early signal for the retention issue H&M faces today.", bold_lead="Meaning. ")
p("Early 2019 cohorts may still contain lapsed existing customers; with a 12-month buffer the drop is 35.8% → 31.0% (−4.8 points, 95% CI 4.0–5.5), so we state the size as 5–12 points. With one clean year, the fall could partly be seasonal. "
  "And the all-customer 90-day repeat rate in October–December 2019 was close to the year before (73.9% → 74.8%, 73.3% → 73.6%, 73.6% → 72.3%): the weakness is specific to new customers.", bold_lead="Caveats. ")

doc.add_heading("RQ 1.2 Time to the second purchase", level=2)
p("Kaplan–Meier estimates that 21.5% of new customers return by day 30, 35.8% by day 90 and 58.1% by day 365. The chance that a customer not yet back returns in the next 30 days is 10.6% at day 30, 6.8% at day 90 and about 3.6% by day 270, after which it flattens at 3.4–3.7%. "
  "Among new customers who returned, the median gap was 47 days and 80% came back within 154 days.", bold_lead="Result. ")
figure("fig3_km.png", "Left: cumulative share returned (Kaplan–Meier). Right: chance of returning in the next 30 days for customers not yet back; the shaded band is days 30–90.")
p("There is no single cliff, but most of the decline happens in the first 90 days, so a reminder has to land between about day 30 and day 60. The Phase 3 figure of 22 days was the median gap between all consecutive purchases, which frequent buyers dominate; it does not describe the first return.", bold_lead="Meaning. ")
p("The curve shows when customers return, not when they are lost for good; a customer who has not returned by the end of the data may still return later.", bold_lead="Caveat. ")

doc.add_heading("RQ 1.3 What turns a first purchase into a repeat purchase", level=2)
p("Repurchase rises steadily with the number of items in the first purchase: 32.4%, 35.9%, 38.2% and 40.7% at 90 days for 1, 2–3, 4–6 and 7+ items, and 58.1% to 65.2% at 365 days. "
  "By first product group the 90-day rate ranges from 29.2% (Nightwear) to 38.1% (Swimwear), a spread similar to basket size, but the spread narrows to 5.8 points at 365 days and the ranking changes; Swimwear's lead is most likely the June sale reaching spring buyers.", bold_lead="Result. ")
figure("fig4_basket.png", "Repurchase rate by number of items in the first purchase, new customers from March 2019 observable for each horizon.")
p("In the same logistic model, a first basket of 7+ items has 1.37 times the odds of a single item (95% CI 1.35–1.40); adjusted repurchase rises from 33.5% to 40.8%. A store first purchase has 1.34 times the odds of an online one. "
  "The model's explanatory power is low (McFadden R² 0.016, AUC 0.59): it measures the direction and size of differences, not who will return.", bold_lead="Test. ")
p("Basket size is the only factor whose order holds at every horizon and after controls, which makes it a usable lever. Phase 3 expected everyday basics to convert best; they do not (Underwear 34.0%, Socks & Tights 32.8%).", bold_lead="Meaning. ")
p("A big first basket may mark a customer who already likes H&M rather than cause the return; only an experiment can separate the two.", bold_lead="Caveat. ")

doc.add_heading("RQ 2.1 The 2020 store closures", level=2)
p("Online's share of rows rose to 85.4% in March–May 2020 (70.1% a year earlier) and 100% in April, then fell to 64.7% in June–August 2020, below 68.8% a year earlier. "
  "At customer level, only 19.8% of the 191,328 customers who used only stores before the closures bought online during them; after reopening, 55.4% bought again, against 47.3% for a group built the same way a year earlier (+8.1 points, 95% CI 7.8–8.4), and 77% of their purchases were back in stores.", bold_lead="Result. ")
figure("fig5_online.png", "Monthly online share of transaction rows; the shaded band is March–May 2020.")
figure("fig6_shutdown.png", "Left: share of each pre-closure group that bought online during the closures. Right: share that bought after reopening, against the same months of 2019.")
p("Purchase behaviour during the closures differs by pre-closure channel type (χ²(2) = 51,121, V = 0.28). Online-only and omni customers were almost exactly at their baselines after reopening.", bold_lead="Test. ")
p("Store customers did not switch online; they waited and came back, apparently with pent-up demand. The assumption behind store closures, that a closed store's customers follow it online, did not hold in 2020.", bold_lead="Meaning. ")
p("This was a temporary, chain-wide shutdown with reopening expected; whether the same holds for permanent closure of a single store is an assumption, and the data has no store or country column to test it. 67,000 customers sit in both years' groups, so the interval is approximate.", bold_lead="Caveat. ")

doc.add_heading("RQ 2.2 Store-only, online-only and omni customers", level=2)
p("Omni customers are 35.5% of customers but 67.7% of value; value per customer is 1.24 for omni, 0.37 for online only and 0.20 for store only. The gap comes from frequency (13.0 occasions vs about 3.1–3.2), not basket size: items per occasion are 3.98 online only, 3.45 omni and 2.72 store only. "
  "Of customers active in the first year, 11.4% of omni customers bought nothing in the second year, against 48.2% of online-only and 47.4% of store-only customers.", bold_lead="Result. ")
figure("fig7_lapse.png", "No purchase in year 2 by year-1 channel type, raw and adjusted (logistic regression on 1,005,899 customers).")
p("Before controls, single-channel customers have about 7 times the lapse odds of omni customers. Controlling year-1 purchases, months observed and age, the odds ratio falls to 1.32 (online only) and 1.37 (store only), 95% CI 1.30–1.40, and adjusted lapse rates are 32.5%, 37.1% and 37.7% (McFadden R² 0.26, AUC 0.83).", bold_lead="Test. ")
p("Most of the single-channel lapse gap, about 31 of 36 points, is explained by single-channel customers buying less to begin with; about 5 points stay with the channel. Phase 3 expected omni customers to buy more per trip; they do not, they come more often. "
  "Store-only customers who became omni gained 79% in value, while those who stayed store-only lost 19%, but this is correlation.", bold_lead="Meaning. ")

doc.add_heading("RQ 2.3 Store dependence by age", level=2)
p("The in-store share of transaction rows is lowest at 25–34 (25.2%) and highest at 65+ (36.6%), in a U shape: 55–64 (32.5%) is below 16–24 (33.2%) and 45–54 (33.3%). Customers aged 65+ pay 18.8% more per item but have half the value per customer of 25–34 (0.41 vs 0.83), and customers aged 16–34 are 55.3% of buyers with a known age.", bold_lead="Result. ")
figure("fig8_age.png", "In-store share of transaction rows by age band (rows with no age, 0.4%, excluded).")
p("A one-way ANOVA of each customer's in-store share across age bands is significant (F = 657) but age explains only 0.2% of the variation (η² = 0.002); Kruskal–Wallis agrees.", bold_lead="Test. ")
p("Only 65+ supports the Phase 2–3 claim that older shoppers rely on stores, and the effect is small. Age is a reasonable way to order a store-closure programme, not a reason to keep stores.", bold_lead="Meaning. ")

doc.add_heading("4.7 Synthesis: what the findings say about H&M's stagnation", level=2)
p("The issues are about 2023–2025, but the transaction data ends in 2020, so we present it as an early signal in four steps. "
  "(1) Today: group sales flat since FY2023 and 1,053 fewer stores between FY2019 Q4 and FY2026 Q3. "
  "(2) Earlier: while the group grew 4–8% a quarter, new customers in the sample were already less likely to return (RQ 1.1) and bought fewer items per visit. "
  "(3) H&M reported fast growth in loyalty members over the same period (from 35 million in FY2019 Q1 to 107 million in FY2020 Q4), which says nothing about whether those members came back. "
  "(4) The boundary: in the same quarters the sample's value fell while group sales grew, and the sample is 70% online against about 30% for the group. "
  "So we claim that the sample's new customers became less likely to return, not that this caused the group's stagnation; testing that link needs H&M's internal data after 2020.")

# ------------------------------------------------------------------ 5 recommendations
doc.add_heading("5. Recommendations", level=1)
p("Each recommendation is tied to a finding, ranked by expected impact relative to cost (which here also runs from lowest to highest cost), and starts as a randomised test, because every gap above is correlational.")
table([
    ["Rank", "Action", "Evidence", "Cost and doability", "Primary metric", "Test"],
    ["1", "Second-purchase prompt (app/email) between day 30 and 60: personalised picks, time-limited offer", "RQ 1.1, 1.2: return chance halves between day 30 and 270; repurchase falling across cohorts", "Low: existing CRM and member contacts; cost = discount on redeemed offers", "90-day repurchase", "Random holdout of new members"],
    ["2", "Grow the first basket: outfit bundles, 'complete the look', free-shipping threshold", "RQ 1.3: 32.4% → 40.7%; OR 1.37 after controls", "Low to medium: recommendation engine exists; margin cost of bundles", "Items in first basket; 90-day repurchase", "A/B on first-time visitors"],
    ["3", "Before a store closes, convert its store-only customers: app sign-up, click-and-collect and returns at the nearest store; 65+ first", "RQ 2.1: only 19.8% went online in 2020; RQ 2.2: +5 points lapse for single-channel; RQ 2.3: 65+ most store-reliant", "Medium: staff time and logistics at nearby stores", "12-month retention of the closed store's customers", "Matched closing stores with vs without the programme"],
], widths=[1.0, 3.8, 3.8, 3.2, 2.4, 2.3], caption="Ranked recommendations", size=8.5)
doc.add_heading("5.1 Sizing the return", level=2)
p("Among 292,217 new customers who first bought between March and September 2019 and can be followed for a year, those who returned within 90 days had almost the same first purchase as those who did not (0.113 vs 0.103), but a first-year value of 0.49 against 0.18, 2.7 times higher. "
  "Each additional point of 90-day repurchase therefore adds about 1% to a new cohort's first-year value; because customers first seen from March 2019 made 28.4% of the sample's last-year value, that is about 0.3% of total sample value.")
table([
    ["Uplift in 90-day repurchase", "New-customer first-year value", "Total sample value"],
    ["+1 point", "+1.0%", "about +0.3%"],
    ["+3 points (planning case)", "+3.1%", "about +0.9%"],
    ["+5 points (back to the September 2019 level)", "+4.9%", "about +1.4%"],
], widths=[6.5, 5.0, 5.0], caption="Impact scenarios for recommendation 1 (sample ratios, upper bound)")
p("Return on investment is ΔRevenue − Cost, with ΔRevenue = N(new) × Δp(90) × V(second purchase). Prices are transformed, so V has to be translated with H&M's reported revenue and customer counts, which is an assumption. "
  "These figures are an upper bound: customers brought back by an offer may spend less than those who return on their own. The A/B test measures the real uplift and the cost of redeemed offers, which together give ROI.")
doc.add_heading("5.2 Feasibility and broader implications", level=2)
bullets([
    ("Why recommendation 1 comes first: ", "it reuses systems H&M already runs (member app, email), its timing comes directly from RQ 1.2, and it can be switched off if the test fails."),
    ("Why recommendation 3 is sized small: ", "after controls only about 5 points of the single-channel lapse gap remain, and the 2020 evidence comes from a temporary closure. It is still worth testing because each permanent closure is irreversible."),
    ("Organisational impact: ", "the three tests share one metric family (repurchase and retention), so they can run in one experimentation programme and inform how H&M reports customer health; today its reports give member counts but no repurchase rate."),
    ("A rule to reject our hypothesis: ", "if H&M's internal data shows that 90-day repurchase of 2023–2025 cohorts has recovered to early-2019 levels, the retention signal is not the driver of today's stagnation and recommendation 1 should be deprioritised."),
])

# ------------------------------------------------------------------ 6 reflection
doc.add_heading("6. Reflection", level=1)
p("Each item below is written as what happened, how we handled it, and the lesson for the next project.")
table([
    ["Challenge", "What happened", "How we handled it", "Lesson"],
    ["A non-random early sample", "Phase 1–2 figures came from the first 1,000,000 rows, which cover only 20 Sep–11 Oct 2018 (214,936 customers; a random sample of that size has about 499,000)", "Recomputed every figure on the full data", "Check the date range and customer count of any subset; sample randomly"],
    ["Censoring at both ends", "Customers first seen early may be old customers; late joiners have not had time to return; later cohorts overlap COVID", "6- and 12-month buffers, observable-only denominators, Kaplan–Meier, clean-cohort endpoint", "Decide what each customer could have done in the window before counting"],
    ["Our own expectations", "Basics did not convert best; omni customers do not buy more per trip; 55–64 are not store-reliant", "Reported as findings and corrected the Phase 2–3 wording", "Treat expected outcomes as hypotheses"],
    ["Mix and causation", "Big gaps (lapse odds of 7) shrank to 1.3 after controlling purchase frequency", "Logistic regression with controls; recommendations start as A/B tests", "Ask who the customers in each group are before reading a gap as an effect"],
    ["Sample vs group", "Sample is 70% online vs about 30%; its value fell while group sales grew", "Claims limited to direction inside the sample; levels from H&M's reports", "Benchmark a sample against official totals early"],
    ["Time gap", "The issues are 2023–2025; the data ends in 2020", "Framed as an early signal with a rejection rule", "State the period each claim is about"],
    ["Large n", "Almost every p-value was near zero", "Read effect sizes (V, η², odds ratios) and intervals", "Significance is not importance"],
], widths=[2.8, 4.6, 4.6, 4.5], caption="Challenges, how they were handled, and lessons", size=8.5)
doc.add_heading("6.1 Limitations", level=2)
bullets([
    "The Kaggle data is a sample of H&M members that leans online; levels such as a 31% repurchase rate are not H&M-wide figures.",
    "Prices are transformed, so value is relative and ROI in currency needs outside figures and an experiment.",
    "Channel 2 = online is an assumption, well supported by April 2020.",
    "There is no store, country, promotion or returns data, so permanent closures and discount-driven first purchases cannot be tested.",
    "Membership and newsletter fields are snapshots at the end of the data, so they were not used as first-purchase features.",
    "With one clean year of new cohorts, the RQ 1.1 decline could be partly seasonal.",
])
doc.add_heading("6.2 Lessons and use of AI", level=2)
p("Three lessons carry to future analytics work. First, define the observation window before computing any rate; most of our corrections were window problems, not arithmetic. "
  "Second, run the formal test even when the chart looks obvious; the channel-lapse result changed from \"half of single-channel customers lapse\" to \"they mostly buy less\". "
  "Third, keep official statements and our own data apart: we extracted 952 statements from H&M's reports, checked each summary against its source page, and labelled every number in the presentation as data, estimate or assumption.")
p("Code and drafts were produced with an AI assistant (Claude). Several of its errors were caught in review, including a wrong observation window, partial months in a comparison and a mislabelled survival-curve value; "
  "every figure in this report was re-derived from the scripts and checked against the aggregate outputs before use.")

# ------------------------------------------------------------------ 7 conclusion
doc.add_heading("7. Conclusion and Next Steps", level=1)
p("The clearest signal in H&M's transaction data is that new customers were becoming less likely to make a second purchase in 2019, while the group was still growing, and that the window to change this is the first 90 days. "
  "The size of the first basket is the most consistent marker of a returning customer. When stores closed in 2020, store customers waited rather than moving online, which makes a bridge to other channels cheaper than assuming they will follow.")
bullets([
    "Run the three A/B tests in Section 5, starting with the day 30–60 second-purchase prompt.",
    "Add store-level, promotion and returns data to test permanent closures and discount-driven first purchases.",
    "Repeat the cohort analysis on 2021–2025 cohorts with H&M's internal data to test the link to today's stagnation.",
])

# ------------------------------------------------------------------ appendices
page_break()
doc.add_heading("Appendix A. Statistical outputs", level=1)
table([
    ["Model", "Row / dependent", "n", "Fit", "Key estimates (95% CI)"],
    ["M1 logistic", "New customer · repurchase within 90 days", "451,476 (165,855 events)", "LR χ²(26) = 9,494; McFadden R² 0.016; AUC 0.59; max VIF 1.8", "First month 2019-11 vs 2019-03 OR 0.61 (0.59–0.63); 2019-09 OR 0.75 (0.73–0.77); basket 7+ vs 1 OR 1.37 (1.35–1.40); 4–6 OR 1.24; 2–3 OR 1.15; store vs online OR 1.34 (1.32–1.35); both OR 2.49"],
    ["M2 logistic", "Year-1 customer · no purchase in year 2", "1,005,899 (365,979 events)", "LR χ²(10) = 346,750; McFadden R² 0.26; AUC 0.83; max VIF 2.1", "Online only vs omni OR 1.32 (1.30–1.34); store only OR 1.37 (1.35–1.40); unadjusted 7.21 and 6.98; log year-1 purchases OR 0.18"],
    ["T1 chi-square", "Clean cohorts 2019-03 to 2019-11 × repurchase", "9 cohorts", "χ²(8) = 3,143", "Cramér's V 0.09; 2019-03 minus 2019-11 = 12.4 points (11.7–13.0); 2019-09 minus 2019-11 = 4.8 (4.0–5.5)"],
    ["T2 chi-square", "Pre-closure channel type × bought online in closures", "675,387 customers", "χ²(2) = 51,121", "Cramér's V 0.28; 19.8% / 36.2% / 55.7%"],
    ["T3 difference", "Store-only customers bought after reopening", "191,328 vs 222,848", "", "55.4% vs 47.3%: +8.1 points (7.8–8.4)"],
    ["T4 ANOVA", "Customer in-store share × age band", "1,346,520", "F = 657; Kruskal–Wallis H = 743", "η² = 0.002"],
], widths=[2.2, 3.6, 2.6, 3.6, 4.5], caption="Full model and test outputs (analysis/hm_tests_results.json); robust (HC1) standard errors change no SE by more than 2.3%", size=8)
doc.add_heading("Appendix B. Formulas", level=1)
bullets([
    "90-day repurchase rate (cohort m) = customers first buying in month m who buy again within 90 days ÷ customers first buying in m who can be observed for 90 days.",
    "Kaplan–Meier: S(t) = Π (1 − dᵢ/nᵢ) over days up to t, where dᵢ returned on day i and nᵢ had not returned and were still observed; next-30-day chance = 1 − S(t+30)/S(t).",
    "Odds ratio = [p₁/(1 − p₁)] ÷ [p₀/(1 − p₀)]; adjusted rate = mean predicted probability with every customer set to the group (g-computation).",
    "Cramér's V = √[χ² ÷ (n × (min(rows, columns) − 1))]; η² = between-group sum of squares ÷ total sum of squares.",
    "Sales decomposition: value = customers × visits per customer × items per visit × price per item, each compared with the same months a year earlier.",
])
doc.add_heading("Appendix C. Files to reproduce the analysis", level=1)
p("All files are in the project repository; the raw Kaggle data is not redistributed and must be downloaded from Kaggle under its terms.")
bullets([
    "analysis/hm_eda_cycle1.py, analysis/hm_eda_cycle2.py: cohorts, Kaplan–Meier, channel and closure analyses.",
    "analysis/hm_tests.py → analysis/hm_tests_results.json: chi-square, logistic regressions, ANOVA.",
    "analysis/hm_profile.py: column profile and descriptive statistics (aggregates in data/profile/).",
    "analysis/hm_eda_results.xlsx: result tables, charts and the L_Lineage sheet mapping every figure to its source.",
    "analysis/hm_report_quarterly.csv, hm_report_statements_full.csv, hm_report_statements_essential.csv: figures and verified statements from 43 H&M reports.",
    "report/phase4/make_figs.py, make_report.py: this report's figures and document.",
])
doc.add_heading("Appendix D. References", level=1)
bullets([
    "H&M Group (2022). H&M Personalized Fashion Recommendations [dataset]. Kaggle.",
    "H&M Group. Annual reports FY2018–FY2025; full-year reports FY2018–FY2025; quarterly reports FY2018–FY2026 Q3.",
    "Kaplan, E. L. & Meier, P. (1958). Nonparametric estimation from incomplete observations. Journal of the American Statistical Association, 53(282), 457–481.",
    "Fader, P. S., Hardie, B. G. S. & Lee, K. L. (2005). \"Counting your customers\" the easy way. Marketing Science, 24(2), 275–286.",
    "Shadish, W. R., Cook, T. D. & Campbell, D. T. (2002). Experimental and Quasi-Experimental Designs for Generalized Causal Inference. Houghton Mifflin.",
])

doc.save(OUT)
print("wrote", OUT)
