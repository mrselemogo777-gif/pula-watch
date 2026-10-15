import streamlit as st

st.set_page_config(
    page_title="About · Pula Watch",
    page_icon="ℹ️",
    layout="wide",
)

st.title("ℹ️ About Pula Watch")
st.caption("Botswana Drought Early-Warning System")

# SCOPE
st.header("⚠️ Scope")

st.warning("""
**Pula Watch is a decision-support tool, not an autonomous warning system.**

It outputs drought probabilities and tiered flags for human review by
extension officers, NGOs, or researchers. It is **not** designed to trigger
aid disbursement, livestock movement, or water rationing without confirmation
from a qualified officer.
""")

# HOW TO USE 
st.header("How to use")

st.markdown("""
1. Go to the **Predict** page (home).
2. Select a **district**, **year**, and **dekad**.
3. Choose an **operating point** in the sidebar:
   - *Farmer / community alert* — high recall, tolerates false alarms
   - *Balanced (default)* — best F1
   - *Budget-constrained* — high precision, fewer false alarms
4. Click **🚨 Run prediction**.
5. Review the three-tier flag (🔴 high confidence / 🟡 elevated / 🟢 low).
6. Expand ** Full feature values** to see exactly what drove the prediction.

**All flags require human review before any action is taken.**
""")

# OPERATING POINTS 
st.header("Operating points")

st.markdown("""
| Persona | Threshold | Precision | Recall | Use case |
|---|---|---|---|---|
| Farmer / community alert | 0.50 | 0.721 | 0.842 | Never miss a drought |
| Balanced (default) | 0.65 | 0.834 | 0.792 | General purpose |
| Budget-constrained | 0.80 + rule | 0.906 | 0.646 | Only high-confidence flags |
| Highest confidence | 0.85 + rule | 0.930 | 0.605 | Minimal false alarms |
""")

# SOURCES 
st.header("Sources")

st.markdown("""
- **Rainfall data:** [HDX / WFP CHIRPS v2](https://data.humdata.org/dataset/bwa-rainfall-subnat-full)
- **District boundaries:** [HDX COD-AB Botswana](https://data.humdata.org/dataset/cod-ab-bwa)
- **Drought thresholds:** SADC / FEWS NET standard (`r3q < 60` = Severe/Extreme)
""")

# FUTURE WORK
st.header("🔬 Future work")

st.markdown("""
- Live CHIRPS API integration (currently manual dekad selection)
- Large-scale climate indices (ENSO, IOD)
- Satellite vegetation indices (NDVI, EVI)
- Soil moisture integration
- SMS / email alerting for extension officers
""")

#  AUTHOR 
st.header("Author")
st.markdown("""
**Legakwa Selemogo**
- GitHub: [@mrselemogo777-gif](https://github.com/mrselemogo777-gif)
- Project: [pula-watch](https://github.com/mrselemogo777-gif/pula-watch)

## License
MIT
""")
