"""English text for the H&M EDA results workbook (hm_eda_workbook.py).

Same structure and numbers as hm_eda_text.py (Korean). Numbers quoted here were
read from the tables the workbook writes next to them; re-check them if the
analysis code changes.
"""

LANG = "en"
FIELD_LABELS = ["Question / link", "What we looked at", "Observation"]
PAGES = {
    "overview": {"sheet": "00_Overview", "title": "H&M EDA results (Kaggle transactions, 2018-09-20 to 2020-09-22)",
                 "header": ["Item", "Description"], "widths": [22, 120]},
    "questions": {"sheet": "Q_Candidates", "title": "Question candidates from cycle 1",
                  "header": ["ID", "Question candidate", "Cycle 1 evidence", "Evidence sheet"], "widths": [6, 48, 80, 26]},
    "union": {"sheet": "U_Union", "title": "Question candidates ∪ issue list → cycle 2 items",
              "header": ["ID", "Sources", "Combined question", "Cycle 2 analysis", "Sheet"], "widths": [6, 22, 48, 70, 26]},
    "findings": {"sheet": "R_Findings", "title": "Cycle 2 results: answer, defined problem, solution direction",
                 "header": ["ID", "Combined question", "Cycle 2 result (answer)", "Defined problem", "Solution direction (hypothesis)"],
                 "widths": [6, 36, 70, 44, 52]},
    "lineage": {"sheet": "L_Lineage", "title": "Data lineage: which CSV, which columns and how, for every table",
                "header": ["Sheet", "Table", "CSV", "Columns used", "Join key", "Grouped by (GROUP BY)", "Filter / period", "Calculation"],
                "widths": [20, 34, 26, 40, 14, 30, 34, 60]},
    "limits": {"sheet": "Z_Limitations", "title": "Assumptions and limitations", "header": ["Item", "Description"],
               "widths": [22, 120]},
}

OVERVIEW = [
    ["Purpose", "Use EDA on H&M transaction data to find questions, merge them with the existing issue list, and define problems and solution directions."],
    ["Method (2 cycles)",
     "Cycle 1: a broad pass with no hypothesis (monthly trend, new vs returning, cohorts, frequency, channel, age, membership, product lines, seasonality, price) → question candidates Q1-Q11.\n"
     "Union: Q1-Q11 ∪ Issue 1-3, overlaps merged → cycle 2 items U1-U9.\n"
     "Cycle 2: one targeted analysis per U item → the Findings sheet gives the answer, the defined problem and a solution direction (hypothesis)."],
    ["Issue list (existing)",
     "Issue 1. Stagnant sales and weak customer retention / Issue 2. Shrinking store network and shift to online / Issue 3. Customer age concentration (analysis/hm_phase1_results.md)"],
    ["Data", "Kaggle h-and-m-personalized-fashion-recommendations: transactions_train.csv 31,788,324 rows (2018-09-20 to 2020-09-22), "
             "customers.csv 1,371,980 customers, articles.csv 105,542 articles. This file holds results (aggregate tables) only, no raw rows."],
    ["Definitions", "Occasion = one customer on one day. Row = one item bought. value = sum of price (a transformed value, not a real currency → read as ratios only). "
                    "Channel 2 = online (assumption). Y1 = 2018-09-20 to 2019-09-19, Y2 = 2019-09-20 to 2020-09-22."],
    ["Sheet layout", "C1_* and C2_* sheets: question and observation at the top, charts below (two per row), source tables at the bottom. Charts reference the tables, so editing a table updates its chart."],
    ["Sheet order", "00_Overview → C1_* (cycle 1 results) → Q_Candidates → U_Union → C2_* (cycle 2 results) → R0_MainQuestion → R_Findings → L_Lineage → Z_Limitations"],
    ["Regenerate", "python analysis/hm_eda_workbook.py (the first run builds a parquet cache in data/hm/)"],
]

SHEETS = [
    # ------------------------------------------------------------ cycle 1
    {"cycle": 1, "sheet": "C1_01_Monthly", "title": "Monthly value, customers and online share",
     "tables": [("By month", "c1.monthly")],
     "link": "→ Q1",
     "what": "Rows, value, purchasing customers and online row share per month, with change vs the same month a year earlier.",
     "obs": "Value fell -0.4% to -13.9% year on year in 2019-10 to 2020-02, before COVID. In 2020-03 to 07 it fell -11.5% to -19.9%. "
            "Online share was 100% in 2020-04. 2018-09 and 2020-09 are partial months."},
    {"cycle": 1, "sheet": "C1_02_Weekday", "title": "Average rows and online share by weekday",
     "tables": [("Daily average by weekday", "c1.weekday")],
     "link": "→ Q6",
     "what": "Average rows per day and online row share by weekday.",
     "obs": "Saturday has the most rows (48,090) and the lowest online share (58.6%). Sunday and Monday are 77-78% online. Store demand peaks at the weekend."},
    {"cycle": 1, "sheet": "C1_03_NewCustomers", "title": "New customers among monthly active customers",
     "tables": [("By month", "c1.new_vs_returning")],
     "link": "→ Q2",
     "what": "Customers whose first purchase in the data falls in that month. In the first months after the data starts, existing customers also count as 'new', so read only from 2019-03.",
     "obs": "New customers: 49k-52k a month in 2019-03 to 06 → 25k-37k a month in 2019-08 to 2020-02. A spike to 41k in 2020-04 (100% online)."},
    {"cycle": 1, "sheet": "C1_04_Cohorts", "title": "Share of each first-purchase-month cohort buying again in month k (%)",
     "tables": [("Cohort x months since first purchase (share buying at least once in M+k)", "c1.cohort")],
     "heat": ["M+1", "M+12"],
     "link": "→ Q3",
     "what": "For each first-purchase month (cohort), the share that bought again k months later. The 2018-09 to 2019-02 cohorts include existing customers and look higher.",
     "obs": "M+1 repurchase: 19.5% for the 2019-03 cohort → 11.8% for the 2020-02 cohort. Cohorts from late 2019 on are lower. Every cohort rises around June (summer sale).",
     },
    {"cycle": 1, "sheet": "C1_05_Frequency", "title": "Customers and value by number of purchase occasions (2 years)",
     "tables": [("Purchase occasion bands", "c1.frequency")],
     "link": "→ Q4",
     "what": "Share of customers and of value by the number of purchase occasions (customer x day) over two years.",
     "obs": "One-time buyers are 32.9% of customers and 4.8% of value. Customers with 20+ occasions are 7.8% of customers and 38.5% of value. Sales depend heavily on a small group of frequent buyers."},
    {"cycle": 1, "sheet": "C1_06_ChannelType", "title": "Customer channel type (whole 2 years)",
     "tables": [("Channel type", "c1.channel_mix")],
     "link": "→ Q5",
     "what": "Customers split by the channels they used over two years: online only / store only / both (omni).",
     "obs": "Omni customers are 35.5% of customers and 67.7% of value. Value per customer: omni 1.24, online only 0.37, store only 0.20 (omni is 3.4x and 6.2x)."},
    {"cycle": 1, "sheet": "C1_07_Basket", "title": "Basket by channel used that day",
     "tables": [("Channel used that day", "c1.basket_channel")],
     "link": "→ Q6",
     "what": "Items and value per purchase occasion (customer x day), by channel used that day.",
     "obs": "Online 4.09 items, store 2.55, both on the same day 6.08. Online baskets are 1.6x larger."},
    {"cycle": 1, "sheet": "C1_08_Age", "title": "Customer value and channel by age band",
     "tables": [("Age band", "c1.age_profile")],
     "link": "→ Q7, Issue 3",
     "what": "Rows per customer, value, online share and omni share of purchasing customers, by age band.",
     "obs": "25-34 have the most rows per customer (29.6); 16-24 have 18.4. Omni share is 41.7% for 25-34 and 17.8% for 65+."},
    {"cycle": 1, "sheet": "C1_09_Membership", "title": "Customer value by membership status and newsletter",
     "tables": [("By field", "c1.member_profile")],
     "link": "→ Q8",
     "what": "Rows per customer and online share of purchasing customers, by club_member_status and fashion_news_frequency.",
     "obs": "PRE-CREATE (sign-up not completed), 92,578 customers: 7.1 rows per customer, 99.8% online. ACTIVE: 24.6 rows. Newsletter Regularly 28.7 rows vs NONE 20.7."},
    {"cycle": 1, "sheet": "C1_10_LineShare", "title": "Monthly value share by product line (index group, %)",
     "tables": [("By month", "c1.line_trend")],
     "link": "→ Q9",
     "what": "Share of each index group in monthly value.",
     "obs": "Baby/Children share 8.0% (2018-09) → 1.6% (2020-09). Ladieswear 60.4% → 64.5% (71.7% in 2020-06)."},
    {"cycle": 1, "sheet": "C1_11_Seasonality", "title": "Monthly share by product group (2018-10 to 2019-09, each month once)",
     "tables": [("Product group x month (row share %)", "c1.seasonality")],
     "heat": ["M01", "M12"],
     "link": "→ Q10",
     "what": "Share of each product group's yearly sales by calendar month. peak_to_trough = busiest month / quietest month.",
     "obs": "Swimwear: 20.5% in June, 1.4% in November, a 14.5x gap. Full body garments 3.6x. Upper body is flat at 1.4x."},
    {"cycle": 1, "sheet": "C1_12_PriceRange", "title": "Price range of the same article (articles with 50+ rows)",
     "tables": [("How far the p05 price is below the p95 price", "c1.price_drop")],
     "link": "→ Q10",
     "what": "For each article, how many % its 5th-percentile selling price is below its 95th. Size of discounts and channel price gaps.",
     "obs": "For 44.5% of articles the 5th-percentile price is 50% or more below the 95th. The same article sells at very different prices."},
    {"cycle": 1, "sheet": "C1_13_Launches", "title": "Articles first sold per month",
     "tables": [("First-sale month", "c1.launches")],
     "link": "Reference",
     "what": "Articles first sold in each month and their later sales. Recent months have short observation windows, so days on sale and sales look small (read with care).",
     "obs": "2,000-4,000 new articles a month. 2018-10 is understated because the data has just started."},
    {"cycle": 1, "sheet": "C1_14_Concentration", "title": "Article sales concentration",
     "tables": [("Share of top articles", "c1.concentration")],
     "link": "→ Q11",
     "what": "Share of all rows taken by the top x% of articles by rows.",
     "obs": "The top 1% of articles (1,045) make 18.6% of rows, the top 10% make 60.8%, the bottom 50% make 3.2%."},

    # ------------------------------------------------------------ cycle 2
    {"cycle": 2, "sheet": "C2_U1_SalesDecomp", "title": "U1. Decomposition of the sales decline (% vs same month a year earlier)",
     "tables": [("value = customers x occasions per customer x items per occasion x price per item", "c2.decomp")],
     "link": "U1 = Issue 1 (stagnant sales) + Q1",
     "what": "Year-on-year change in value split into four factors. The total rows use unique customers over the whole period.",
     "obs": "Before COVID (2019-10 to 2020-02) -7.5%: customers -4.3%, items per occasion -6.5%, price per item +4.1%. "
            "2020-03 to 08 -12.1%: unique customers +1.8% but occasions per customer -10.3%."},
    {"cycle": 2, "sheet": "C2_U2_Repurchase", "title": "U2. First repurchase of new customers (first purchase from 2019-03)",
     "tables": [("30-, 90- and 365-day repurchase rate by first-purchase month", "c2.rep_by_month"),
                ("Days to the second purchase", "c2.rep_gap"),
                ("By first-purchase channel", "c2.rep_by_channel"),
                ("By items in the first basket", "c2.rep_by_basket"),
                ("By main line of the first basket", "c2.rep_by_line"),
                ("By age band", "c2.rep_by_age")],
     "link": "U2 = Issue 1 (retention) + Q3",
     "what": "Share buying again within 30, 90 and 365 days of the first purchase. Only customers with that much observation time left are included (n). Segments are as of the first purchase.",
     "obs": "90-day repurchase fell from 43.4% (2019-03) to 29.8% (2020-02), before COVID. 41.0% of repeat buyers return within 30 days, 20.2% within 7 days. "
            "First basket of 1 item 32.4% vs 7+ items 40.7%. First purchase in store 41.4% vs online 34.2%. Age makes little difference (31.7-38.0%)."},
    {"cycle": 2, "sheet": "C2_U3_Acquisition", "title": "U3. New customers per month and their mix",
     "tables": [("New customers by first-purchase month (age band %, first channel %)", "c2.new_mix")],
     "link": "U3 = Q2 + Issue 3",
     "what": "Monthly count and age / channel mix of customers whose first purchase is from 2019-03.",
     "obs": "Share of 16-24 among new customers: 24.1% (2019-03) → 37-40% (2020-03 to 08). New customers are getting younger. The 35-44 and 55-64 shares fell."},
    {"cycle": 2, "sheet": "C2_U4_ChannelShift", "title": "U4. Channel type shift (Y1 → Y2) and behaviour during store closures",
     "tables": [("Y2 type distribution by Y1 channel type (%)", "c2.migration"),
                ("Change in value per customer by Y1 type x Y2 type", "c2.migration_value"),
                ("By channel type in 2019-09-20 to 2020-02: behaviour during closures (2020-03-15 to 05-31) and after reopening (2020-06 on)", "c2.covid_store")],
     "heat": ["omni", "no purchase"],
     "link": "U4 = Issue 2 (store network, online) + Q5 + Q6",
     "what": "Change in channel type and value for the same customers from Y1 to Y2. For each pre-closure channel type, whether they bought during closures and after reopening, and through which channel.",
     "obs": "About half of Y1 single-channel customers bought nothing in Y2 (online only 48.2%, store only 47.4%) vs 11.4% of omni. "
            "Store-only customers who became omni: value per customer +79%; those who stayed store only: -19%. "
            "Of store-only customers before closures, 19.8% bought online during closures; after reopening 77% of their purchases were still in store."},
    {"cycle": 2, "sheet": "C2_U5_AgeShift", "title": "U5. Age mix change (Y1 vs Y2) and product lines by age",
     "tables": [("Customers and value share by age band, Y1 vs Y2", "c2.age_years"),
                ("Line share of each age band's value (%, whole 2 years)", "c2.age_mix")],
     "link": "U5 = Issue 3 (age concentration) + Q7",
     "what": "Purchasing customers and value share by age band in the two years. Which lines each age band buys.",
     "obs": "16-24 purchasing customers +20.9%, value share 17.3% → 21.2% (+4.0pp). 35-44 customers -15.2%. The 16-34 value share rose from 54.5% to 57.6%, so concentration grew. "
            "16-24 spend 28.3% of value on Divided; 65+ spend 76.6% on Ladieswear."},
    {"cycle": 2, "sheet": "C2_U6_TopCustomers", "title": "U6. Y2 retention and spending change by Y1 value decile",
     "tables": [("Y1 value decile (D1 = top 10%)", "c2.heavy"),
                ("Where Y2 value comes from", "c2.y_split")],
     "link": "U6 = Q4 + Issue 1",
     "what": "Y1 customers ranked by value into ten groups: did they buy in Y2, and how much did their spending change. Y2 value split into existing and new customers.",
     "obs": "",  # filled below from the y_split numbers
     },
    {"cycle": 2, "sheet": "C2_U7_Children", "title": "U7. Articles sold (supply) and sales per article (demand) by line",
     "tables": [("By month", "c2.line_supply")],
     "link": "U7 = Q9",
     "what": "Articles sold at least once in each month (active_articles) and rows per article (rows_per_article).",
     "obs": "Baby/Children articles sold 9,501 (2019-01) → 5,116 (2020-08), -46%. Rows per article 9.8 → 4.2, -57%. Supply and demand per article fell together. "
            "Ladieswear articles sold rose from 12,887 to 15,465."},
    {"cycle": 2, "sheet": "C2_U8_Membership", "title": "U8. Newsletter and membership effect (controlling for age band)",
     "tables": [("Rows per customer by age band", "c2.member_age"),
                ("New-customer repurchase rate by membership status", "c2.rep_by_club"),
                ("New-customer repurchase rate by newsletter", "c2.rep_by_news")],
     "link": "U8 = Q8",
     "what": "Within each age band: newsletter Regularly vs NONE, ACTIVE vs PRE-CREATE. Repurchase rate of new customers by sign-up status.",
     "obs": "In every age band, Regularly customers have 35-67% more rows per customer than NONE (25-34: 36.3 vs 26.9). "
            "New-customer 90-day repurchase: Regularly 42.9% vs NONE 33.6%, PRE-CREATE 19.8% vs ACTIVE 37.6%."},
    {"cycle": 2, "sheet": "C2_U9_Markdown", "title": "U9. Selling price vs launch price (median of the first 28 days = 1.0)",
     "tables": [("By month: share of rows sold 30%+ below launch price", "c2.md_month"),
                ("By weeks since launch", "c2.md_age")],
     "link": "U9 = Q10",
     "what": "Each selling price as a ratio to the article's launch price (median price in its first 28 days). Only articles first sold from 2018-10-20.",
     "obs": "",  # filled below
     },
]

QUESTIONS = [
    ["Q1", "Did sales fall before COVID? If so, because of fewer customers or less buying per customer?",
     "2019-10 to 2020-02 value -0.4% to -13.9% year on year; purchasing customers -7.3% to +3.2% over the same months.", "C1_01_Monthly"],
    ["Q2", "Is customer acquisition shrinking? Who are the new customers?",
     "New customers about 50k a month in 2019-03 to 06 → 25k-37k in 2019-08 to 2020-02.", "C1_03_NewCustomers"],
    ["Q3", "Do recent cohorts repurchase less after their first purchase? What drives the first repurchase?",
     "M+1 repurchase 19.5% for the 2019-03 cohort → 11.8% for the 2020-02 cohort.", "C1_04_Cohorts"],
    ["Q4", "Is relying on a few frequent buyers risky? Are they leaving or spending less?",
     "Customers with 20+ occasions: 7.8% of customers, 38.5% of value. One-time buyers: 32.9% of customers, 4.8% of value.", "C1_05_Frequency"],
    ["Q5", "Are omni customers simply big spenders, or does adding a channel make them buy more?",
     "Omni: 35.5% of customers = 67.7% of value. Value per customer omni 1.24 vs online only 0.37 vs store only 0.20.", "C1_06_ChannelType"],
    ["Q6", "Do stores and online play different roles? (basket size, weekday)",
     "Items per occasion online 4.09 vs store 2.55. Online share Saturday 58.6% (lowest), Sunday 78.1%.", "C1_07_Basket, C1_02_Weekday"],
    ["Q7", "Where do value differences between age bands come from? Is the young group lower value?",
     "Rows per customer 25-34 29.6 vs 16-24 18.4 vs 65+ 13.3. Omni share 65+ 17.8%.", "C1_08_Age"],
    ["Q8", "Is there room to activate PRE-CREATE (sign-up not completed) and non-newsletter customers?",
     "PRE-CREATE 92,578 customers at 7.1 rows per customer (ACTIVE 24.6). Newsletter Regularly 28.7 rows vs NONE 20.7.", "C1_09_Membership"],
    ["Q9", "Is the drop in the children's line share a fall in demand or a smaller range?",
     "Baby/Children value share 8.0% (2018-09) → 1.6% (2020-09).", "C1_10_LineShare"],
    ["Q10", "How much do sales depend on discounts and seasonal sales?",
     "For 44.5% of articles the 5th-percentile price is 50%+ below the 95th. Swimwear's monthly share varies 14.5x.", "C1_12_PriceRange, C1_11_Seasonality"],
    ["Q11", "Is the assortment a long tail?",
     "The top 10% of articles make 60.8% of rows; the bottom 50% make 3.2%.", "C1_14_Concentration"],
]

UNION = [
    ["U1", "Issue 1 + Q1", "Is the sales decline driven by customers, frequency, basket size or price?",
     "Year-on-year value change split into four factors; totals before and after COVID.", "C2_U1_SalesDecomp"],
    ["U2", "Issue 1 + Q3", "Is the first repurchase of new customers weakening? What drives it?",
     "30-, 90- and 365-day repurchase of customers first buying from 2019-03, by first-purchase month, channel, basket, line and age.", "C2_U2_Repurchase"],
    ["U3", "Q2 + Issue 3", "Is acquisition shrinking? What age and channel are new customers?",
     "New customers per month and their age and first-channel mix.", "C2_U3_Acquisition"],
    ["U4", "Issue 2 + Q5 + Q6", "Did store customers move online? Do customers who add a channel buy more?",
     "Y1 → Y2 channel type shift and value change of the same customers. Behaviour during closures and after reopening by pre-closure channel type.", "C2_U4_ChannelShift"],
    ["U5", "Issue 3 + Q7", "Is age concentration growing? What does each age band buy?",
     "Purchasing customers and value share by age band, Y1 vs Y2. Line mix by age band.", "C2_U5_AgeShift"],
    ["U6", "Q4 + Issue 1", "Is lower spending or churn by top customers behind the sales decline?",
     "Y2 active share and spending change by Y1 value decile. Y2 value split into existing and new customers.", "C2_U6_TopCustomers"],
    ["U7", "Q9", "Is the children's line shrinking because of a smaller range or lower demand?",
     "Articles sold and rows per article by line and month.", "C2_U7_Children"],
    ["U8", "Q8", "Do newsletter and fully signed-up customers buy more even within the same age band?",
     "Within age bands: Regularly vs NONE, ACTIVE vs PRE-CREATE. New-customer repurchase rate.", "C2_U8_Membership"],
    ["U9", "Q10", "From when, and how much, are articles sold below launch price?",
     "Selling price vs launch price per article. Share of rows 30%+ below launch price by month and by weeks since launch.", "C2_U9_Markdown"],
    ["-", "Q6 (part), Q11", "Basket and weekday differences, assortment long tail",
     "Cycle 1 facts are enough. Not a separate cycle 2 item; used when reading U4 (channel). Q11 is outside the scope of this proposal and is set aside.", "-"],
]

FINDINGS = []  # filled by fill() after the tables are computed
LIMITS = [
    ["Channel", "sales_channel_id has no official definition. Channel 2 is assumed to be online and channel 1 stores."],
    ["Price", "price is a transformed value. Read as ratios and changes only, not amounts. The markdown analysis (U9) uses price relative to each article, so the unit does not matter."],
    ["Observation window", "2018-09-20 to 2020-09-22. 'New' customers and early cohorts right after the start include existing customers (new customers are read only from 2019-03). "
                           "Recent customers have short observation windows (repurchase rates include only customers that can be observed long enough)."],
    ["Causality", "Differences for omni shift (U4) and newsletter (U8) are correlations. Customers who already buy a lot may be the ones adding a channel or subscribing. Confirm with experiments (A/B tests)."],
    ["Regression to the mean", "In U6, the Y2 drop for Y1 top customers and the rise for bottom customers are partly regression to the mean (a year of unusually high or low buying)."],
    ["COVID", "Y2 includes the store closures of 2020-03 to 05. U1, U6 and U4 look at the pre-COVID period separately or are read with that in mind."],
    ["Sample", "The data was released for a Kaggle competition and may not represent all H&M markets or sales (for example, the children's line decline may come from how the data was extracted)."],
    ["Age", "From registration data, about 1.2% missing. One account may be used by more than one person."],
]


def fill(tables):
    """Fill text that depends on numbers computed at run time."""
    fill_main(tables, 'The 365-day rate went from {va:.1f}% for {a} first purchases to {vb:.1f}% for {b} (the last cohort observable for 365 days).',
              'Share buying after reopening (2020-06 to 09): store-only customers before the closures {s20:.1f}% (same months a year earlier: {s19:.1f}%), '
              'online only {o20:.1f}% ({o19:.1f}%), omni {m20:.1f}% ({m19:.1f}%). There is no sign that store customers left because of the closures.')
    ys = tables["c2.y_split"].set_index("part")
    y1, old, new, y2 = (ys.loc[k] for k in ["Y1 total", "Y2 from Y1 customers", "Y2 from customers new in Y2", "Y2 total"])
    hv = tables["c2.heavy"].set_index("decile")
    md = tables["c2.md_month"].set_index("month")
    mda = tables["c2.md_age"].set_index("weeks_since_launch")
    u6 = (f"The Y1 top 10% (D1) made {hv.loc['D1', 'share_of_y1_value_pct']:.1f}% of Y1 value. {hv.loc['D1', 'active_in_y2_pct']:.0f}% of them bought again in Y2, "
          f"but their spending changed {hv.loc['D1', 'value_y2_vs_y1_pct']:.1f}% (D2 {hv.loc['D2', 'value_y2_vs_y1_pct']:.1f}%). "
          f"Y2 value was {y2.vs_y1_total_pct:.1f}% of Y1: {old.vs_y1_total_pct:.1f}% from existing customers + {new.vs_y1_total_pct:.1f}% from new customers.")
    u9 = (f"{md.loc['all months', 'rows_30pct_below_pct']:.1f}% of all rows sold 30%+ below launch price, concentrated in sale months: "
          f"2019-07 {md.loc['2019-07', 'rows_30pct_below_pct']:.1f}%, 2019-12 {md.loc['2019-12', 'rows_30pct_below_pct']:.1f}%. "
          f"{mda.loc['12-15w', 'rows_30pct_below_pct']:.1f}% at 12-15 weeks after launch, about 40% at 20-31 weeks. "
          f"2020-06 was {md.loc['2020-06', 'rows_30pct_below_pct']:.1f}%, about twice the {md.loc['2019-06', 'rows_30pct_below_pct']:.1f}% a year earlier (the sale started earlier).")
    for s in SHEETS:
        if s["sheet"] == "C2_U6_TopCustomers":
            s["obs"] = u6
        if s["sheet"] == "C2_U9_Markdown":
            s["obs"] = u9
    FINDINGS[:] = [
        ["U1", "What drives the sales decline?",
         "Before COVID (2019-10 to 2020-02) value -7.5%: items per occasion -6.5%, customers -4.3%, price per item +4.1%. "
         "Prices rose, while the number of items bought at once and the number of buyers fell. In 2020-03 to 08 the main driver was purchase frequency per customer, -10.3%.",
         "Smaller baskets + fewer buying customers (not a price problem).",
         "Grow baskets: outfit and bundle recommendations, a free-shipping threshold, 'bought together' recommendations. Address buyer numbers together with U2 and U3."],
        ["U2", "Is the first repurchase weakening? What drives it?",
         "New-customer 90-day repurchase fell from 43.4% (2019-03) to 29.8% (2020-02), before COVID. 41% of repeat buyers return within 30 days, 20% within 7 days. "
         "Higher for bigger first baskets (1 item 32.4% → 7+ items 40.7%), first purchase in store (41.4% vs online 34.2%), ACTIVE members and newsletter subscribers. Age makes little difference.",
         "New customers convert to a second purchase within 90 days less and less, especially online, single-item and not-signed-up new customers.",
         "30-day onboarding after the first purchase: personalised recommendations within 7 days, a second-purchase coupon, prompts to complete sign-up and opt in to the newsletter at first purchase. KPI = new-customer 90-day repurchase rate."],
        ["U3", "Is acquisition shrinking? Who is coming in?",
         "New customers about 50k a month in H1 2019 → 25k-37k in 2019-08 to 2020-02. The 16-24 share of new customers rose from 24% to 37-40%. 41k new online customers arrived during the 2020-04 closures.",
         "Fewer new customers, and new customers shifting to a younger, lower-value group.",
         "Stronger acquisition channels for 25-44. A programme that turns large acquisition waves, like the online newcomers of 2020-04, into repeat buyers (linked to U2)."],
        ["U4", "Did store customers move online? Does adding a channel help?",
         "About half of Y1 single-channel customers bought nothing in Y2 (online only 48.2%, store only 47.4%) vs 11.4% of omni. Store only → omni: value +79%; online only → omni: +28%; staying single-channel: -14% to -19%. "
         "Of store-only customers before closures, only 19.8% bought online during closures, and after reopening 77% of their purchases were in store.",
         "High churn of single-channel customers. Store customers did not move online (the 'shift to online' in Issue 2 was temporary, during closures).",
         "Connect store customers to online: link the app or membership at store checkout, click & collect, online recommendations after a store purchase. The omni effect needs causal testing (experiment)."],
        ["U5", "Is age concentration growing?",
         "16-24 purchasing customers +20.9%, value share 17.3% → 21.2%. 35-44 customers -15.2%. 16-34 value share 54.5% → 57.6%. 16-24 value per customer is about 58% of 25-34.",
         "The customer base is tilting to a younger, lower-value group while 35-44 drop away (Issue 3 is getting stronger).",
         "Reactivate 35-54 (recommendations around the Ladieswear and Menswear they buy); raise frequency for 16-24 (alerts for new Divided items)."],
        ["U6", "Is lower spending by top customers behind the sales decline?",
         u6 + " (partly regression to the mean)",
         "A large part of the decline comes from existing top customers spending less. The problem is buying less, more than leaving.",
         "VIP management for the top two deciles: early detection of falling spend (dropping purchase frequency), personalised new arrivals and exclusive benefits."],
        ["U7", "Why is the children's line shrinking?",
         "Baby/Children articles sold -46%, rows per article -57% (2019-01 → 2020-08). The range and demand per article shrank at the same time.",
         "Children's line demand and range shrank together. This may come from the Kaggle sample extraction.",
         "Outside the core scope of this proposal. If covered, review with U5 together with 35-44 customers (7.2% of their value is children's line)."],
        ["U8", "Do newsletter and full sign-up make a difference within the same age band?",
         "In every age band Regularly customers have 35-67% more rows per customer than NONE. New-customer 90-day repurchase Regularly 42.9% vs NONE 33.6%, PRE-CREATE 19.8% vs ACTIVE 37.6%.",
         "92,578 PRE-CREATE customers and 870k non-subscribers are low-activity.",
         "Experiments (A/B tests) on prompts to complete sign-up and opt in to the newsletter. The gap may be correlation, so confirm the effect with an experiment."],
        ["U9", "How much do sales depend on markdowns?",
         u9,
         "From 12 weeks after launch, 30-40% of sales are 30%+ below launch price → the full-price selling period is short.",
         "Sell more at full price in the first 8-12 weeks: personalised exposure of new arrivals, demand forecasting to size initial stock. (Read together with the +4.1% price per item in U1.)"],
    ]


# Main-question sheet (R0): the question, the 4-step narrative with its numbers, the charts,
# how it answers the draft's research questions, a check of the draft's figures, solution
# directions and limits. Report figures come from hm_report_quarterly.csv; "{rep365}" is filled
# in by fill_main() from the 365-day repurchase table.
MAIN = {
    "sheet": "R0_MainQuestion",
    "title": "Main question: why do fewer new customers come back for a second purchase?",
    "lead": "H&M group sales have been flat for four years since Q3 2022, and the store network is shrinking. The Kaggle sample (2018-09 to 2020-09) "
            "shows an earlier weakness: while the group was still growing, fewer new customers were converting to a second purchase. In the same period "
            "H&M tripled its loyalty programme. This sheet sets out the evidence for making this the main question, the answers to the draft's research "
            "questions (RQ), and the limits.",
    "columns": {"sales": "Group sales growth (local currencies, %)", "kaggle": "Kaggle data period",
                "stores": "Stores (period end)", "members": "Loyalty members (million)"},
    "data_label": "Chart source data (used by the charts above)",
    "sections": [
        {"heading": "Questions", "header": ["Type", "Question", "Link", "Phase 2 RQ"], "rows": [
            ["Main question", "Why is the repurchase rate of H&M's new customers after their first purchase falling, and which first-purchase experiences lead to a second purchase?", "Issue 1 + Q3 → U2", "RQ1.1, RQ1.2"],
            ["Sub-question 1", "Among which customers and product lines did the number of items per purchase fall?", "Issue 1 + Q1 → U1", "Not in Phase 2 (new; links to first-basket size in RQ1.2)"],
            ["Sub-question 2", "Is the repurchase decline concentrated by age, channel or sign-up status?", "U5, U4 and U8 used as segments", "RQ2.2, RQ2.3"],
        ]},
        {"heading": "Narrative (4 steps)", "header": ["Step", "Message", "Evidence (figures)", "Source"], "rows": [
            ["1. The problem today",
             "Group sales have been flat since Q3 2022 and the store network is shrinking.",
             "Quarterly sales growth in local currencies was -4% in Q3 2022 and has stayed between -4% and +3% since. FY2025 +2%; the first nine months of 2026 in line with the previous year. "
             "Stores 5,076 (2019-11) → 4,023 (2026-08), -21%.",
             "H&M quarterly and full-year reports (charts 1-2)"],
            ["2. An earlier weakness",
             "While the group was still growing, new customers were already returning less, and buying fewer items per visit.",
             "The group grew +4% to +8% every quarter from 2018-12 to 2020-02. Over the same period the Kaggle 90-day repurchase rate of new customers fell from 43.4% (first purchase 2019-03) to 29.8% (2020-02). "
             "Cohorts from 2019-09 on, which are least likely to include returning customers, still fall from 35.8% to 29.8%. {rep365} Items per purchase occasion -6.5% in 2019-10 to 2020-02.",
             "C2_U2, C2_U1 (chart 3)"],
            ["3. Loyalty expansion at the same time",
             "H&M grew its loyalty programme fast in this period. Sign-ups rose while new customers' conversion to a second purchase fell.",
             "Loyalty members 35 million (FY2019 Q1) → 65 million (FY2019) → 107 million (FY2020) → 130 million (FY2021 Q2) → more than 200 million (FY2024 Q1). "
             "92.7% of registered Kaggle customers are ACTIVE members. 90-day repurchase of new customers who did not complete sign-up (PRE-CREATE) 19.8% vs ACTIVE 37.6%. "
             "Sign-up status is the value at the end of the data (a snapshot), so customers who never came back may simply have stayed unregistered. Read it as a related measure, not a cause.",
             "Reports (chart 4), C1_09, C2_U8"],
            ["4. Limits of the reading",
             "Kaggle is a sample, not the whole group. So we say 'the sample's customers bought less', not 'group sales fell'.",
             "In the same quarters group sales grew (2019-09 to 11 +5%, 2019-12 to 2020-02 +5%) while Kaggle value fell (2019-10 to 11 -5.9%, 2019-12 to 2020-02 -8.8%).",
             "Reports FY2019 Q4 and FY2020 Q1, C1_01"],
        ]},
        {"heading": "Evidence charts: the group (H&M reports)", "charts": [
            {"table": "rp.sales", "type": "column", "overlap": True,
             "cols": ["Group sales growth (local currencies, %)", "Kaggle data period"],
             "title": {"en": "Chart 1. Group quarterly sales growth: around 0% since Q3 2022"}},
            {"table": "rp.stores", "type": "line", "cols": ["Stores (period end)"],
             "title": {"en": "Chart 2. Stores: 5,076 (2019-11) → 4,023 (2026-08)"}},
        ]},
        {"heading": "Evidence charts: customers (Kaggle) and members (reports)", "charts": [
            {"table": "c2.rep_by_month", "type": "line", "cols": ["repurchase_90d_pct", "repurchase_365d_pct"], "only": (0, 16),
             "title": {"en": "Chart 3. New-customer 90- and 365-day repurchase (%) by first-purchase month"}},
            {"table": "rp.members", "type": "column", "cols": ["Loyalty members (million)"],
             "title": {"en": "Chart 4. Loyalty members (million), quarters where the reports give a number"}},
        ]},
        {"heading": "Answers to the Phase 2 research questions (RQ1.1 to RQ2.4)", "header": ["RQ", "Phase 2 question (short)", "Our answer", "Sheet · status"], "rows": [
            ["RQ1.1", "30-, 90- and 365-day repurchase of new customers, and differences by first-purchase month",
             "90 days 43.4% (2019-03) → 29.8% (2020-02); 30 days 24.3% → 17.9%. {rep365} The decline across first-purchase months is larger than the seasonal differences. "
             "However, the 2020-03 to 06 cohorts (the COVID period) rise again to 32.4% to 36.3%, so the decline stops at 2020-02. "
             "20.2% of repeat buyers return within 7 days, 41.0% within 30, 66.7% within 90.",
             "C2_U2 · answered. Confirm with survival curves (Phase 3 method)"],
            ["RQ1.2", "Which first-purchase features (channel, line, items, price, age, newsletter) go with returning",
             "90-day repurchase by main line of the first basket ranges only from 33.3% (Sport) to 38.1% (Baby/Children). First-basket size matters more (1 item 32.4% vs 7+ items 40.7%). "
             "Newsletter (Regularly 42.9% vs NONE 33.6%) and sign-up status (PRE-CREATE 19.8% vs ACTIVE 37.6%) are end-of-data values, so they cannot be used as first-purchase features.",
             "C2_U2, C2_U8 · partly. Leave the snapshot variables out of the regression or flag them"],
            ["RQ1.3", "Sales share of repeat vs one-time customers, and concentration among top buyers",
             "The 32.9% of customers who bought on one day only bring 4.8% of value. The 7.8% who bought on 20+ occasions bring 38.5%. Repeat customers make the sales.",
             "C1_05 · answered"],
            ["RQ1.4", "How the FY2018 to FY2025 reports describe loyalty and membership (qualitative)",
             "Member counts only, as a series: 35 million (FY2019 Q1) → 107 million (FY2020) → more than 200 million (FY2024 Q1). Thematic coding of the strategy text not done yet.",
             "Chart 4, hm_report_quarterly.csv · not done"],
            ["RQ2.1", "Online share before, during and after the 2020 closures, and whether it stayed higher",
             "Online 85.4% in 2020-03 to 05 (70.1% a year earlier), 100% in April. After reopening, 2020-06 to 08 was 64.7%, below the year before (68.8%), so it did not stay higher.",
             "C1_01 · answered"],
            ["RQ2.2", "Did store-reliant customers keep buying after the closures, compared with online-reliant ones",
             "{reopen} Of store-only customers before the closures, 19.8% bought online during them.",
             "C2_U4 · answered (baseline comparison)"],
            ["RQ2.3", "Which product lines and age groups rely most on stores",
             "Store share of transactions is lowest for 25-34 (25.2%) and highest for 65+ (36.6%). 65+ pay 18.8% more per item than 16-24 but spend the least per customer (0.41 vs 0.83 for 25-34).",
             "C1_08 · answered for age. This workbook has no table of online share by line (the Phase 2 figures such as Menswear 55.0% were computed separately)"],
            ["RQ2.4", "Reported store counts and online share vs the transaction data (secondary data)",
             "In the same quarters group sales grew while Kaggle value fell (2019-09 to 11: group +5% vs Kaggle Oct-Nov -5.9%; 2019-12 to 2020-02: +5% vs -8.8%). Online share is about 70% in Kaggle vs 26-30% officially. The sample does not represent the whole group.",
             "Narrative step 4, charts 1-2 · answered"],
        ]},
        {"heading": "Check of the Phase 1 to 3 document (current Google Doc)", "header": ["Document wording (where)", "Full-data result", "Fix", "Verdict"], "order": [3, 0, 1, 2], "rows": [
            ["23.5% of customers observable for a year never bought again (Phase 2-3 Issue 1)",
             "23.5% on the same definition. Among all purchasing customers, 32.9% bought on one day only.", "Keep", "Match"],
            ["Online 70.1% → 85.4% in the closures, 64.7% after reopening vs 68.8% a year earlier (Phase 2 Issue 2)",
             "Same values.", "Keep", "Match"],
            ["H&M brand 3,579 stores vs group 4,801 → 4,101 stores (Phase 1)",
             "Both are report figures but on different bases (brand vs group).", "Use the group basis throughout", "Tidy"],
            ["Sales growth 12% → 6% → -1% → 1% → 2%, first nine months of 2026 (Phase 1)",
             "Match the reports.", "Keep", "Match"],
            ["First purchase date = earliest purchase in the data (Phase 3 variables)",
             "Customers who shopped before 2018-09 are counted as new (left censoring). The workbook counts only first purchases from 2019-03-01 as new.", "Add a six-month buffer to the new-customer definition", "Fix"],
            ["RQ1.2 includes newsletter subscription as a first-purchase feature (Phase 2-3)",
             "Newsletter and sign-up status in customers.csv are end-of-data values, not values at the first purchase.", "Report them separately as related measures; leave them out of the regression", "Fix"],
            ["Alternative data 'None' for RQ1.2, 1.3 and 2.2 (Phase 3 table)",
             "The rubric asks for viable alternatives.", "E.g. Google mobility reports and the quarterly reports' reopening notes for RQ2.2", "Add"],
        ]},
        {"heading": "Solution directions (hypotheses)", "header": ["Direction", "Evidence", "Measure"], "rows": [
            ["First-30-day onboarding", "Personalised recommendations within 7 days of the first purchase, a second-purchase offer. 41% of repeat buyers return within 30 days, 20% within 7.", "New-customer 90-day repurchase rate"],
            ["Complete sign-up", "Prompt full sign-up and newsletter opt-in at first purchase. PRE-CREATE 19.8% vs ACTIVE 37.6%; newsletter Regularly 42.9% vs NONE 33.6% (end-of-data values, so the direction of cause is unknown).", "Sign-up completion rate; that group's 90-day repurchase"],
            ["Bigger first basket", "Outfit and bundle recommendations. First basket of 1 item 32.4% vs 7+ items 40.7%.", "Items in the first purchase"],
            ["How to test", "All these gaps are correlations: customers who already buy more may be the ones who sign up or subscribe. Confirm effects with A/B tests.", "Test vs control repurchase rate"],
        ]},
        {"heading": "Next analyses and limits", "header": ["Item", "Description", "Reference"], "rows": [
            ["Next analyses", "Survival analysis to confirm the decline and the drop-off point (RQ1.1), first purchase by product_group and a regression without snapshot variables (RQ1.2), repurchase of customers whose first purchase was discounted, thematic coding of the reports (RQ1.4), cohort cumulative value in money terms.", "Excel handbook 5-8, 5-3, 5-7"],
            ["Limit: sample", "Kaggle is a sample with no market column, and price is transformed. It is not the same measure as group sales.", "Z_Limitations"],
            ["Limit: causality", "Nothing proves that the 2019-2020 change in sample customers' behaviour caused the group's stagnation from 2022. It is a hypothesis: a weakness that came earlier.", ""],
            ["Limit: reports", "The reports do not publish repurchase rates. After 2020 they give member counts only in FY2021 Q2 and FY2024 Q1.", "hm_report_quarterly.csv"],
        ]},
    ],
}


def fill_main(tables, rep365, reopen):
    """Put run-time figures into MAIN's "{rep365}" and "{reopen}" slots."""
    r = tables["c2.rep_by_month"].dropna(subset=["repurchase_365d_pct"])
    a, b = r.iloc[0], r.iloc[-1]
    cs = tables["c2.covid_store"].set_index("group")
    slots = {
        "{rep365}": rep365.format(a=a["segment"], va=a["repurchase_365d_pct"], b=b["segment"], vb=b["repurchase_365d_pct"]),
        "{reopen}": reopen.format(**{f"{k}{y}": cs.loc[g, col] for k, g in [("s", "store only before"), ("o", "online only before"), ("m", "omni before")]
                                     for y, col in [("20", "bought_after_reopen_pct"), ("19", "same_months_2019_pct")]}),
    }
    for sec in MAIN["sections"]:
        for row in sec.get("rows", []):
            for j, cell in enumerate(row):
                for k, v in slots.items():
                    cell = cell.replace(k, v)
                row[j] = cell
