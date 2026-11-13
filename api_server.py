"""FastAPI server for Pula Watch — serves classifier, forecaster, and latest forecast."""
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Pula Watch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
bundle = joblib.load("models/drought_ensemble.pkl")
rf, xgb = bundle["rf"], bundle["xgb"]
features = joblib.load("models/features.pkl")

df = pd.read_csv("utils/bwa-rainfall-engineered.csv", parse_dates=["date"])
df = df[df.r3q.notna()].copy()


class PredictRequest(BaseModel):
    district: str
    year: int
    dekad: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "models_loaded": True,
        "latest_forecast_exists": Path("utils/latest_forecast.json").exists(),
    }


@app.get("/forecast/latest")
def forecast_latest():
    """Return the latest auto-generated forecast from GitHub Actions."""
    path = Path("utils/latest_forecast.json")
    if not path.exists():
        raise HTTPException(status_code=404, detail="No forecast generated yet")
    with open(path) as f:
        return json.load(f)


@app.post("/predict")
def predict(req: PredictRequest):
    target = pd.to_datetime(req.dekad).date()
    matches = df[(df["district"] == req.district) & (df["date"].dt.date == target)]
    if matches.empty:
        raise HTTPException(status_code=404, detail="Dekad not found")

    row = matches.iloc[0]
    X = pd.DataFrame([row[features].fillna(0).to_dict()])[features]

    rf_p = float(rf.predict_proba(X)[0, 1])
    xgb_p = float(xgb.predict_proba(X)[0, 1])
    prob = (rf_p + xgb_p) / 2

    tier = "HIGH" if prob >= 0.80 else "ELEVATED" if prob >= 0.65 else "LOW"

    return {
        "district": req.district,
        "dekad": req.dekad,
        "probability": round(prob, 4),
        "tier": tier,
        "lagged_3mo_ratio": round(float(row["lagged_3mo_ratio"]), 3),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
