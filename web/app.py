from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, send_from_directory

from common.pipeline import (
    TABLE_NAME,
    db_path,
    load_dataframe_from_db,
    plots_dir,
    reports_dir,
)


app = Flask(__name__)


def read_json_report(name: str) -> dict:
    target = reports_dir() / name
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def preview_records(limit: int = 10) -> list[dict]:
    database = db_path()
    if not database.exists():
        return []

    try:
        df = load_dataframe_from_db(TABLE_NAME).head(limit)
    except Exception:
        return []

    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


@app.get("/")
def index() -> str:
    return render_template(
        "index.html",
        project_name="Docker Workspace Data Analytics",
        dataset_rows=preview_records(),
        quality_report=read_json_report("data_quality_report.json"),
        research_report=read_json_report("data_research_report.json"),
        visualization_report=read_json_report("visualization_report.json"),
    )


@app.get("/plots/<path:filename>")
def plot_file(filename: str):
    return send_from_directory(plots_dir(), filename)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "port": os.environ.get("PORT", "8000")}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
