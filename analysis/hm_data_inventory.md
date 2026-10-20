# H&M data inventory (data/hm/)

All files live under `data/hm/`, which is gitignored. Re-create them with
`analysis/hm_phase1.py` (Kaggle CSVs) and `analysis/download_hm_reports.py` (PDFs).

## 1. Kaggle transaction data

Competition: `h-and-m-personalized-fashion-recommendations`. Images were not downloaded.

| File | Rows | Columns | Content |
|---|---|---|---|
| transactions_train.csv (~3.5 GB) | 31,788,324 | 5 | One row per item bought. 2018-09-20 to 2020-09-22 |
| customers.csv (~200 MB) | 1,371,980 | 7 | One row per registered customer |
| articles.csv (~35 MB) | 105,542 | 25 | One row per product |

**transactions_train.csv**: `t_dat` (date), `customer_id`, `article_id`, `price` (transformed, not a real currency), `sales_channel_id` (1/2, no official definition; 2 assumed online).

**customers.csv**: `customer_id`, `FN`, `Active`, `club_member_status`, `fashion_news_frequency`, `age` (~1% missing), `postal_code` (hashed).

**articles.csv**: `article_id` plus product, type, group, graphical appearance, colour, perceived colour, department, index (e.g. Ladieswear, Divided, Menswear), section and garment group, each as a code and a name, and a free-text `detail_desc`.

There is no store, country or customer gender column.

## 2. H&M Group investor reports (31 PDFs, ~97 MB)

Source: https://hmgroup.com/investors/reports/. H&M's fiscal year runs **1 December to 30 November**,
so "2019" means 1 Dec 2018 to 30 Nov 2019.

### Full-year reports (`reports/full-year/`), Q4 interim report with full-year figures

| File | Fiscal year covered | Pages |
|---|---|---|
| 2018.pdf | 1 Dec 2017 to 30 Nov 2018 | 25 |
| 2019.pdf | 1 Dec 2018 to 30 Nov 2019 | 27 |
| 2020.pdf | 1 Dec 2019 to 30 Nov 2020 | 27 |
| 2021.pdf | 1 Dec 2020 to 30 Nov 2021 | 26 |
| 2022.pdf | 1 Dec 2021 to 30 Nov 2022 | 27 |
| 2023.pdf | 1 Dec 2022 to 30 Nov 2023 | 28 |
| 2024.pdf | FY2024 | 36 |
| 2025.pdf | FY2025 | 38 |

### Interim reports (`reports/quarterly/`), cumulative from 1 December

| File | Period | Pages |
|---|---|---|
| 2018-3m / 6m / 9m | 1 Dec 2017 to 28 Feb / 31 May / 31 Aug 2018 | 17 / 19 / 19 |
| 2019-3m / 6m / 9m | 1 Dec 2018 to 28 Feb / 31 May / 31 Aug 2019 | 19 / 21 / 21 |
| 2020-3m / 6m / 9m | 1 Dec 2019 to 29 Feb / 31 May / 31 Aug 2020 | 20 / 25 / 22 |
| 2025-3m / 6m / 9m | FY2025 Q1 / Q2 / Q3 | 30 / 34 / 32 |
| 2026-3m / 6m / 9m | FY2026 Q1 / Q2 / Q3 | 28 / 32 / 30 |

Not downloaded: 2021 to 2024 interim reports. The FY2026 full-year report is not published yet.

### Annual (and sustainability) reports (`reports/annual/`)

| File | Title on cover | Pages |
|---|---|---|
| 2018.pdf | Annual report 2018 | 80 |
| 2019.pdf | Annual report 2019 | 88 |
| 2020.pdf | Annual report 2020 | 92 |
| 2021.pdf | Annual and Sustainability Report 2021 | 118 |
| 2022.pdf | H&M Group Annual and Sustainability Report 2022 | 152 |
| 2023.pdf | H&M Group Annual and Sustainability Report 2023 | 75 |
| 2024.pdf | H&M Group Annual & Sustainability Report 2024 | 87 |
| 2025.pdf | H&M Group Annual & Sustainability Report 2025 | 99 |

## 3. How the Kaggle period lines up with H&M's fiscal years

| Kaggle months | H&M fiscal period | Matching report |
|---|---|---|
| 2018-09-20 to 2018-11-30 | FY2018 Q4 (partial) | full-year/2018 |
| 2018-12 to 2019-11 | FY2019, complete | full-year/2019, quarterly/2019-*, annual/2019 |
| 2019-12 to 2020-08 | FY2020 Q1 to Q3 (includes COVID store closures, Mar to May 2020) | quarterly/2020-* |
| 2020-09-01 to 2020-09-22 | FY2020 Q4 (partial) | full-year/2020, annual/2020 |
