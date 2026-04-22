from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DEFAULT_DATASET_PATH = "/workspace/data/raw/marketing_campaign.csv"
DEFAULT_DB_PATH = "/workspace/runtime/analytics.db"
DEFAULT_REPORTS_DIR = "/workspace/reports"
DEFAULT_PLOTS_DIR = "/workspace/plots"
TABLE_NAME = "customers"


def env_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default))


def dataset_path() -> Path:
    return env_path("DATASET_PATH", DEFAULT_DATASET_PATH)


def db_path() -> Path:
    return env_path("DB_PATH", DEFAULT_DB_PATH)


def reports_dir() -> Path:
    path = env_path("REPORTS_DIR", DEFAULT_REPORTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plots_dir() -> Path:
    path = env_path("PLOTS_DIR", DEFAULT_PLOTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    csv_path = path or dataset_path()
    df = pd.read_csv(csv_path, sep="\t")
    df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
    df["Dt_Customer"] = pd.to_datetime(
        df["Dt_Customer"], format="%d-%m-%Y", errors="coerce"
    )
    return df


def connect_database(path: Path | None = None) -> sqlite3.Connection:
    database_path = path or db_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(database_path)


def load_dataframe_from_db(table_name: str = TABLE_NAME) -> pd.DataFrame:
    with connect_database() as connection:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


def wait_for_table(table_name: str = TABLE_NAME, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    database = db_path()
    while time.time() < deadline:
        if database.exists():
            try:
                with connect_database(database) as connection:
                    row = connection.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
                        (table_name,),
                    ).fetchone()
                if row:
                    return
            except sqlite3.Error:
                pass
        time.sleep(2)
    raise TimeoutError(f"Timed out waiting for table '{table_name}' in {database}")


def write_json_report(filename: str, payload: dict) -> Path:
    target = reports_dir() / filename
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target


def load_csv_into_sqlite(table_name: str = TABLE_NAME) -> tuple[Path, int]:
    df = load_dataset()
    with connect_database() as connection:
        df.to_sql(table_name, connection, if_exists="replace", index=False)
    return db_path(), len(df)


def build_quality_report(table_name: str = TABLE_NAME) -> dict:
    wait_for_table(table_name)
    df = load_dataframe_from_db(table_name)

    numeric_columns = [
        column
        for column in [
            "Income",
            "MntWines",
            "MntMeatProducts",
            "NumWebPurchases",
            "NumStorePurchases",
        ]
        if column in df.columns
    ]
    type_validation = {}
    for column in numeric_columns:
        coerced = pd.to_numeric(df[column], errors="coerce")
        type_validation[column] = int(coerced.isna().sum() - df[column].isna().sum())

    report = {
        "dataset": TABLE_NAME,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_values": {
            column: int(value) for column, value in df.isna().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_ids": int(df.duplicated(subset=["ID"]).sum())
        if "ID" in df.columns
        else 0,
        "invalid_numeric_values": type_validation,
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }
    write_json_report("data_quality_report.json", report)
    return report


def build_research_report(table_name: str = TABLE_NAME) -> dict:
    wait_for_table(table_name)
    df = load_dataframe_from_db(table_name)

    numeric_summary = (
        df[
            [
                "Income",
                "MntWines",
                "MntMeatProducts",
                "NumWebPurchases",
                "NumStorePurchases",
            ]
        ]
        .apply(pd.to_numeric, errors="coerce")
        .describe()
        .round(2)
        .to_dict()
    )

    response_rate = float(
        pd.to_numeric(df["Response"], errors="coerce").fillna(0).mean()
    )
    top_education = (
        df["Education"].fillna("Unknown").value_counts().head(5).to_dict()
        if "Education" in df.columns
        else {}
    )

    report = {
        "row_count": int(len(df)),
        "income_mean": round(
            float(pd.to_numeric(df["Income"], errors="coerce").mean()), 2
        ),
        "income_median": round(
            float(pd.to_numeric(df["Income"], errors="coerce").median()), 2
        ),
        "response_rate": round(response_rate, 4),
        "top_education_levels": top_education,
        "numeric_summary": numeric_summary,
        "generated_at": pd.Timestamp.utcnow().isoformat(),
    }
    write_json_report("data_research_report.json", report)
    return report


def build_visualizations(table_name: str = TABLE_NAME) -> list[str]:
    wait_for_table(table_name)
    df = load_dataframe_from_db(table_name)
    target_dir = plots_dir()
    generated_files = []

    income_path = target_dir / "income_distribution.png"
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Income", bins=40, kde=True)
    plt.title("Income Distribution")
    plt.xlabel("Income")
    plt.tight_layout()
    plt.savefig(income_path)
    plt.close()
    generated_files.append(income_path.name)

    spending_path = target_dir / "wine_vs_meat_spending.png"
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="MntWines", y="MntMeatProducts", hue="Education")
    plt.title("Wine vs Meat Spending")
    plt.xlabel("Wine Spending")
    plt.ylabel("Meat Spending")
    plt.tight_layout()
    plt.savefig(spending_path)
    plt.close()
    generated_files.append(spending_path.name)

    write_json_report(
        "visualization_report.json",
        {
            "generated_files": generated_files,
            "generated_at": pd.Timestamp.utcnow().isoformat(),
        },
    )
    return generated_files
