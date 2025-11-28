"""
Train a simple regression model to predict housing prices.

This script reads the provided housing dataset, splits it into training and test sets,
trains a linear regression model (wrapped in a pipeline that standardises numerical
features), evaluates it and saves both the trained model and its metadata.

The resulting artefacts are stored in the same directory:

* `house_price_model.pkl` – a pickled scikit‑learn pipeline ready for inference.
* `model_info.json` – a JSON file containing the model's coefficients, intercept and
  evaluation metrics.

Run this script from the repository root or from within the `model` directory:

```sh
python model/train_model.py
```

or

```sh
cd model
python train_model.py
```
"""
import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def load_dataset(csv_path: Path) -> pd.DataFrame:
    """Read the housing dataset from CSV."""
    return pd.read_csv(csv_path)


def train_model(df: pd.DataFrame):
    """Train a linear regression model on the housing dataset.

    Returns the trained pipeline, evaluation metrics and column names.
    """
    # Drop id column if present
    X = df.drop(columns=[col for col in ["id", "price"] if col in df.columns])
    y = df["price"]

    # Identify numerical columns
    numeric_features = X.columns.tolist()

    # Create preprocessing and model pipeline
    preprocessor = ColumnTransformer(
        transformers=[("num", StandardScaler(), numeric_features)]
    )
    model = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("regressor", LinearRegression()),
    ])

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Fit model
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Compute metrics
    metrics = {
        "r2": r2_score(y_test, y_pred),
        "mae": mean_absolute_error(y_test, y_pred),
        "mse": mean_squared_error(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
    }

    # Extract coefficients (inverse transform to original scale)
    regressor = model.named_steps["regressor"]
    # Coefficients correspond to scaled features; we can compute approximate original coefficients
    # by dividing by standard deviation of each feature and scaling with target standard deviation.
    # For simplicity, record coefficients on the scaled space.
    coefficients = {feature: float(coef) for feature, coef in zip(numeric_features, regressor.coef_)}
    intercept = float(regressor.intercept_)

    model_info = {
        "features": numeric_features,
        "coefficients": coefficients,
        "intercept": intercept,
        "metrics": metrics,
    }
    return model, model_info


def save_artifacts(model, model_info: dict, output_dir: Path) -> None:
    """Persist the trained model and metadata to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "house_price_model.pkl"
    joblib.dump(model, model_path)
    info_path = output_dir / "model_info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(model_info, f, indent=2)
    print(f"Model saved to {model_path}")
    print(f"Model info saved to {info_path}")


def main():
    # Determine dataset path relative to project root
    # The dataset lives at the top level of the repository (one level above
    # `property_portal`).  Ascend two levels from this script to reach the
    # repository root (e.g. `/home/oai/share`) and locate the CSV.
    repo_root = Path(__file__).resolve().parents[2]
    data_path = repo_root / "House Price Dataset.csv"
    df = load_dataset(data_path)
    model, model_info = train_model(df)
    output_dir = Path(__file__).resolve().parent
    save_artifacts(model, model_info, output_dir)


if __name__ == "__main__":
    main()
