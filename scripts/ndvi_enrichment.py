"""NDVI enrichment for Pula Watch forecast pipeline."""
import requests
import pandas as pd

DISTRICT_TO_PCODE = {
    "CENTRAL":    "BW12",
    "CHOBE":      "BW15",
    "GHANZI":     "BW16",
    "KGALAGADI":  "BW17",
    "KGATLENG":   "BW11",
    "KWENENG":    "BW10",
    "NORTH EAST": "BW13",
    "NORTH WEST": "BW14",
    "SOUTH EAST": "BW09",
    "SOUTHERN":   "BW08",
}


def fetch_ndvi_data():
    try:
        meta = requests.get(
            "https://data.humdata.org/api/action/package_show",
            params={"id": "bwa-ndvi-subnational"}, timeout=20,
        ).json()
        csv_url = next(
            r["url"] for r in meta["result"]["resources"]
            if "5ytd" in r["name"].lower()
        )
        df = pd.read_csv(csv_url)
        latest_date = df["date"].max()
        latest = df[df["date"] == latest_date]
        by_pcode = {}
        for _, row in latest.iterrows():
            vim = float(row["vim"]) if pd.notna(row["vim"]) else None
            viq = float(row["viq"]) if pd.notna(row["viq"]) else None
            by_pcode[row["PCODE"]] = {"vim": vim, "viq": viq}
        print(f"NDVI fetched: {latest_date}, {len(by_pcode)} PCODEs")
        return {"date": latest_date, "by_pcode": by_pcode}
    except Exception as e:
        print(f"NDVI fetch failed: {e}")
        return None


def enrich_output(output):
    ndvi = fetch_ndvi_data()
    for pred in output["predictions"]:
        pcode = DISTRICT_TO_PCODE.get(pred["district"].upper())
        if ndvi and pcode and pcode in ndvi["by_pcode"]:
            entry = ndvi["by_pcode"][pcode]
            pred["ndvi_vim"] = round(entry["vim"], 4) if entry["vim"] is not None else None
            pred["ndvi_viq"] = round(entry["viq"], 4) if entry["viq"] is not None else None
        else:
            pred["ndvi_vim"] = None
            pred["ndvi_viq"] = None

        tier = pred.get("tier", "LOW")
        viq  = pred.get("ndvi_viq")
        if tier == "HIGH" and viq is not None and viq < 100:
            pred["food_security_flag"] = "PRIORITY"
        elif tier == "HIGH":
            pred["food_security_flag"] = "HIGH_RAINFALL"
        elif tier == "ELEVATED":
            pred["food_security_flag"] = "MONITOR"
        else:
            pred["food_security_flag"] = "NORMAL"

    output["ndvi_date"] = ndvi["date"] if ndvi else None
    return output
