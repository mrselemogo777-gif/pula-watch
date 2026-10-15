"""Historical context: drought dekads per year + district exposure ranking."""
import streamlit as st


class HistoryView:
    """Renders the historical charts below the prediction panel."""

    def __init__(self, data_loader):
        self.dl = data_loader

    def render(self) -> None:
        df = self.dl.rainfall
        col1, col2 = st.columns(2)

        with col1:
            self._render_yearly_chart(df)
        with col2:
            self._render_district_table(df)

    # ------------------------------------------------------------------
    def _render_yearly_chart(self, df) -> None:
        st.subheader("Drought dekads per year")
        yearly = df[df["is_drought"] == 1].groupby("year").size()
        st.bar_chart(yearly)

    def _render_district_table(self, df) -> None:
        st.subheader("Most exposed districts")
        rank = (
            df[df["r3q"].notna()]
            .groupby("district")["is_drought"].mean().mul(100)
            .sort_values(ascending=False)
        )
        st.dataframe(rank.round(1).rename("% dekads in drought"))
