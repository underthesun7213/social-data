"""Data lineage for every table in the H&M EDA results workbook.

One entry per table key (the keys hm_eda_text*.SHEETS use): which of the three
Kaggle CSVs it reads, which columns, how they are joined, filtered and grouped,
and what is computed. Sheet and table names come from the language module, so
only the filter and calculation text is written in both languages here.

Keep this in step with hm_eda_cycle1.py / hm_eda_cycle2.py.
"""

TX, CU, AR = "transactions_train.csv", "customers.csv", "articles.csv"
RP = "hm_report_quarterly.csv (H&M 보고서 / reports)"
OCC = "(customer_id, t_dat)"  # one purchase occasion


def t(ko, en):
    return {"ko": ko, "en": en}


ALL = t("전체 기간", "Whole period")
NEW = t("첫 구매일(t_dat 최소) ≥ 2019-03-01", "First purchase date (min t_dat) ≥ 2019-03-01")
Y12 = t("Y1 = 2018-09-20 ~ 2019-09-19, Y2 = 2019-09-20 ~ 2020-09-22",
        "Y1 = 2018-09-20 to 2019-09-19, Y2 = 2019-09-20 to 2020-09-22")
REP = t("첫 구매 후 다음 구매 기회까지 일수 ≤ 30 / 90 / 365 인 고객 비율. 그 기간을 관찰할 수 있는 고객만(첫 구매 + 30/90/365일 ≤ 2020-09-22)",
        "Share of customers whose next occasion is within 30 / 90 / 365 days of the first. Only customers observable for that long (first purchase + 30/90/365 days ≤ 2020-09-22)")

# key: csvs, columns, join, group by, filter, calculation
LINEAGE = {
    # ------------------------------------------------------------ cycle 1
    "c1.monthly": (TX, "t_dat, customer_id, price, sales_channel_id", "-", "month(t_dat)", ALL,
                   t("rows = COUNT(*), value = SUM(price), customers = COUNT(DISTINCT customer_id), avg_price = AVG(price), "
                     "online_row_share = AVG(sales_channel_id = 2), YoY = 같은 달 12개월 전 대비",
                     "rows = COUNT(*), value = SUM(price), customers = COUNT(DISTINCT customer_id), avg_price = AVG(price), "
                     "online_row_share = AVG(sales_channel_id = 2), YoY = vs the same month 12 months earlier")),
    "c1.weekday": (TX, "t_dat, sales_channel_id", "-", "t_dat → weekday(t_dat)", ALL,
                   t("날짜별 COUNT(*)·온라인 비중을 먼저 구하고 요일별 평균", "Daily COUNT(*) and online share first, then averaged by weekday")),
    "c1.new_vs_returning": (TX, "t_dat, customer_id", "-", "month(t_dat)", ALL,
                            t("고객별 MIN(t_dat) = 첫 구매일. 월별 COUNT(DISTINCT customer_id), 그중 첫 구매일이 그 달인 고객 수",
                              "MIN(t_dat) per customer = first purchase. Per month COUNT(DISTINCT customer_id) and those whose first purchase is that month")),
    "c1.cohort": (TX, "t_dat, customer_id", "-", t("cohort = month(MIN(t_dat)), k = 경과 월", "cohort = month(MIN(t_dat)), k = months since"), ALL,
                  t("코호트 크기 대비 k개월 뒤 구매 고객 수(DISTINCT) 비율, k = 1~12",
                    "Distinct customers buying in month k / cohort size, k = 1-12")),
    "c1.frequency": (TX, "customer_id, t_dat, price", "-", t(f"{OCC} → customer_id → 구간", f"{OCC} → customer_id → band"), ALL,
                     t("고객별 구매 기회 수 = COUNT(DISTINCT t_dat), value = SUM(price). 구간별 고객 수·value 비중",
                       "Occasions per customer = COUNT(DISTINCT t_dat), value = SUM(price). Customers and value share per band")),
    "c1.channel_mix": (TX, "customer_id, t_dat, price, sales_channel_id", "-", "customer_id → channel_type", ALL,
                       t("고객이 2년간 channel 2만 / 1만 / 둘 다 썼는지로 유형. 유형별 고객 수, 평균 구매 기회, 평균·합계 value",
                         "Type by whether the customer used only channel 2 / only 1 / both over 2 years. Customers, average occasions, average and total value per type")),
    "c1.basket_channel": (TX, "customer_id, t_dat, price, sales_channel_id", "-", t(f"{OCC} → 그날 채널", f"{OCC} → channel that day"), ALL,
                          t("구매 기회별 COUNT(*) = 상품 수, SUM(price). 그날 쓴 채널(온라인/매장/둘 다)별 평균·중앙값",
                            "Per occasion COUNT(*) = items, SUM(price). Mean and median by channel used that day (online / store / both)")),
    "c1.age_profile": (f"{TX} + {CU}", "tx: customer_id, price, sales_channel_id / cu: age", "customer_id", "customer_id → age band",
                       t("age 결측 고객 제외", "Customers without age excluded"),
                       t("고객별 행 수·value·온라인 비중을 구한 뒤 연령대(16-24, 25-34 …)별 평균. 옴니 비율은 c1.channel_mix 유형 사용",
                         "Rows, value and online share per customer, then averaged by age band (16-24, 25-34 …). Omni share uses the c1.channel_mix type")),
    "c1.member_profile": (f"{TX} + {CU}", "tx: customer_id, price, sales_channel_id / cu: club_member_status, fashion_news_frequency",
                          "customer_id", "customer_id → field value", t("결측은 '(missing)'으로 묶음", "Missing values grouped as '(missing)'"),
                          t("고객당 행 수·value·온라인 비중의 값별 평균", "Average rows, value and online share per customer by field value")),
    "c1.line_trend": (f"{TX} + {AR}", "tx: t_dat, article_id, price / ar: index_group_name", "article_id", "month(t_dat), index_group_name", ALL,
                      t("월별 라인 SUM(price) / 월 SUM(price)", "Line SUM(price) / month SUM(price)")),
    "c1.seasonality": (f"{TX} + {AR}", "tx: t_dat, article_id / ar: product_group_name", "article_id", "product_group_name, calendar month",
                       t("2018-10-01 ~ 2019-09-30 (각 달 1번), 행 10만 이상 상품군", "2018-10-01 to 2019-09-30 (each month once), product groups with 100k+ rows"),
                       t("상품군의 연간 COUNT(*) 중 달별 비중. peak_to_trough = 최대 달 / 최소 달",
                         "Each month's share of the group's yearly COUNT(*). peak_to_trough = busiest / quietest month")),
    "c1.price_drop": (TX, "article_id, price", "-", t("article_id → 구간", "article_id → band"), t("행 50개 이상 상품", "Articles with 50+ rows"),
                      t("상품별 1 - PERCENTILE(price, 5%) / PERCENTILE(price, 95%), 구간별 상품 수",
                        "Per article 1 - PERCENTILE(price, 5%) / PERCENTILE(price, 95%); articles per band")),
    "c1.launches": (TX, "article_id, t_dat", "-", "month(MIN(t_dat) per article)",
                    t("첫 판매일이 데이터 시작 + 30일 이후인 상품", "Articles first sold more than 30 days after the data starts"),
                    t("첫 판매 월별 상품 수, 평균 판매 행, 첫~마지막 판매일 수 중앙값", "Articles per first-sale month, average rows, median days from first to last sale")),
    "c1.concentration": (TX, "article_id", "-", "article_id", ALL,
                         t("상품별 COUNT(*) 내림차순 누적합 / 전체 행", "Cumulative COUNT(*) per article, descending, / all rows")),
    # ------------------------------------------------------------ cycle 2
    "c2.decomp": (TX, "customer_id, t_dat, price", "-", f"{OCC} → month",
                  t("2019-10 ~ 2020-08 각 월과 12개월 전. 합계 행: 2019-10 ~ 2020-02, 2020-03 ~ 08",
                    "2019-10 to 2020-08, each month vs 12 months earlier. Total rows: 2019-10 to 2020-02, 2020-03 to 08"),
                  t("value = 고객 수 x (구매 기회 / 고객) x (상품 수 / 구매 기회) x (value / 상품 수). 각 요인의 전년 대비 %",
                    "value = customers x (occasions / customer) x (items / occasion) x (value / item). % vs a year earlier for each factor")),
    "c2.rep_by_month": (TX, "customer_id, t_dat", "-", "month(first purchase)", NEW, REP),
    "c2.rep_gap": (TX, "customer_id, t_dat", "-", t("첫→둘째 구매 일수 구간", "days first → second, banded"), NEW,
                   t("두 번째 구매 기회가 있는 고객만. 구간별 비중·누적 비중", "Customers with a second occasion only. Share and cumulative share per band")),
    "c2.rep_by_channel": (TX, "customer_id, t_dat, sales_channel_id", "-", t("첫 구매일 채널", "channel on first purchase day"), NEW, REP),
    "c2.rep_by_basket": (TX, "customer_id, t_dat", "-", t("첫 구매일 COUNT(*) 구간", "items on first day, banded"), NEW, REP),
    "c2.rep_by_line": (f"{TX} + {AR}", "tx: customer_id, t_dat, article_id / ar: index_group_name", "article_id",
                       t("첫 구매일 상품 수가 가장 많은 index_group_name", "index_group_name with most items on first day"), NEW, REP),
    "c2.rep_by_age": (f"{TX} + {CU}", "tx: customer_id, t_dat / cu: age", "customer_id", "age band", NEW, REP),
    "c2.rep_by_club": (f"{TX} + {CU}", "tx: customer_id, t_dat / cu: club_member_status", "customer_id", "club_member_status", NEW, REP),
    "c2.rep_by_news": (f"{TX} + {CU}", "tx: customer_id, t_dat / cu: fashion_news_frequency", "customer_id", "fashion_news_frequency", NEW, REP),
    "c2.new_mix": (f"{TX} + {CU}", "tx: customer_id, t_dat, sales_channel_id / cu: age", "customer_id", "month(first purchase)", NEW,
                   t("첫 구매 월별 신규 고객 수, 연령대 비중, 첫 구매일 채널 비중", "New customers per first-purchase month, age band shares, first-day channel shares")),
    "c2.migration": (TX, "customer_id, t_dat, price, sales_channel_id", "-", "Y1 type x Y2 type", Y12,
                     t("해마다 고객 유형(옴니 / 온라인만 / 매장만), Y2에 없으면 'no purchase'. Y1 고객 기준 Y2 유형 비중, 유형별 value 합계 변화",
                       "Customer type per year (omni / online only / store only); 'no purchase' if absent in Y2. Y2 type shares among Y1 customers, change in total value per type")),
    "c2.migration_value": (TX, "customer_id, t_dat, price, sales_channel_id", "-", "Y1 type → Y2 type", Y12,
                           t("두 해 모두 산 고객만. 경로별 고객 수, 고객당 평균 value Y1·Y2, 변화율",
                             "Customers buying in both years only. Customers, mean value per customer in Y1 and Y2, change per path")),
    "c2.covid_store": (TX, "customer_id, t_dat, sales_channel_id", "-", t("휴업 전 유형", "pre-closure type"),
                       t("휴업 전 2019-09-20 ~ 2020-02-29, 휴업기 2020-03-15 ~ 05-31, 재개장 후 2020-06-01 ~",
                         "Before 2019-09-20 to 2020-02-29, closures 2020-03-15 to 05-31, after reopening 2020-06-01 on"),
                       t("휴업 전 유형별로 휴업기 구매 비율, 휴업기 온라인 구매 비율, 재개장 후 구매 비율, 재개장 후 온라인 구매 기회 비중",
                         "Per pre-closure type: share buying in closures, share buying online in closures, share buying after reopening, online share of occasions after reopening")),
    "c2.age_years": (f"{TX} + {CU}", "tx: customer_id, t_dat, price / cu: age", "customer_id", "year, age band", Y12,
                     t("해마다 연령대별 COUNT(DISTINCT customer_id)와 SUM(price) 비중, 증감", "Per year COUNT(DISTINCT customer_id) and SUM(price) share by age band, and change")),
    "c2.age_mix": (f"{TX} + {CU} + {AR}", "tx: customer_id, article_id, price / cu: age / ar: index_group_name",
                   "customer_id, article_id", "age band, index_group_name", ALL,
                   t("연령대별 SUM(price) 중 라인 비중", "Line share of each age band's SUM(price)")),
    "c2.heavy": (TX, "customer_id, t_dat, price", "-", "Y1 value decile", Y12,
                 t("Y1 고객을 SUM(price) 순으로 10등분. 십분위별 Y1 value 비중, Y2 구매 비율, value 변화",
                   "Y1 customers split into ten groups by SUM(price). Share of Y1 value, share buying in Y2 and value change per decile")),
    "c2.y_split": (TX, "customer_id, t_dat, price", "-", t("Y2 고객이 Y1에도 샀는지", "whether the Y2 customer bought in Y1"), Y12,
                   t("Y2 SUM(price)를 기존(Y1에도 구매) 고객분과 신규 고객분으로 나눠 Y1 합계 대비 %",
                     "Y2 SUM(price) split into existing (also bought in Y1) and new customers, as % of Y1 total")),
    "c2.line_supply": (f"{TX} + {AR}", "tx: t_dat, article_id / ar: index_group_name", "article_id", "month(t_dat), index_group_name", ALL,
                       t("active_articles = COUNT(DISTINCT article_id), rows_per_article = COUNT(*) / active_articles",
                         "active_articles = COUNT(DISTINCT article_id), rows_per_article = COUNT(*) / active_articles")),
    "c2.member_age": (f"{TX} + {CU}", "tx: customer_id / cu: age, fashion_news_frequency, club_member_status", "customer_id",
                      "age band x field value",
                      t("age 있는 고객, 뉴스레터 NONE·Regularly, 멤버십 ACTIVE·PRE-CREATE만", "Customers with age; newsletter NONE / Regularly and membership ACTIVE / PRE-CREATE only"),
                      t("고객당 COUNT(*) 평균", "Average COUNT(*) per customer")),
    "c2.md_month": (TX, "article_id, t_dat, price", "-", "month(t_dat)",
                    t("첫 판매일 ≥ 2018-10-20 상품", "Articles first sold on or after 2018-10-20"),
                    t("출시가 = 첫 판매 후 28일 내 price 중앙값. 비율 = price / 출시가. 비율 < 0.7 인 행 비중, 비율 중앙값",
                      "Launch price = median price in the first 28 days. Ratio = price / launch price. Share of rows with ratio < 0.7, median ratio")),
    "c2.md_age": (TX, "article_id, t_dat, price", "-", t("출시 후 4주 구간", "4-week bucket since launch"),
                  t("첫 판매일 ≥ 2018-10-20 상품", "Articles first sold on or after 2018-10-20"),
                  t("c2.md_month와 같은 비율을 출시 후 경과 주 구간별로", "Same ratio as c2.md_month, by weeks since launch")),
    # ------------------------------------------------------------ H&M reports (main-question sheet)
    "rp.sales": (RP, "fiscal_quarter, sales_lc_pct", "-", "fiscal quarter", t("FY2018 1분기 ~ FY2026 3분기", "FY2018 Q1 to FY2026 Q3"),
                 t("보고서 문장(일부는 표)의 분기 매출 증감, 현지 통화. Kaggle 기간(FY2018 4분기 ~ FY2020 4분기)은 별도 계열로 겹쳐 표시",
                   "Quarterly sales growth in local currencies from report sentences (some from tables). Kaggle-period quarters (FY2018 Q4 to FY2020 Q4) overlaid as a second series")),
    "rp.stores": (RP, "fiscal_quarter, stores_end", "-", "fiscal quarter", t("FY2018 1분기 ~ FY2026 3분기", "FY2018 Q1 to FY2026 Q3"),
                  t("분기말 그룹 매장 수", "Group store count at quarter end")),
    "rp.members": (RP, "fiscal_quarter, loyalty_members_million", "-", "fiscal quarter", t("회원 수가 적힌 분기만", "Quarters with a stated member count only"),
                   t("보고서의 로열티 회원 수(백만 명). '이상'·'약' 표현은 적힌 숫자 그대로", "Loyalty members (million) as stated; 'over' / 'around' wording kept as the stated number")),
}


def rows(T):
    """One row per table in sheet order: sheet, table, CSV, columns, join, group by, filter, calculation."""
    out = []
    for spec in T.SHEETS:
        for sub, key in spec["tables"]:
            csvs, cols, join, group, flt, calc = LINEAGE[key]
            group = group[T.LANG] if isinstance(group, dict) else group
            out.append([spec["sheet"], sub, csvs, cols, join, group, flt[T.LANG], calc[T.LANG]])
    # Charts on the main-question sheet, each with its source table.
    for sec in T.MAIN["sections"]:
        for c in sec.get("charts", []):
            csvs, cols, join, group, flt, calc = LINEAGE[c["table"]]
            group = group[T.LANG] if isinstance(group, dict) else group
            out.append([T.MAIN["sheet"], c["title"][T.LANG], csvs, cols, join, group, flt[T.LANG], calc[T.LANG]])
    return out
