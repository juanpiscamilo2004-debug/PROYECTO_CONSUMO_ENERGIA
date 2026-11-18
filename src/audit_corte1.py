"""Replica auditable del protocolo de Corte 1 sin modificar sus notebooks."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "energydata_complete.csv"
OUTPUT_PATH = ROOT / "reports" / "cp08_auditoria_corte1.json"


def metrics(y_true: pd.Series, prediction: np.ndarray) -> dict[str, float]:
    return {
        "mae_wh": float(mean_absolute_error(y_true, prediction)),
        "rmse_wh": float(np.sqrt(mean_squared_error(y_true, prediction))),
        "r2": float(r2_score(y_true, prediction)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    raw = args.data.read_bytes()
    raw_df = pd.read_csv(args.data)
    original_shape = list(raw_df.shape)
    original_columns = list(raw_df.columns)
    df = raw_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["hour"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.day_of_week
    df["month"] = df["date"].dt.month
    df["weekend"] = (df["day_of_week"] >= 5).astype(int)

    n_rows = len(df)
    train_end, validation_end = int(n_rows * 0.70), int(n_rows * 0.85)
    train = df.iloc[:train_end].copy()
    validation = df.iloc[train_end:validation_end].copy()
    test = df.iloc[validation_end:].copy()
    y_train, y_validation = train["Appliances"], validation["Appliances"]

    median_prediction = np.full(len(validation), y_train.median())
    hourly_medians = train.groupby("hour")["Appliances"].median()
    hourly_prediction = validation["hour"].map(hourly_medians).to_numpy()

    excluded = ["date", "Appliances", "rv1", "rv2"]
    features = [column for column in train.columns if column not in excluded]
    x_train, x_validation = train[features], validation[features]
    linear = LinearRegression().fit(x_train, y_train)
    ridge = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=1.0)),
    ]).fit(x_train, y_train)

    linear_prediction = linear.predict(x_validation)
    ridge_prediction = ridge.predict(x_validation)
    p90_train = float(y_train.quantile(0.90))
    high = y_validation >= p90_train

    results = {
        "audit_type": "independent exact replication of Corte 1 protocol",
        "data": {
            "path": str(args.data),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "shape": original_shape,
            "columns": original_columns,
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "date_min": str(df["date"].min()),
            "date_max": str(df["date"].max()),
            "rv1_equals_rv2": bool(df["rv1"].equals(df["rv2"])),
            "rv_max_absolute_difference": float((df["rv1"] - df["rv2"]).abs().max()),
        },
        "split": {
            "train_rows": len(train), "validation_rows": len(validation), "test_rows": len(test),
            "train_end": str(train["date"].max()),
            "validation_start": str(validation["date"].min()),
            "validation_end": str(validation["date"].max()),
            "test_start": str(test["date"].min()),
        },
        "features_excluding_rv1_rv2": features,
        "validation_metrics": {
            "baseline_historical_median": metrics(y_validation, median_prediction),
            "baseline_hourly_median": metrics(y_validation, hourly_prediction),
            "linear_regression": metrics(y_validation, linear_prediction),
            "ridge_alpha_1": metrics(y_validation, ridge_prediction),
        },
        "p90_train_wh": p90_train,
        "validation_high_consumption_rows": int(high.sum()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
