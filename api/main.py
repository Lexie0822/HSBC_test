"""
FastAPI service exposing the housing price prediction model.

This application loads a pre‑trained scikit‑learn pipeline from the `model` directory and
provides REST endpoints for making predictions, retrieving model information and checking
service health.

The service defines three routes:

* `GET /health` – returns a simple JSON object to indicate the API is running.
* `GET /model-info` – returns the model's features, coefficients, intercept and evaluation metrics.
* `POST /predict` – accepts either a single house object or a list of houses and returns
  predicted prices.

To run the application locally:

```sh
pip install -r requirements.txt
uvicorn main:app --reload
```
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Union

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, confloat


class HouseFeatures(BaseModel):
    """Represents the input schema for a single house.

    All fields are required and mirror the columns used during training (except `id` and `price`).
    """
    square_footage: confloat(gt=0)
    bedrooms: conint(ge=0)
    bathrooms: confloat(gt=0)
    year_built: conint(gt=1800)
    lot_size: confloat(gt=0)
    distance_to_city_center: confloat(ge=0)
    school_rating: confloat(ge=0, le=10)


class PredictionResponse(BaseModel):
    """Response schema for the predict endpoint."""
    predictions: List[float]



def load_artifacts() -> tuple[object, dict]:
    """Load the trained model pipeline and metadata from disk."""
    # The model directory is sibling to this file's parent: property_portal/model
    base_dir = Path(__file__).resolve().parents[2] / "model"
    model_path = base_dir / "house_price_model.pkl"
    info_path = base_dir / "model_info.json"
    if not model_path.exists() or not info_path.exists():
        raise FileNotFoundError(
            "Model artifacts not found. Please run the training script in `model/train_model.py`."
        )
    model = joblib.load(model_path)
    with open(info_path, "r", encoding="utf-8") as f:
        model_info = json.load(f)
    return model, model_info


app = FastAPI(title="Housing Price Prediction API", version="1.0.0")

# Load model and info at startup
MODEL, MODEL_INFO = load_artifacts()


@app.get("/health")
async def health_check():
    """Health endpoint used for readiness and liveness probes."""
    return {"status": "ok"}


@app.get("/model-info", response_model=dict)
async def model_info():
    """Return information about the trained model."""
    return MODEL_INFO


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: Union[HouseFeatures, List[HouseFeatures]]):
    """Predict house prices for a single property or a list of properties.

    The endpoint accepts either a JSON object representing a single house or a JSON array
    of such objects.  It returns a list of predicted prices in the same order.
    """
    # Normalise to a list
    if isinstance(features, HouseFeatures):
        feature_list = [features]
    else:
        if not features:
            raise HTTPException(status_code=400, detail="Input list is empty")
        feature_list = features

    # Convert to DataFrame
    data = pd.DataFrame([item.dict() for item in feature_list])
    # Perform prediction
    try:
        preds = MODEL.predict(data).tolist()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")
    return PredictionResponse(predictions=[round(float(p), 2) for p in preds])
