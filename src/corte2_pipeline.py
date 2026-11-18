"""CP09-CP12: pipeline temporal, benchmark y análisis de validación.

El instante de predicción es el del registro a estimar. Solo se usan calendario
derivado de ``date`` y mediciones exógenas del mismo instante. No se emplean
``Appliances`` contemporáneo, rezagos del objetivo ni información futura.
El bloque Test se delimita, pero este script no lo transforma, ajusta, predice
ni puntúa: permanece reservado para Corte 3.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "energydata_complete.csv"
REPORTS = ROOT / "reports"
RANDOM_STATE = 2026


def add_calendar_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create features known at the prediction timestamp, without lags."""
    result = frame.copy()
    date = pd.to_datetime(result["date"])
    hour = date.dt.hour + date.dt.minute / 60
    dow = date.dt.day_of_week
    doy = date.dt.day_of_year
    result["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    result["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    result["dow_sin"] = np.sin(2 * np.pi * dow / 7)
    result["dow_cos"] = np.cos(2 * np.pi * dow / 7)
    result["doy_sin"] = np.sin(2 * np.pi * doy / 366)
    result["doy_cos"] = np.cos(2 * np.pi * doy / 366)
    result["weekend"] = (dow >= 5).astype(int)
    return result


def scores(y_true: pd.Series, prediction: np.ndarray) -> dict[str, float]:
    return {
        "mae_wh": float(mean_absolute_error(y_true, prediction)),
        "rmse_wh": float(np.sqrt(mean_squared_error(y_true, prediction))),
        "r2": float(r2_score(y_true, prediction)),
    }


def model_candidates() -> dict[str, object]:
    """Small, predeclared search: regularization and capacity only."""
    return {
        "ridge_alpha_1": Pipeline([
            ("scale", StandardScaler()), ("model", Ridge(alpha=1.0))
        ]),
        "ridge_alpha_10": Pipeline([
            ("scale", StandardScaler()), ("model", Ridge(alpha=10.0))
        ]),
        "ridge_alpha_100": Pipeline([
            ("scale", StandardScaler()), ("model", Ridge(alpha=100.0))
        ]),
        "hist_gb_shallow": HistGradientBoostingRegressor(
            learning_rate=0.05, max_iter=300, max_leaf_nodes=15,
            l2_regularization=1.0, random_state=RANDOM_STATE,
        ),
        "hist_gb_medium": HistGradientBoostingRegressor(
            learning_rate=0.05, max_iter=400, max_leaf_nodes=31,
            l2_regularization=1.0, random_state=RANDOM_STATE,
        ),
        "extra_trees_regularized": ExtraTreesRegressor(
            n_estimators=300, max_features=0.7, min_samples_leaf=3,
            random_state=RANDOM_STATE, n_jobs=-1,
        ),
        "extra_trees_flexible": ExtraTreesRegressor(
            n_estimators=300, max_features=1.0, min_samples_leaf=1,
            random_state=RANDOM_STATE, n_jobs=-1,
        ),
    }


def make_figures(errors: pd.DataFrame, importances: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    window = errors.iloc[: 7 * 24 * 6]
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(window["date"], window["actual"], label="Consumo real", lw=1.4)
    ax.plot(window["date"], window["prediction"], label="Modelo provisional", lw=1.2)
    ax.axhline(errors["p90_train"].iat[0], color="tab:red", ls="--", lw=1, label="P90 Train")
    ax.set(title="Validación temporal: primera semana", xlabel="Fecha", ylabel="Appliances (Wh)")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(REPORTS / "cp12_serie_temporal_validacion.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = np.where(errors["is_high"], "tab:red", "tab:blue")
    ax.scatter(errors["actual"], errors["residual"], c=colors, alpha=0.35, s=10)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(errors["p90_train"].iat[0], color="tab:red", ls="--", lw=1)
    ax.set(title="Residuos en validación", xlabel="Consumo real (Wh)", ylabel="Residual: real - predicción (Wh)")
    fig.tight_layout()
    fig.savefig(REPORTS / "cp12_residuos_validacion.png", dpi=180)
    plt.close(fig)

    top = importances.head(12).sort_values("importance_mean")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.barh(top["feature"], top["importance_mean"], xerr=top["importance_std"], color="tab:green")
    ax.set(title="Importancia por permutación en validación", xlabel="Aumento de MAE al permutar")
    fig.tight_layout()
    fig.savefig(REPORTS / "cp12_importancia_permutacion.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DATA_PATH)
    args = parser.parse_args()
    REPORTS.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(args.data)
    raw["date"] = pd.to_datetime(raw["date"])
    raw = raw.sort_values("date").reset_index(drop=True)
    data = add_calendar_features(raw)
    n = len(data)
    train_end, validation_end = int(n * 0.70), int(n * 0.85)
    train, validation = data.iloc[:train_end].copy(), data.iloc[train_end:validation_end].copy()

    excluded = {"date", "Appliances", "rv1", "rv2"}
    features = [column for column in data.columns if column not in excluded]
    x_train, y_train = train[features], train["Appliances"]
    x_validation, y_validation = validation[features], validation["Appliances"]
    p90_train = float(y_train.quantile(0.90))

    records: list[dict[str, object]] = []
    predictions: dict[str, np.ndarray] = {}
    median_prediction = np.full(len(validation), y_train.median())
    hourly_median = train.assign(hour=train["date"].dt.hour).groupby("hour")["Appliances"].median()
    hourly_prediction = validation["date"].dt.hour.map(hourly_median).to_numpy()
    for name, prediction in {
        "baseline_historical_median": median_prediction,
        "baseline_hourly_median": hourly_prediction,
    }.items():
        records.append({"model": name, "family": "baseline", **scores(y_validation, prediction)})
        predictions[name] = prediction

    fitted: dict[str, object] = {}
    for name, model in model_candidates().items():
        model.fit(x_train, y_train)
        prediction = model.predict(x_validation)
        fitted[name], predictions[name] = model, prediction
        family = "ridge" if name.startswith("ridge") else ("hist_gradient_boosting" if name.startswith("hist") else "extra_trees")
        records.append({"model": name, "family": family, **scores(y_validation, prediction)})

    benchmark = pd.DataFrame(records).sort_values(["rmse_wh", "mae_wh"], ignore_index=True)
    benchmark.to_csv(REPORTS / "cp10_benchmark_validacion.csv", index=False)
    selected_name = benchmark.loc[benchmark["family"] != "baseline"].iloc[0]["model"]
    selected_model = fitted[str(selected_name)]
    selected_prediction = predictions[str(selected_name)]

    # Controlled ablation: same selected family/hyperparameters, only rv columns change.
    ablations: list[dict[str, object]] = []
    rv_sets = {
        "without_rv": [], "rv1_only": ["rv1"], "rv2_only": ["rv2"], "rv1_and_rv2": ["rv1", "rv2"],
    }
    params = selected_model.get_params(deep=True)
    for label, rv_columns in rv_sets.items():
        cols = features + rv_columns
        if str(selected_name).startswith("ridge"):
            model = Pipeline([("scale", StandardScaler()), ("model", Ridge(alpha=params["model__alpha"]))])
        elif str(selected_name).startswith("hist"):
            model = HistGradientBoostingRegressor(
                learning_rate=params["learning_rate"], max_iter=params["max_iter"],
                max_leaf_nodes=params["max_leaf_nodes"], l2_regularization=params["l2_regularization"],
                random_state=RANDOM_STATE,
            )
        else:
            model = ExtraTreesRegressor(
                n_estimators=params["n_estimators"], max_features=params["max_features"],
                min_samples_leaf=params["min_samples_leaf"], random_state=RANDOM_STATE, n_jobs=-1,
            )
        model.fit(train[cols], y_train)
        prediction = model.predict(validation[cols])
        ablations.append({"configuration": label, "included_rv_columns": ",".join(rv_columns) or "none", **scores(y_validation, prediction)})
    ablation = pd.DataFrame(ablations)
    ablation.to_csv(REPORTS / "cp12_ablacion_rv.csv", index=False)

    high = y_validation >= p90_train
    errors = pd.DataFrame({
        "date": validation["date"].to_numpy(), "actual": y_validation.to_numpy(),
        "prediction": selected_prediction, "p90_train": p90_train, "is_high": high.to_numpy(),
    })
    errors["residual"] = errors["actual"] - errors["prediction"]
    errors["absolute_error"] = errors["residual"].abs()
    errors.to_csv(REPORTS / "cp12_residuos_validacion.csv", index=False)
    segment_rows = []
    high_mask = errors["is_high"].to_numpy()
    for segment, mask in {"normal_<p90_train": ~high_mask, "high_>=p90_train": high_mask}.items():
        subset = errors.loc[mask]
        segment_rows.append({
            "segment": segment, "n": len(subset), "mae_wh": float(subset["absolute_error"].mean()),
            "rmse_wh": float(np.sqrt(np.mean(subset["residual"] ** 2))),
            "mean_residual_wh": float(subset["residual"].mean()),
            "underprediction_rate": float((subset["prediction"] < subset["actual"]).mean()),
        })
    segments = pd.DataFrame(segment_rows)
    segments.to_csv(REPORTS / "cp12_metricas_por_segmento.csv", index=False)
    errors.nlargest(15, "absolute_error").to_csv(REPORTS / "cp12_picos_peores_predichos.csv", index=False)

    importance = permutation_importance(
        selected_model, x_validation, y_validation, scoring="neg_mean_absolute_error",
        n_repeats=10, random_state=RANDOM_STATE, n_jobs=-1,
    )
    importances = pd.DataFrame({
        "feature": features, "importance_mean": importance.importances_mean,
        "importance_std": importance.importances_std,
    }).sort_values("importance_mean", ascending=False, ignore_index=True)
    importances.to_csv(REPORTS / "cp12_importancia_permutacion.csv", index=False)
    make_figures(errors, importances)

    metadata = {
        "prediction_contract": "Calendar and contemporaneous exogenous readings only; no target lags, current target, or future rows.",
        "test_policy": "Test begins at row 16774 and was neither fitted, predicted nor scored by this CP09-CP12 run.",
        "split": {"train_rows": len(train), "validation_rows": len(validation), "test_rows_reserved": n - validation_end},
        "p90_train_wh": p90_train,
        "selected_provisional_model_by_validation_rmse": str(selected_name),
        "selected_validation_metrics": scores(y_validation, selected_prediction),
        "software": {"python": sys.version, "platform": platform.platform(), "pandas": pd.__version__, "scikit_learn": sklearn.__version__},
        "random_state": RANDOM_STATE,
    }
    (REPORTS / "cp11_configuracion_y_metadatos.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
