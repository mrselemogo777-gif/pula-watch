"""Botswana district choropleth: % of dekads in drought, 1981–2026."""
import plotly.express as px
import streamlit as st


class MapView:
    """Renders the district-exposure choropleth (falls back to bar chart)."""

    def __init__(self, data_loader):
        self.dl = data_loader

    def render(self) -> None:
        st.subheader("District drought exposure")
        try:
            self._render_map()
        except AttributeError:
            st.info("Map requires plotly<6. Showing bar chart instead.")
            self._render_bar_fallback()

    # ------------------------------------------------------------------
    def _render_map(self) -> None:
        df  = self.dl.rainfall
        gdf = self.dl.districts

        exposure = (
            df.groupby("district")["is_drought"].mean().mul(100)
            .reset_index().rename(columns={"is_drought": "exposure"})
        )
        merged = gdf.merge(exposure, left_on="ADM1_EN",
                           right_on="district", how="left")

        fig = px.choropleth_mapbox(
            merged,
            geojson=merged.geometry,
            locations=merged.index,
            color="exposure",
            hover_name="district",
            hover_data={"exposure": ":.1f"},
            color_continuous_scale="YlOrRd",
            mapbox_style="carto-positron",
            zoom=4.5,
            center={"lat": -22.3, "lon": 24.7},
            opacity=0.7,
        )
        fig.update_layout(
            height=550,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="% dekads\nin drought"),
        )
        st.plotly_chart(fig, use_container_width=True)

    def _render_bar_fallback(self) -> None:
        exposure = (
            self.dl.rainfall.groupby("district")["is_drought"].mean()
            .mul(100).sort_values(ascending=True)
        )
        st.bar_chart(exposure)
