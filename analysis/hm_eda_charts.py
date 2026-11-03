"""Chart definitions for the H&M EDA results workbook, shared by both languages.

Keyed by the first 5 characters of the sheet name (e.g. "C1_01"). Each chart:
  table   index of the table on that sheet (default 0)
  type    xlsxwriter chart type; subtype optional
  cols    value columns, one series each (or, with rows=, the column range)
  rows    plot these rows (matched on the first column) as series across cols
  only    (start, stop) slice of table rows to plot
  cats    number of leading columns used as category labels (default 1)
  ymax    fixed value-axis maximum (e.g. 100 for shares)
  title   {"ko": ..., "en": ...}
Single y-axis only; two measures of different scale go in two charts.
"""

MONTHS = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"]


def t(ko, en):
    return {"ko": ko, "en": en}


CHARTS = {
    "C1_01": [
        {"type": "line", "cols": ["value"], "title": t("월별 value", "Monthly value")},
        {"type": "line", "cols": ["customers"], "title": t("월별 구매 고객 수", "Purchasing customers per month")},
        {"type": "line", "cols": ["online_row_share"], "ymax": 100, "title": t("온라인 행 비중(%)", "Online row share (%)")},
        {"type": "column", "cols": ["value_yoy_pct", "customers_yoy_pct"], "only": (13, 24),
         "title": t("전년 동월 대비 %: value, 고객 수 (2019-10 ~ 2020-08)", "% vs a year earlier: value, customers (2019-10 to 2020-08)")},
    ],
    "C1_02": [
        {"type": "column", "cols": ["avg_rows"], "title": t("요일별 하루 평균 행 수", "Average rows per day")},
        {"type": "column", "cols": ["online_row_share"], "ymax": 100, "title": t("요일별 온라인 행 비중(%)", "Online row share by weekday (%)")},
    ],
    "C1_03": [
        {"type": "column", "cols": ["new_customers"], "only": (6, 25),
         "title": t("월별 신규 고객 수 (2019-03~)", "New customers per month (from 2019-03)")},
        {"type": "line", "cols": ["new_share_pct"], "only": (6, 25),
         "title": t("활성 고객 중 신규 비중(%)", "New share of active customers (%)")},
    ],
    "C1_04": [
        {"type": "line", "cols": ["M+1", "M+3", "M+6"], "only": (6, 24),
         "title": t("코호트별 M+1·M+3·M+6 재구매율(%)", "Repurchase in M+1, M+3, M+6 by cohort (%)")},
        {"type": "column", "cols": ["cohort_size"], "only": (6, 25),
         "title": t("코호트 크기(첫 구매 고객 수)", "Cohort size (first-time buyers)")},
    ],
    "C1_05": [
        {"type": "column", "cols": ["customer_share_pct", "value_share_pct"],
         "title": t("구매 기회 수별 고객 비중 vs value 비중(%)", "Customer share vs value share by occasions (%)")},
    ],
    "C1_06": [
        {"type": "column", "cols": ["customer_share_pct", "value_share_pct"],
         "title": t("채널 유형별 고객 비중 vs value 비중(%)", "Customer share vs value share by channel type (%)")},
        {"type": "column", "cols": ["avg_value"], "title": t("고객당 value", "Value per customer")},
    ],
    "C1_07": [
        {"type": "column", "cols": ["avg_items"], "title": t("구매 기회당 평균 상품 수", "Average items per occasion")},
    ],
    "C1_08": [
        {"type": "column", "cols": ["rows_per_customer"], "title": t("연령대별 고객당 행 수(2년)", "Rows per customer by age band (2 years)")},
        {"type": "column", "cols": ["omni_share_pct", "online_row_share_pct"],
         "title": t("옴니 고객 비율 vs 온라인 행 비중(%)", "Omni customer share vs online row share (%)")},
    ],
    "C1_09": [
        {"type": "bar", "cols": ["rows_per_customer"],
         "title": t("멤버십·뉴스레터 값별 고객당 행 수", "Rows per customer by membership and newsletter")},
    ],
    "C1_10": [
        {"type": "line", "cols": ["Ladieswear", "Divided", "Menswear", "Sport", "Baby/Children"],
         "title": t("라인별 value 비중(%)", "Value share by line (%)")},
    ],
    "C1_11": [
        {"type": "line", "rows": ["Swimwear", "Garment Full body", "Socks & Tights", "Garment Upper body"], "cols": MONTHS,
         "title": t("상품군별 월 비중(%)", "Monthly share by product group (%)")},
        {"type": "bar", "cols": ["peak_to_trough"], "title": t("최대 월 / 최소 월", "Busiest month / quietest month")},
    ],
    "C1_12": [
        {"type": "column", "cols": ["share_pct"], "title": t("가격 폭 구간별 상품 비중(%)", "Share of articles by price range (%)")},
    ],
    "C1_13": [
        {"type": "column", "cols": ["new_articles"], "title": t("월별 신규 출시 상품 수", "New articles per month")},
    ],
    "C1_14": [
        {"type": "column", "cols": ["share_of_rows_pct"], "title": t("상위 x% 상품의 누적 행 비중(%)", "Cumulative row share of top x% articles (%)")},
    ],
    "C2_U1": [
        {"type": "line", "cols": ["value_yoy_pct", "customers_yoy_pct", "items_per_occ_yoy_pct"], "only": (0, 11),
         "title": t("월별 전년 대비 %: value, 고객 수, 기회당 상품 수", "% vs a year earlier: value, customers, items per occasion")},
        {"type": "column", "cols": ["value_yoy_pct", "customers_yoy_pct", "occ_per_customer_yoy_pct", "items_per_occ_yoy_pct", "price_per_item_yoy_pct"],
         "only": (11, 13), "title": t("기간 합계: 요인별 전년 대비 %", "Period totals: % vs a year earlier by factor")},
    ],
    "C2_U2": [
        {"table": 0, "type": "line", "cols": ["repurchase_30d_pct", "repurchase_90d_pct"],
         "title": t("첫 구매 월별 30일·90일 재구매율(%)", "30- and 90-day repurchase by first-purchase month (%)")},
        {"table": 1, "type": "column", "cols": ["share_pct"],
         "title": t("두 번째 구매까지 걸린 일수(재구매자 %)", "Days to second purchase (% of repeat buyers)")},
        {"table": 2, "type": "column", "cols": ["repurchase_90d_pct"], "title": t("첫 구매 채널별 90일 재구매율(%)", "90-day repurchase by first channel (%)")},
        {"table": 3, "type": "column", "cols": ["repurchase_90d_pct"], "title": t("첫 장바구니 상품 수별 90일 재구매율(%)", "90-day repurchase by first-basket items (%)")},
        {"table": 4, "type": "column", "cols": ["repurchase_90d_pct"], "title": t("첫 장바구니 라인별 90일 재구매율(%)", "90-day repurchase by first-basket line (%)")},
        {"table": 5, "type": "column", "cols": ["repurchase_90d_pct"], "title": t("연령대별 90일 재구매율(%)", "90-day repurchase by age band (%)")},
        {"table": 7, "type": "line", "cols": ["returned_pct"], "ymax": 100,
         "title": t("d일까지 재구매한 신규 고객 비율(%), Kaplan–Meier", "New customers returned by day d (%), Kaplan–Meier")},
        {"table": 7, "type": "column", "cols": ["next_30d_pct"],
         "title": t("d일까지 안 돌아온 고객이 다음 30일 안에 재구매할 확률(%)", "Chance of returning in the next 30 days if not back by day d (%)")},
        {"table": 8, "type": "bar", "cols": ["repurchase_90d_pct"],
         "title": t("첫 장바구니 상품군별 90일 재구매율(%)", "90-day repurchase by first-basket product group (%)")},
    ],
    "C2_U3": [
        {"type": "column", "cols": ["new_customers"], "title": t("월별 신규 고객 수", "New customers per month")},
        {"type": "line", "cols": ["16-24", "25-34", "35-44", "45-54"], "title": t("신규 고객 연령 구성(%)", "Age mix of new customers (%)")},
        {"type": "line", "cols": ["online_pct", "store_pct"], "ymax": 100, "title": t("신규 고객 첫 구매 채널(%)", "First-purchase channel of new customers (%)")},
    ],
    "C2_U4": [
        {"table": 0, "type": "bar", "subtype": "percent_stacked", "cols": ["omni", "online only", "store only", "no purchase"],
         "title": t("Y1 유형별 Y2 유형 구성(%)", "Y2 type mix by Y1 type (%)")},
        {"table": 1, "type": "bar", "cols": ["change_pct"],
         "title": t("Y1 → Y2 유형별 고객당 value 변화(%)", "Change in value per customer by Y1 → Y2 type (%)")},
        {"table": 2, "type": "column", "cols": ["bought_during_closure_pct", "bought_online_during_closure_pct", "bought_after_reopen_pct"],
         "title": t("휴업 전 유형별: 휴업기 구매, 휴업기 온라인 구매, 재개장 후 구매(%)",
                    "By pre-closure type: bought in closures, bought online in closures, bought after reopening (%)")},
        {"table": 2, "type": "column", "cols": ["bought_after_reopen_pct", "same_months_2019_pct"],
         "title": t("재개장 후(2020-06 ~ 09) 구매 vs 1년 전 같은 달 기준선(%)",
                    "Bought after reopening (2020-06 to 09) vs same months a year earlier (%)")},
    ],
    "C2_U5": [
        {"table": 0, "type": "column", "cols": ["value_share_pct_Y1", "value_share_pct_Y2"],
         "title": t("연령대별 value 비중 Y1 vs Y2(%)", "Value share by age band, Y1 vs Y2 (%)")},
        {"table": 0, "type": "column", "cols": ["customers_change_pct"],
         "title": t("연령대별 구매 고객 수 변화 Y1 → Y2(%)", "Change in purchasing customers, Y1 → Y2 (%)")},
        {"table": 1, "type": "bar", "subtype": "percent_stacked", "cols": ["Ladieswear", "Divided", "Menswear", "Sport", "Baby/Children"],
         "title": t("연령대별 라인 구성(value %)", "Line mix by age band (value %)")},
    ],
    "C2_U6": [
        {"table": 0, "type": "column", "cols": ["share_of_y1_value_pct"], "title": t("십분위별 Y1 value 비중(%)", "Share of Y1 value by decile (%)")},
        {"table": 0, "type": "column", "cols": ["active_in_y2_pct"], "title": t("십분위별 Y2에도 구매한 비율(%)", "Share also buying in Y2 by decile (%)")},
        {"table": 0, "type": "column", "cols": ["value_y2_vs_y1_pct"], "title": t("십분위별 지출 변화 Y1 → Y2(%)", "Spending change Y1 → Y2 by decile (%)")},
        {"table": 1, "type": "column", "cols": ["vs_y1_total_pct"], "title": t("Y1 value = 100 기준", "Indexed to Y1 value = 100")},
    ],
    "C2_U7": [
        {"type": "line", "cols": ["Ladieswear | active_articles", "Divided | active_articles", "Baby/Children | active_articles", "Menswear | active_articles"],
         "title": t("라인별 월 판매 상품 수", "Articles sold per month by line")},
        {"type": "line", "cols": ["Ladieswear | rows_per_article", "Divided | rows_per_article", "Baby/Children | rows_per_article", "Menswear | rows_per_article"],
         "title": t("라인별 상품당 판매 행", "Rows per article by line")},
    ],
    "C2_U8": [
        {"table": 0, "type": "column", "cols": ["fashion_news_frequency = NONE", "fashion_news_frequency = Regularly"],
         "title": t("연령대별 고객당 행 수: 뉴스레터 NONE vs Regularly", "Rows per customer by age: newsletter NONE vs Regularly")},
        {"table": 0, "type": "column", "cols": ["club_member_status = ACTIVE", "club_member_status = PRE-CREATE"],
         "title": t("연령대별 고객당 행 수: ACTIVE vs PRE-CREATE", "Rows per customer by age: ACTIVE vs PRE-CREATE")},
        {"table": 2, "type": "column", "cols": ["repurchase_90d_pct"], "title": t("뉴스레터별 신규 90일 재구매율(%)", "New-customer 90-day repurchase by newsletter (%)")},
    ],
    "C2_U9": [
        {"table": 0, "type": "column", "cols": ["rows_30pct_below_pct"], "only": (0, 24),
         "title": t("월별 출시가 대비 30% 이상 할인 행 비중(%)", "Share of rows 30%+ below launch price by month (%)")},
        {"table": 1, "type": "column", "cols": ["rows_30pct_below_pct"],
         "title": t("출시 후 경과 주별 30% 이상 할인 행 비중(%)", "Share of rows 30%+ below launch price by weeks since launch (%)")},
    ],
}
