import streamlit as st

st.set_page_config(
    page_title="Resources · Pula Watch",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Resources")
st.caption("Data sources, references, and links for further reading.")

# ---------------- DATASETS ----------------
st.header("Rainfall & climate data")

st.markdown("""
| Source | Coverage | Link |
|---|---|---|
| **CHIRPS v2** (via HDX) | Global, 1981–present, 0.05° | [data.humdata.org](https://data.humdata.org/dataset/bwa-rainfall-subnat-full) |
| **CHIRPS** (UCSB official) | Global, 1981–present | [chc.ucsb.edu](https://www.chc.ucsb.edu/data/chirps) |
| **TAMSAT** | Africa, 1983–present | [tamsat.org](https://www.tamsat.org.uk/) |
| **ERA5** | Global reanalysis, 1940–present | [copernicus.eu](https://cds.climate.copernicus.eu/) |
| **SMAP** | Soil moisture, 2015–present | [smap.jpl.nasa.gov](https://smap.jpl.nasa.gov/) |
""")

# ---------------- BOUNDARIES ----------------
st.header("Administrative boundaries")

st.markdown("""
| Source | Coverage | Link |
|---|---|---|
| **COD-AB Botswana** | District boundaries (ADM1, ADM2) | [data.humdata.org](https://data.humdata.org/dataset/cod-ab-bwa) |
| **GADM** | Global admin boundaries | [gadm.org](https://gadm.org/) |
| **Natural Earth** | Global boundaries, scale 1:10m | [naturalearthdata.com](https://www.naturalearthdata.com/) |
""")

# ---------------- CLIMATE INDICES ----------------
st.header("Climate indices")

st.markdown("""
| Index | Relevance to Botswana | Link |
|---|---|---|
| **ENSO** (ONI) | Strong control on southern African rainfall | [NOAA CPC](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php) |
| **Indian Ocean Dipole (IOD)** | Modulates southern African wet season | [BOM](http://www.bom.gov.au/climate/iod/) |
| **Southern Annular Mode (SAM)** | Mid-latitude pressure belt influence | [NOAA](https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/aao/aao.shtml) |
| **Standardized Precipitation Index (SPI)** | WMO-recommended drought index | [WMO](https://public.wmo.int/en/resources/library/standardized-precipitation-index-spi) |
""")

# ---------------- DROUGHT STANDARDS ----------------
st.header("Drought classification standards")

st.markdown("""
Pula Watch classifies drought using **SADC / FEWS NET** thresholds on the
3-month rainfall percentile (`r3q`):

| `r3q` range | Classification |
|---|---|
| < 50 | Extreme drought |
| 50–60 | Severe drought |
| 60–80 | Moderate drought |
| 80–120 | Normal |
| 120–160 | Wet |
| > 160 | Very wet |

**Reference documents:**
- [FEWS NET methodology](https://fews.net/) — Famine Early Warning Systems Network
- [SADC Climate Services Centre](https://www.sadc.int/) — Regional climate bulletins
- [WMO Handbook on Drought Indicators](https://library.wmo.int/) — Global standards
""")

# ---------------- TOOLS & LIBRARIES ----------------
st.header("Tools & libraries")

st.markdown("""
- [Streamlit](https://streamlit.io/) — interactive web apps in Python
- [scikit-learn](https://scikit-learn.org/) — Random Forest, model selection
- [XGBoost](https://xgboost.readthedocs.io/) — gradient boosting
- [GeoPandas](https://geopandas.org/) — vector spatial data
- [Plotly](https://plotly.com/python/) — interactive visualisation
- [pandas](https://pandas.pydata.org/) — data manipulation
""")

# ---------------- FURTHER READING ----------------
st.header("Further reading")

st.markdown("""
**Drought monitoring in southern Africa:**
- Nicholson, S. E. (2018). *Climate and environmental change in Africa during the last 40 years.* Climate Research.
- Reason, C. J. C. (2017). *Climate change and its impacts on southern African rainfall.* WIREs Climate Change.
- Archer, E. et al. (2017). *Understanding the evolution of the 2015–2016 El Niño-induced drought in South Africa.*

**Machine learning for climate:**
- Reichstein, M. et al. (2019). *Deep learning and process understanding for data-driven Earth system science.* Nature.
- Ham, Y. G. et al. (2019). *Deep learning for multi-year ENSO forecasts.* Nature.

**Botswana-specific:**
- [Botswana Department of Meteorological Services](http://www.met.gov.bw/)
- [Botswana Ministry of Agriculture](https://www.gov.bw/ministries/ministry-agricultural-development-and-food-security)
""")

st.markdown("---")
st.caption("Links checked October 2026. External sources are not affiliated with Pula Watch.")
