from utils.data_loader import DataLoader
from services.feature_builder import FeatureBuilder
from services.predictor import DroughtPredictor
import joblib

dl = DataLoader().load()
features = joblib.load("models/features.pkl")
fb = FeatureBuilder(dl.rainfall, features)
predictor = DroughtPredictor().load()

sub = dl.rainfall[dl.rainfall["r3h_lag6"].notna()].copy()

yellows = []
total = len(sub)
for i, (_, row) in enumerate(sub.iterrows()):
    if i % 2000 == 0:
        print(f"  scanned {i}/{total}...")
    d = row["date"].date()
    try:
        frow = fb.build(row["district"], d)
    except ValueError:
        continue
    probs = predictor.predict_proba(frow)
    p = probs["probability"]
    if 0.65 <= p < 0.80:
        yellows.append((row["district"], str(d), round(p, 3),
                        round(frow["lagged_3mo_ratio"], 3)))

yellows.sort(key=lambda x: -x[2])
print(f"\nYellow-flag dekads found: {len(yellows)}\n")
print(f"{'District':<12} {'Date':<12} {'Prob':>6} {'Lag':>6}")
print("-" * 42)
for y in yellows[:20]:
    print(f"{y[0]:<12} {y[1]:<12} {y[2]:>6} {y[3]:>6}")
