"""Enterprise Pipeline: Fetch latest HDX data, engineer features, run model."""
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from pathlib import Path

RAW_DATA_PATH = "experiments/gefs/bwa-rainfall-raw-new.csv"
ENGINEERED_PATH = "utils/bwa-rainfall-engineered.csv"
MODEL_PATH = "models/drought_ensemble.pkl"
FEATURES_PATH = "models/features.pkl"
OUTPUT_JSON = "utils/latest_forecast.json"


def load_and_engineer():
    print("1. Loading latest raw data...")
    df = pd.read_csv(RAW_DATA_PATH, parse_dates=["date"])
    df = df[df["adm_level"] == 1].copy()
    df["year"] = df.date.dt.year
    df["month"] = df.date.dt.month
    df["district"] = df["PCODE"].map({
        "BW08": "SOUTHERN", "BW09": "SOUTH EAST", "BW10": "KWENENG",
        "BW11": "KGATLENG", "BW12": "CENTRAL", "BW13": "NORTH EAST",
        "BW14": "NORTH WEST", "BW15": "CHOBE", "BW16": "GHANZI", "BW17": "KGALAGADI"
    })

    df = df.sort_values(["district", "date"]).reset_index(drop=True)

    print("2. Merging climate indices (ENSO, IOD)...")
    try:
        enso = pd.read_csv("utils/climate/enso_monthly.csv")
        df = df.merge(enso, on=["year", "month"], how="left")
        print(f"   ENSO merged: {df['enso_oni'].notna().sum():,} non-null")
    except FileNotFoundError:
        df["enso_oni"] = 0.0
        print("   ⚠️ enso_monthly.csv not found — filling with 0")

    # IOD merge (parse wide format if exists)
    try:
        from pathlib import Path
        iod_path = Path("utils/climate/iod_raw.txt")
        if iod_path.exists():
            lines = iod_path.read_text().strip().split("\n")[1:]
            rows = []
            for line in lines:
                parts = line.split()
                if len(parts) != 13:
                    continue
                year = int(parts[0])
                for month in range(1, 13):
                    try:
                        val = float(parts[month])
                        if abs(val) > 100:
                            val = None
                    except ValueError:
                        val = None
                    rows.append({"year": year, "month": month, "iod": val})
            iod_df = pd.DataFrame(rows)
            df = df.merge(iod_df, on=["year", "month"], how="left")
            print(f"   IOD merged: {df['iod'].notna().sum():,} non-null")
        else:
            df["iod"] = 0.0
    except Exception as e:
        df["iod"] = 0.0
        print(f"   ⚠️ IOD merge failed: {e}")

    print("3. Engineering features...")
    df['is_wet']    = df.month.isin([11, 12, 1, 2, 3]).astype(int)
    df['rfh_ratio'] = df.rfh / (df.rfh_avg + 1)
    df['r1h_ratio'] = df.r1h / (df.r1h_avg + 1)

    for lag in range(1, 7):
        df[f'r3h_lag{lag}'] = df.groupby('district').r3h.shift(lag)
        df[f'r3h_lag{lag}_ratio'] = df[f'r3h_lag{lag}'] / (df.groupby('district').r3h_avg.shift(lag) + 1)

    for lag in range(1, 4):
        df[f'r1h_lag{lag}'] = df.groupby('district').r1h.shift(lag)

    df['lagged_3mo_avg']   = (df.r3h_lag1 + df.r3h_lag2 + df.r3h_lag3) / 3
    df['lagged_3mo_ratio'] = df.lagged_3mo_avg / (df.groupby('district').r3h_avg.shift(1) + 1)

    for lag in range(1, 7):
        df[f'r3h_below_{lag}'] = (df[f'r3h_lag{lag}'] < df.groupby('district').r3h_avg.shift(lag)).astype(int)
    df['recent_deficit_count'] = sum(df[f'r3h_below_{l}'] for l in range(1, 7))

    daily_region = (df.groupby('date')['r3h_lag1_ratio'].transform('mean') * df.shape[0] - df['r3h_lag1_ratio']) / (df.shape[0] - 1)
    df['neighbour_lag1_ratio'] = daily_region

    daily_region2 = (df.groupby('date')['r3h_lag2_ratio'].transform('mean') * df.shape[0] - df['r3h_lag2_ratio']) / (df.shape[0] - 1)
    df['neighbour_lag2_ratio'] = daily_region2

    df.to_csv(ENGINEERED_PATH, index=False)
    return df


def run_pipeline():
    df = load_and_engineer()

    print("4. Loading model...")
    bundle = joblib.load(MODEL_PATH)
    rf, xgb = bundle["rf"], bundle["xgb"]
    features = joblib.load(FEATURES_PATH)
    print(f"   Model expects {len(features)} features")

    latest_date = df["date"].max()
    latest_data = df[df["date"] == latest_date].copy()
    print(f"5. Running predictions for {latest_date.date()} ({len(latest_data)} districts)...")

    # Verify all features exist
    missing = [f for f in features if f not in latest_data.columns]
    if missing:
        print(f"   ❌ Missing features: {missing}")
        return

    results = []
    for _, row in latest_data.iterrows():
        X = pd.DataFrame([row[features].fillna(0).to_dict()])[features]

        rf_p = rf.predict_proba(X)[0, 1]
        xgb_p = xgb.predict_proba(X)[0, 1]
        prob = (rf_p + xgb_p) / 2

        tier = "HIGH" if prob >= 0.80 else "ELEVATED" if prob >= 0.65 else "LOW"

        results.append({
            "district": row["district"],
            "dekad": str(latest_date.date()),
            "probability": round(float(prob), 4),
            "tier": tier
        })

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "dekad": str(latest_date.date()),
        "predictions": results
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved: {OUTPUT_JSON}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run_pipeline()
