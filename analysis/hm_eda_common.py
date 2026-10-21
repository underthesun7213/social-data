"""Shared loader for the H&M EDA cycles.

The first call reads the Kaggle CSVs from data/hm/ and caches compact parquet
copies next to them (customer and article ids become integer codes), so later
runs load in seconds instead of minutes.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "hm"
ONLINE = 2  # assumption: sales_channel_id 2 = online
AGE_BINS = [16, 25, 35, 45, 55, 65, np.inf]
AGE_LABELS = ["16-24", "25-34", "35-44", "45-54", "55-64", "65+"]
ART_COLS = ["article_id", "product_code", "product_type_name", "product_group_name",
            "graphical_appearance_name", "colour_group_name", "perceived_colour_master_name",
            "department_name", "index_name", "index_group_name", "section_name", "garment_group_name"]


def _build_cache():
    cust = pd.read_csv(DATA / "customers.csv", dtype={"customer_id": "string", "age": "float32"})
    cust["c"] = np.arange(len(cust), dtype=np.int32)
    art = pd.read_csv(DATA / "articles.csv", usecols=ART_COLS, dtype={"article_id": "int32"})
    tx = pd.read_csv(
        DATA / "transactions_train.csv",
        dtype={"t_dat": "category", "customer_id": "string", "article_id": "int32",
               "price": "float32", "sales_channel_id": "int8"},
    )
    tx["t_dat"] = tx["t_dat"].cat.rename_categories(pd.to_datetime(tx["t_dat"].cat.categories))
    tx["t_dat"] = tx["t_dat"].astype("datetime64[ns]")
    code = pd.Series(cust["c"].to_numpy(), index=cust["customer_id"])
    tx["c"] = code.reindex(tx["customer_id"]).to_numpy().astype(np.int32)
    tx = tx.drop(columns="customer_id")
    tx.to_parquet(DATA / "tx.parquet", index=False)
    cust.drop(columns="customer_id").to_parquet(DATA / "customers.parquet", index=False)
    art.to_parquet(DATA / "articles.parquet", index=False)


def load():
    """Return (tx, cust, art). tx columns: t_dat, article_id, price, sales_channel_id, c."""
    if not (DATA / "tx.parquet").exists():
        _build_cache()
    tx = pd.read_parquet(DATA / "tx.parquet")
    cust = pd.read_parquet(DATA / "customers.parquet")
    art = pd.read_parquet(DATA / "articles.parquet")
    cust["age_band"] = pd.cut(cust["age"], AGE_BINS, right=False, labels=AGE_LABELS)
    return tx, cust, art
