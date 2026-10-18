"""Build the H&M data dictionary: one row per column of the three Kaggle CSVs.

Run from anywhere:
    python analysis/hm_data_dictionary.py

Output:
    analysis/hm_data_dictionary.csv   (UTF-8 with BOM, opens in Excel and Google Sheets)
    analysis/hm_data_dictionary.xlsx  (only if openpyxl is installed; one sheet per file)

Counts, missing shares and examples are computed from data/hm/; the
descriptions below are written by hand.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "hm"
OUT_CSV = ROOT / "analysis" / "hm_data_dictionary.csv"
OUT_XLSX = ROOT / "analysis" / "hm_data_dictionary.xlsx"

# (column, type, description EN, description KO, used in this analysis)
DESCRIPTIONS = {
    "transactions_train.csv": [
        ("t_dat", "date", "Purchase date, no time of day", "구매 날짜 (시간 없음)", "Monthly and daily trends, repeat-purchase gaps"),
        ("customer_id", "string (hash)", "Anonymised customer ID; links to customers.csv", "익명화된 고객 ID. customers.csv와 연결", "Repeat purchases, items per customer"),
        ("article_id", "string (10 digits)", "Article ID; links to articles.csv. Read as text to keep the leading 0", "상품 ID. articles.csv와 연결. 앞의 0을 살리려면 문자로 읽음", "Product-line shares"),
        ("price", "float", "Transformed price, not a real currency", "변환된 가격. 실제 통화 아님", "Shares of spend only"),
        ("sales_channel_id", "int (1, 2)", "Sales channel. No official definition; 2 assumed online, 1 stores", "판매 채널. 공식 정의 없음, 2 = 온라인·1 = 매장으로 가정", "Online share, COVID comparison"),
    ],
    "customers.csv": [
        ("customer_id", "string (hash)", "Anonymised customer ID", "익명화된 고객 ID", "Join key"),
        ("FN", "float (1 or blank)", "Fashion news flag; blank most likely means no", "패션 뉴스 수신 표시. 빈칸은 '아니오'로 보는 게 자연스러움", "Not used"),
        ("Active", "float (1 or blank)", "Active-customer flag; meaning not documented", "활성 고객 표시. 정확한 정의는 공개되지 않음", "Not used"),
        ("club_member_status", "category", "Club membership status; PRE-CREATE = sign-up not completed", "회원 상태. PRE-CREATE = 가입 미완료", "Not used (LEFT CLUB almost empty, no churn analysis)"),
        ("fashion_news_frequency", "category", "How often the customer gets the newsletter", "뉴스레터 수신 빈도", "Candidate engagement variable"),
        ("age", "int", "Age as entered at sign-up", "가입 때 입력한 나이", "Age bands"),
        ("postal_code", "string (hash)", "Hashed postal code; one value shared by 120,303 customers is a placeholder", "암호화된 우편번호. 고객 120,303명이 공유하는 값은 미입력 대체값", "Not used (city unknown)"),
    ],
    "articles.csv": [
        ("article_id", "string (10 digits)", "Article ID = product code (7 digits) + variant (3 digits, usually the colour)", "상품 ID = 상품 코드(7자리) + 변형(3자리, 보통 색상)", "Join key"),
        ("product_code", "string (7 digits)", "Style code shared by all colours of one product", "같은 상품의 모든 색상이 공유하는 코드", ""),
        ("prod_name", "string", "Product name", "상품명", ""),
        ("product_type_no", "int", "Product type code", "상품 유형 코드", ""),
        ("product_type_name", "category", "Product type (Vest top, Trousers, Dress, ...)", "상품 유형", ""),
        ("product_group_name", "category", "Broad product group (upper body, lower body, accessories, ...)", "큰 상품군 (상의, 하의, 액세서리 등)", ""),
        ("graphical_appearance_no", "int", "Pattern code", "무늬 코드", ""),
        ("graphical_appearance_name", "category", "Pattern (Solid, All over pattern, ...)", "무늬", ""),
        ("colour_group_code", "string", "Colour code", "색상 코드", ""),
        ("colour_group_name", "category", "Colour", "색상", ""),
        ("perceived_colour_value_id", "int", "Lightness code", "명도 코드", ""),
        ("perceived_colour_value_name", "category", "Lightness of the colour (Dark, Light, ...)", "색의 밝기", ""),
        ("perceived_colour_master_id", "int", "Main colour family code", "대표 색 계열 코드", ""),
        ("perceived_colour_master_name", "category", "Main colour family", "대표 색 계열", ""),
        ("department_no", "int", "Department code", "부서 코드", ""),
        ("department_name", "category", "Buying department", "상품 기획 부서", ""),
        ("index_code", "string", "Product line code", "상품 라인 코드", ""),
        ("index_name", "category", "Product line (Ladieswear, Divided, Menswear, ...)", "상품 라인", "Product-line shares"),
        ("index_group_no", "int", "Line group code", "라인 그룹 코드", ""),
        ("index_group_name", "category", "Line group, the broadest level", "가장 큰 분류인 라인 그룹", ""),
        ("section_no", "int", "Section code", "섹션 코드", ""),
        ("section_name", "category", "Section within a line", "라인 안의 섹션", ""),
        ("garment_group_no", "int", "Garment group code", "의류 그룹 코드", ""),
        ("garment_group_name", "category", "Garment group by material or style", "소재·스타일별 의류 그룹", ""),
        ("detail_desc", "string", "Product description text", "상품 설명 문장", ""),
    ],
}

ROW_UNIT = {
    "transactions_train.csv": "one item bought",
    "customers.csv": "one registered customer",
    "articles.csv": "one article",
}


def profile(file, columns):
    df = pd.read_csv(DATA / file, dtype=str, usecols=[c[0] for c in columns])
    rows = []
    for col, typ, en, ko, used in columns:
        s = df[col]
        top = s.value_counts().head(3).index.tolist()
        rows.append({
            "file": file,
            "row_unit": ROW_UNIT[file],
            "column": col,
            "type": typ,
            "description_en": en,
            "description_ko": ko,
            "examples": " | ".join(x[:40] for x in top),
            "distinct_values": int(s.nunique()),
            "missing_pct": round(float(s.isna().mean() * 100), 2),
            "rows_in_file": len(df),
            "used_in_analysis": used,
        })
        print(f"{file}.{col}")
    return rows


def main():
    rows = []
    for file, columns in DESCRIPTIONS.items():
        rows += profile(file, columns)
    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"saved {OUT_CSV}")
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        print("openpyxl not installed; skipped .xlsx")
        return
    with pd.ExcelWriter(OUT_XLSX) as xw:
        out.to_excel(xw, sheet_name="all", index=False)
        for file in DESCRIPTIONS:
            out[out["file"] == file].to_excel(xw, sheet_name=file.split(".")[0][:31], index=False)
    print(f"saved {OUT_XLSX}")


if __name__ == "__main__":
    main()
