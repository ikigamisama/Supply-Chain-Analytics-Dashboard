import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


PRIMARY = "#0F4C81"
ACCENT = "#00B4D8"
SUCCESS = "#06D6A0"
WARNING = "#FFB703"
DANGER = "#EF233C"
BG_CARD = "#1A2744"
BG_DARK = "#0D1B2A"
TEXT_LIGHT = "#E8EDF4"
TEXT_MUTED = "#8FA3BF"
CHART_COLORS = [ACCENT, SUCCESS, WARNING,
                "#9B5DE5", "#F15BB5", "#FEE440", PRIMARY]

KPI_ACCENT_MAP = {
    "blue":   ACCENT,
    "green":  SUCCESS,
    "teal":   "#06D6A0",
    "yellow": WARNING,
    "purple": "#9B5DE5",
    "orange": "#FF6B35",
    "red":    DANGER,
}


@st.cache_data
def load_data(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    return df


class Data:
    def __init__(self, datasets: dict):
        self.datasets = datasets
        self.f_sales = load_data(self.datasets["sales"])
        self.f_procurement = load_data(self.datasets["procurement"])
        self.f_production = load_data(self.datasets["production"])
        self.f_inventory = load_data(self.datasets["inventory"])
        self.f_shipment = load_data(self.datasets["shipment"])
        self.dim_date = load_data(self.datasets["dim_date"])
        self.dim_product = load_data(self.datasets["dim_product"])
        self.dim_supplier = load_data(self.datasets["dim_supplier"])
        self.dim_customer = load_data(self.datasets["dim_customer"])
        self.dim_facility = load_data(self.datasets["dim_facility"])

    def filters_df(self, sel: dict):
        date_filtered = self.dim_date[self.dim_date["year"].isin(
            sel.get("year", []))]
        date_keys = date_filtered["date_key"].tolist()

        product_filtered = self.dim_product[self.dim_product["category"].isin(
            sel.get("category", []))]
        product_ids = product_filtered["product_id"].tolist()

        facility_filtered = self.dim_facility[self.dim_facility["facility_name"].isin(
            sel.get("facility_name", []))]
        facility_ids = facility_filtered["facility_id"].tolist()

        customer_filtered = self.dim_customer[self.dim_customer["country"].isin(
            sel.get("country", []))]
        customer_ids = customer_filtered["customer_id"].tolist()

        supplier_filtered = self.dim_supplier[self.dim_supplier["tier"].isin(
            sel.get("tier", []))]
        supplier_ids = supplier_filtered["supplier_id"].tolist()

        self.f_sales = self.f_sales[self.f_sales["date_key"].isin(date_keys) & self.f_sales["product_id"].isin(
            product_ids) & self.f_sales["customer_id"].isin(customer_ids)]
        self.f_procurement = self.f_procurement[self.f_procurement["order_date_key"].isin(
            date_keys) & self.f_procurement["product_id"].isin(product_ids) & self.f_procurement["supplier_id"].isin(supplier_ids)]
        self.f_production = self.f_production[self.f_production["date_key"].isin(
            date_keys) & self.f_production["product_id"].isin(product_ids) & self.f_production["facility_id"].isin(facility_ids)]
        self.f_inventory = self.f_inventory[self.f_inventory["date_key"].isin(
            date_keys) & self.f_inventory["product_id"].isin(product_ids) & self.f_inventory["facility_id"].isin(facility_ids)]
        self.f_shipment = self.f_shipment[
            self.f_shipment["ship_date_key"].isin(date_keys) &
            self.f_shipment["product_id"].isin(product_ids)
        ]

    def unique_values(self, df, column):
        return sorted(df[column].dropna().unique())

    def compute_kpis(self):
        return {
            'total_revenue': self.f_sales["net_revenue"].sum(),
            'total_profit': self.f_sales["profit"].sum(),
            'profit_margin': (self.f_sales["profit"].sum() / self.f_sales["net_revenue"].sum() * 100) if self.f_sales["net_revenue"].sum() > 0 else 0,
            'total_cost_sales': self.f_sales["total_cost"].sum(),
            'cost_ratio': (self.f_sales["total_cost"].sum() / self.f_sales["net_revenue"].sum() * 100) if self.f_sales["net_revenue"].sum() > 0 else 0,
            'total_orders': len(self.f_sales["order_number"].unique()),
            'delivered_ship': self.f_shipment[self.f_shipment["status"] == "Delivered"].shape[0],
            'total_ship': self.f_shipment.shape[0],
            'perfect_order_rate': (self.f_shipment[self.f_shipment["status"] == "Delivered"].shape[0] / self.f_shipment.shape[0] * 100) if self.f_shipment.shape[0] > 0 else 0,
            'avg_lead_time': self.f_procurement["lead_time_days"].mean() if len(self.f_procurement) > 0 else 0,
            'avg_discount': self.f_sales["discount_pct"].mean() if len(self.f_sales) > 0 else 0,
            'cash_cycle_days': self.f_procurement["lead_time_days"].mean() + 30
        }

    def render_kpi_card(self, col, icon, label, value, color_key, delta=""):
        accent = KPI_ACCENT_MAP.get(color_key, ACCENT)
        delta_html = (
            f"<div style='font-size:0.68rem; margin-top:0.2rem; color:{TEXT_MUTED}; "
            f"font-family:JetBrains Mono,monospace;'>{delta}</div>"
        ) if delta else ""
        col.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {BG_CARD} 0%, #0F2235 100%);
                border: 1px solid #1E3A5F;
                border-top: 3px solid {accent};
                border-radius: 12px;
                padding: 0.95rem 1.1rem 0.85rem 1.1rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                height: 100%;
            ">
                <div style="font-size:1.3rem; margin-bottom:0.3rem; line-height:1;">{icon}</div>
                <div style="
                    font-size:0.65rem;
                    color:{TEXT_MUTED};
                    text-transform:uppercase;
                    letter-spacing:0.07em;
                    font-family:'JetBrains Mono',monospace;
                    margin-bottom:0.25rem;
                ">{label}</div>
                <div style="
                    font-size:1.35rem;
                    font-weight:700;
                    color:white;
                    line-height:1.15;
                    font-family:'Sora',sans-serif;
                ">{value}</div>
                {delta_html}
            </div>
        """, unsafe_allow_html=True)

    def fmt_currency(self, v):
        if v >= 1e9:
            return f"${v/1e9:.2f}B"
        if v >= 1e6:
            return f"${v/1e6:.1f}M"
        if v >= 1e3:
            return f"${v/1e3:.1f}K"
        return f"${v:.0f}"


def get_title_style():
    theme = st.get_option("theme.base") or "light"

    return {
        'font': {
            'size': 22,
            'color': 'white' if theme != "dark" else "#2d3748"
        }
    }


def get_chart_layout(title="", height=340):
    return dict(
        title=dict(
            text=title,
            font=dict(size=13, color=TEXT_LIGHT, family="Sora"),
            x=0, xanchor="left"
        ),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_MUTED, family="Sora", size=11),
        margin=dict(l=10, r=10, t=38, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MUTED, size=10),
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ),
        xaxis=dict(
            gridcolor="#1E3A5F", zerolinecolor="#1E3A5F",
            tickfont=dict(color=TEXT_MUTED, size=10)
        ),
        yaxis=dict(
            gridcolor="#1E3A5F", zerolinecolor="#1E3A5F",
            tickfont=dict(color=TEXT_MUTED, size=10)
        ),
        colorway=CHART_COLORS,
    )


def apply_theme(fig, title="", height=340):
    fig.update_layout(**get_chart_layout(title, height))
    return fig


def chart_card(fig, title=""):
    st.markdown(f"#### {title}")
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)


class Chart(Data):
    def __init__(self, datasets: dict):
        super().__init__(datasets)

    def revenue_trend_chart(self):
        merged = self.f_sales.merge(
            self.dim_date[["date_key", "year", "month", "month_name"]], on="date_key")
        grouped = merged.groupby(["year", "month", "month_name"]).agg(
            revenue=("net_revenue", "sum"), profit=("profit", "sum")
        ).reset_index().sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["period"], y=grouped["revenue"], name="Revenue",
                             marker_color=ACCENT, opacity=0.85))
        fig.add_trace(go.Bar(x=grouped["period"], y=grouped["profit"], name="Profit",
                             marker_color=SUCCESS, opacity=0.85))
        fig.add_trace(go.Scatter(x=grouped["period"], y=grouped["profit"]/grouped["revenue"]*100,
                                 name="Margin %", yaxis="y2", line=dict(color=WARNING, width=2),
                                 mode="lines+markers", marker=dict(size=5)))
        fig.update_layout(barmode="overlay", yaxis2=dict(
            overlaying="y", side="right", ticksuffix="%",
            gridcolor="rgba(0,0,0,0)", tickfont=dict(color=WARNING, size=10)
        ))
        apply_theme(fig, height=320)
        return fig

    # Revenue by category
    def revenue_category_chart(self):
        merged = self.f_sales.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby("category")["net_revenue"].sum().reset_index()
        fig = px.pie(grouped, names="category", values="net_revenue",
                     color_discrete_sequence=CHART_COLORS, hole=0.55)
        fig.update_traces(textfont=dict(color="white", size=11),
                          marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=300)
        return fig

    # Top customers
    def top_customers_chart(self):
        merged = self.f_sales.merge(
            self.dim_customer[["customer_id", "customer_name"]], on="customer_id")
        grouped = merged.groupby("customer_name")[
            "net_revenue"].sum().nlargest(8).reset_index()
        grouped["short"] = grouped["customer_name"].str[:20]
        fig = px.bar(grouped, x="net_revenue", y="short", orientation="h",
                     color="net_revenue", color_continuous_scale=[[0, PRIMARY], [1, ACCENT]])
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=300)
        return fig

    # Profit margin by product line
    def margin_product_chart(self):
        merged = self.f_sales.merge(
            self.dim_product[["product_id", "product_line"]], on="product_id")
        grouped = merged.groupby("product_line").agg(
            revenue=("net_revenue", "sum"), profit=("profit", "sum")
        ).reset_index()
        grouped["margin"] = grouped["profit"] / grouped["revenue"] * 100
        fig = px.bar(grouped, x="product_line", y="margin",
                     color="margin", color_continuous_scale=[[0, DANGER], [0.5, WARNING], [1, SUCCESS]])
        fig.update_coloraxes(showscale=False)
        fig.update_layout(yaxis_ticksuffix="%")
        apply_theme(fig, height=290)
        return fig

    # Revenue by customer country
    def revenue_by_country_chart(self):
        merged = self.f_sales.merge(
            self.dim_customer[["customer_id", "country"]], on="customer_id")
        grouped = merged.groupby("country")["net_revenue"].sum(
        ).reset_index().sort_values("net_revenue", ascending=False)
        fig = px.bar(grouped, x="country", y="net_revenue",
                     color="net_revenue", color_continuous_scale=[[0, PRIMARY], [1, ACCENT]],
                     text=grouped["net_revenue"].map(self.fmt_currency))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=10))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # YoY Revenue comparison
    def yoy_revenue_chart(self):
        merged = self.f_sales.merge(
            self.dim_date[["date_key", "year", "month"]], on="date_key")
        grouped = merged.groupby(["year", "month"])[
            "net_revenue"].sum().reset_index()
        fig = px.line(grouped, x="month", y="net_revenue", color=grouped["year"].astype(str),
                      color_discrete_sequence=CHART_COLORS, markers=True, line_shape="spline")
        fig.update_traces(line_width=2, marker=dict(size=5))
        fig.update_layout(xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ), legend_title_text="Year")
        apply_theme(fig, height=290)
        return fig

    # Customer size segment revenue
    def customer_size_chart(self):
        merged = self.f_sales.merge(
            self.dim_customer[["customer_id", "size"]], on="customer_id")
        grouped = merged.groupby("size").agg(
            revenue=("net_revenue", "sum"),
            orders=("order_number", "nunique")
        ).reset_index()
        fig = px.bar(grouped, x="size", y="revenue", color="size",
                     color_discrete_sequence=CHART_COLORS,
                     text=grouped["revenue"].map(self.fmt_currency))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=10))
        apply_theme(fig, height=290)
        return fig

    def supplier_quality_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "supplier_name", "tier"]], on="supplier_id")
        grouped = merged.groupby("supplier_name").agg(
            quality=("quality_score", "mean"), orders=("procurement_id", "count")
        ).reset_index().nlargest(10, "orders")
        grouped["short"] = grouped["supplier_name"].str[:22]
        fig = px.bar(grouped, x="short", y="quality", color="quality",
                     color_continuous_scale=[
                         [0, DANGER], [0.6, WARNING], [1, SUCCESS]],
                     text=grouped["quality"].map(lambda x: f"{x:.1f}"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=10))
        fig.update_coloraxes(showscale=False)
        fig.update_layout(yaxis=dict(range=[80, 100]))
        apply_theme(fig, height=310)
        return fig

    def supplier_spend_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "supplier_name", "tier"]], on="supplier_id")
        grouped = merged.groupby(["supplier_name", "tier"])[
            "total_cost"].sum().reset_index().nlargest(8, "total_cost")
        grouped["short"] = grouped["supplier_name"].str[:20]
        fig = px.bar(grouped, x="total_cost", y="short", color="tier",
                     orientation="h", color_discrete_sequence=CHART_COLORS)
        apply_theme(fig, height=310)
        return fig

    def lead_time_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "supplier_name", "country"]], on="supplier_id")
        grouped = merged.groupby("country")[
            "lead_time_days"].mean().reset_index()
        fig = px.bar(grouped, x="country", y="lead_time_days",
                     color="lead_time_days",
                     color_continuous_scale=[[0, SUCCESS], [0.5, WARNING], [1, DANGER]])
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=280)
        return fig

    def supplier_tier_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "tier"]], on="supplier_id")
        grouped = merged.groupby("tier")["total_cost"].sum().reset_index()
        fig = px.pie(grouped, names="tier", values="total_cost",
                     color_discrete_sequence=CHART_COLORS, hole=0.5)
        fig.update_traces(marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=280)
        return fig

    # Procurement trend over time
    def procurement_trend_chart(self):
        merged = self.f_procurement.merge(self.dim_date[["date_key", "year", "month", "month_name"]],
                                          left_on="order_date_key", right_on="date_key")
        grouped = merged.groupby(["year", "month", "month_name"]).agg(
            spend=("total_cost", "sum"), orders=("procurement_id", "count")
        ).reset_index().sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grouped["period"], y=grouped["spend"],
                                 fill="tozeroy", fillcolor="rgba(0,180,216,0.15)",
                                 line=dict(color=ACCENT, width=2), name="Spend", mode="lines"))
        fig.add_trace(go.Scatter(x=grouped["period"], y=grouped["orders"],
                                 name="# Orders", yaxis="y2",
                                 line=dict(color=WARNING,
                                           width=1.5, dash="dot"),
                                 mode="lines+markers", marker=dict(size=4)))
        fig.update_layout(yaxis2=dict(
            overlaying="y", side="right",
            gridcolor="rgba(0,0,0,0)", tickfont=dict(color=WARNING, size=10)
        ))
        apply_theme(fig, height=300)
        return fig

    # Quality score distribution (box per supplier country)
    def quality_distribution_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "country"]], on="supplier_id")
        fig = px.box(merged, x="country", y="quality_score",
                     color="country", color_discrete_sequence=CHART_COLORS,
                     points="outliers")
        fig.update_layout(showlegend=False)
        apply_theme(fig, height=300)
        return fig

    # Supplier order count vs quality scatter
    def supplier_reliability_chart(self):
        merged = self.f_procurement.merge(
            self.dim_supplier[["supplier_id", "supplier_name", "tier"]], on="supplier_id")
        grouped = merged.groupby(["supplier_name", "tier"]).agg(
            orders=("procurement_id", "count"),
            quality=("quality_score", "mean"),
            spend=("total_cost", "sum")
        ).reset_index()
        grouped["short"] = grouped["supplier_name"].str[:18]
        fig = px.scatter(grouped, x="orders", y="quality", size="spend",
                         color="tier", text="short",
                         color_discrete_sequence=CHART_COLORS, size_max=40)
        fig.update_traces(textposition="top center",
                          textfont=dict(color=TEXT_LIGHT, size=8))
        apply_theme(fig, height=300)
        return fig

    def production_volume_chart(self):
        merged = self.f_production.merge(
            self.dim_date[["date_key", "year", "month", "month_name"]], on="date_key")
        grouped = merged.groupby(["year", "month", "month_name"]).agg(
            produced=("quantity_produced", "sum"), defective=("defective_units", "sum")
        ).reset_index().sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["period"], y=grouped["produced"],
                             name="Produced", marker_color=ACCENT, opacity=0.9))
        fig.add_trace(go.Bar(x=grouped["period"], y=grouped["defective"],
                             name="Defective", marker_color=DANGER, opacity=0.9))
        apply_theme(fig, height=310)
        return fig

    def defect_rate_chart(self):
        merged = self.f_production.merge(
            self.dim_facility[["facility_id", "facility_name"]], on="facility_id")
        grouped = merged.groupby("facility_name")[
            "defect_rate_pct"].mean().reset_index()
        grouped["short"] = grouped["facility_name"].str[:22]
        fig = px.bar(grouped, x="short", y="defect_rate_pct",
                     color="defect_rate_pct",
                     color_continuous_scale=[
                         [0, SUCCESS], [0.5, WARNING], [1, DANGER]],
                     text=grouped["defect_rate_pct"].map(lambda x: f"{x:.2f}%"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=310)
        return fig

    def facility_utilization_chart(self):
        merged = self.f_production.merge(self.dim_facility[[
                                         "facility_id", "facility_name", "annual_capacity"]], on="facility_id")
        grouped = merged.groupby(["facility_name", "annual_capacity"])[
            "quantity_produced"].sum().reset_index()
        grouped["utilization"] = grouped["quantity_produced"] / \
            grouped["annual_capacity"] * 100
        grouped["short"] = grouped["facility_name"].str[:20]
        fig = px.bar(grouped, x="short", y="utilization",
                     color="utilization",
                     color_continuous_scale=[[0, ACCENT], [0.7, SUCCESS], [1, WARNING]])
        fig.update_layout(yaxis_ticksuffix="%")
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    def product_production_chart(self):
        merged = self.f_production.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby("category")[
            "quantity_produced"].sum().reset_index()
        fig = px.pie(grouped, names="category", values="quantity_produced",
                     color_discrete_sequence=CHART_COLORS, hole=0.5)
        fig.update_traces(marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=290)
        return fig

    # Production yield rate by facility
    def yield_rate_chart(self):
        merged = self.f_production.merge(
            self.dim_facility[["facility_id", "facility_name"]], on="facility_id")
        grouped = merged.groupby("facility_name").agg(
            produced=("quantity_produced", "sum"),
            defective=("defective_units", "sum")
        ).reset_index()
        grouped["yield_rate"] = (
            grouped["produced"] - grouped["defective"]) / grouped["produced"] * 100
        grouped["short"] = grouped["facility_name"].str[:20]
        fig = px.bar(grouped, x="short", y="yield_rate",
                     color="yield_rate",
                     color_continuous_scale=[
                         [0, DANGER], [0.7, WARNING], [1, SUCCESS]],
                     text=grouped["yield_rate"].map(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_layout(yaxis=dict(range=[90, 101]), yaxis_ticksuffix="%")
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Production by product line over time
    def production_trend_by_line_chart(self):
        merged = self.f_production.merge(
            self.dim_date[["date_key", "year", "month", "month_name"]], on="date_key")
        merged = merged.merge(
            self.dim_product[["product_id", "product_line"]], on="product_id")
        grouped = merged.groupby(["year", "month", "month_name", "product_line"])[
            "quantity_produced"].sum().reset_index()
        grouped = grouped.sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = px.line(grouped, x="period", y="quantity_produced", color="product_line",
                      line_shape="spline", color_discrete_sequence=CHART_COLORS)
        fig.update_traces(line_width=2)
        apply_theme(fig, height=290)
        return fig

    # Defect units by product category
    def defect_by_category_chart(self):
        merged = self.f_production.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby("category").agg(
            produced=("quantity_produced", "sum"),
            defective=("defective_units", "sum")
        ).reset_index()
        grouped["defect_rate"] = grouped["defective"] / \
            grouped["produced"] * 100
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["category"], y=grouped["defective"],
                             name="Defective Units", marker_color=DANGER, opacity=0.85))
        fig.add_trace(go.Scatter(x=grouped["category"], y=grouped["defect_rate"],
                                 name="Defect Rate %", yaxis="y2",
                                 line=dict(color=WARNING, width=2),
                                 mode="lines+markers", marker=dict(size=7)))
        fig.update_layout(yaxis2=dict(
            overlaying="y", side="right", ticksuffix="%",
            gridcolor="rgba(0,0,0,0)", tickfont=dict(color=WARNING, size=10)
        ))
        apply_theme(fig, height=290)
        return fig

    def stock_level_chart(self):
        merged = self.f_inventory.merge(
            self.dim_date[["date_key", "year", "month", "month_name"]], on="date_key")
        merged = merged.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby(["year", "month", "month_name", "category"])[
            "stock_level"].mean().reset_index()
        grouped = grouped.sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = px.line(grouped, x="period", y="stock_level", color="category",
                      line_shape="spline", color_discrete_sequence=CHART_COLORS)
        fig.update_traces(line_width=2)
        apply_theme(fig, height=310)
        return fig

    def reorder_analysis_chart(self):
        merged = self.f_inventory.merge(
            self.dim_product[["product_id", "product_name", "category"]], on="product_id")
        merged["below_reorder"] = merged["stock_level"] < merged["reorder_point"]
        grouped = merged.groupby("category").agg(
            total=("inventory_id", "count"),
            below=("below_reorder", "sum")
        ).reset_index()
        grouped["above"] = grouped["total"] - grouped["below"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["category"], y=grouped["above"],
                             name="Above Reorder", marker_color=SUCCESS))
        fig.add_trace(go.Bar(x=grouped["category"], y=grouped["below"],
                             name="Below Reorder", marker_color=DANGER))
        fig.update_layout(barmode="stack")
        apply_theme(fig, height=310)
        return fig

    def safety_stock_chart(self):
        merged = self.f_inventory.merge(
            self.dim_facility[["facility_id", "facility_name"]], on="facility_id")
        grouped = merged.groupby("facility_name").agg(
            stock=("stock_level", "mean"), safety=("safety_stock_level", "mean")
        ).reset_index()
        grouped["short"] = grouped["facility_name"].str[:20]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["short"], y=grouped["stock"],
                             name="Avg Stock", marker_color=ACCENT))
        fig.add_trace(go.Bar(x=grouped["short"], y=grouped["safety"],
                             name="Safety Stock", marker_color=WARNING))
        fig.update_layout(barmode="group")
        apply_theme(fig, height=290)
        return fig

    def inventory_heatmap_chart(self):
        merged = self.f_inventory.merge(
            self.dim_date[["date_key", "year", "month_name"]], on="date_key")
        merged = merged.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby(["month_name", "category"])[
            "stock_level"].mean().unstack(fill_value=0)
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        grouped = grouped.reindex(
            [m for m in month_order if m in grouped.index])
        fig = px.imshow(grouped, color_continuous_scale=[[0, BG_DARK], [0.5, PRIMARY], [1, ACCENT]],
                        aspect="auto", text_auto=".0f")
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Stock coverage ratio (stock / safety stock)
    def stock_coverage_chart(self):
        merged = self.f_inventory.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby("category").agg(
            stock=("stock_level", "mean"),
            safety=("safety_stock_level", "mean"),
            reorder=("reorder_point", "mean")
        ).reset_index()
        grouped["coverage"] = grouped["stock"] / grouped["safety"]
        fig = px.bar(grouped, x="category", y="coverage",
                     color="coverage",
                     color_continuous_scale=[[0, DANGER], [1, SUCCESS]],
                     text=grouped["coverage"].map(lambda x: f"{x:.2f}x"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=10))
        fig.update_coloraxes(showscale=False)
        fig.add_hline(y=1.0, line_dash="dash", line_color=WARNING,
                      annotation_text="Safety threshold", annotation_font_color=WARNING)
        apply_theme(fig, height=290)
        return fig

    # Inventory turnover proxy (facility level)
    def inventory_turnover_chart(self):
        inv_merged = self.f_inventory.merge(
            self.dim_facility[["facility_id", "facility_name"]], on="facility_id")
        sales_merged = self.f_sales.merge(
            self.dim_product[["product_id"]], on="product_id")
        avg_stock = inv_merged.groupby("facility_name")[
            "stock_level"].mean().reset_index()
        avg_stock.columns = ["facility_name", "avg_stock"]
        total_sold = sales_merged["quantity_sold"].sum()
        avg_stock["turnover"] = total_sold / \
            avg_stock["avg_stock"].replace(0, 1)
        avg_stock["short"] = avg_stock["facility_name"].str[:20]
        fig = px.bar(avg_stock, x="short", y="turnover",
                     color="turnover",
                     color_continuous_scale=[[0, PRIMARY], [1, ACCENT]],
                     text=avg_stock["turnover"].map(lambda x: f"{x:.1f}x"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Stock distribution across facilities (treemap)
    def stock_treemap_chart(self):
        merged = self.f_inventory.merge(
            self.dim_facility[["facility_id", "facility_name"]], on="facility_id")
        merged = merged.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby(["facility_name", "category"])[
            "stock_level"].sum().reset_index()
        grouped["short"] = grouped["facility_name"].str[:18]
        fig = px.treemap(grouped, path=["short", "category"], values="stock_level",
                         color="stock_level",
                         color_continuous_scale=[[0, PRIMARY], [0.5, ACCENT], [1, SUCCESS]])
        fig.update_coloraxes(showscale=False)
        fig.update_traces(textfont=dict(color="white", size=11))
        apply_theme(fig, height=300)
        return fig

    def shipment_status_chart(self):
        if self.f_shipment.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No shipment data for current filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(color=TEXT_MUTED, size=13)
            )
            apply_theme(fig, height=300)
            return fig

        grouped = self.f_shipment.groupby(
            "status")["shipment_id"].count().reset_index()
        grouped.columns = ["status", "count"]
        fig = px.pie(grouped, names="status", values="count",
                     color_discrete_sequence=CHART_COLORS, hole=0.55)
        fig.update_traces(marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=300)
        return fig

    def carrier_performance_chart(self):
        grouped = self.f_shipment.groupby("carrier").agg(
            shipments=("shipment_id", "count"),
            avg_cost=("shipping_cost", "mean")
        ).reset_index()
        fig = px.scatter(grouped, x="shipments", y="avg_cost", size="shipments",
                         color="avg_cost", text="carrier",
                         color_continuous_scale=[[0, SUCCESS], [1, DANGER]])
        fig.update_traces(textposition="top center",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=300)
        return fig

    def shipment_volume_chart(self):
        merged = self.f_shipment.merge(self.dim_date[["date_key", "year", "month", "month_name"]],
                                       left_on="ship_date_key", right_on="date_key")
        grouped = merged.groupby(["year", "month", "month_name"])[
            "quantity"].sum().reset_index()
        grouped = grouped.sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = px.area(grouped, x="period", y="quantity",
                      color_discrete_sequence=[ACCENT])
        fig.update_traces(
            fill="tozeroy", fillcolor=f"rgba(0,180,216,0.15)", line_width=2)
        apply_theme(fig, height=290)
        return fig

    def shipping_cost_chart(self):
        grouped = self.f_shipment.groupby("carrier").agg(
            total_cost=("shipping_cost", "sum"),
            shipments=("shipment_id", "count")
        ).reset_index()
        grouped["cost_per_shipment"] = grouped["total_cost"] / \
            grouped["shipments"]
        fig = px.bar(grouped, x="carrier", y="cost_per_shipment",
                     color="cost_per_shipment",
                     color_continuous_scale=[
                         [0, SUCCESS], [0.5, WARNING], [1, DANGER]],
                     text=grouped["cost_per_shipment"].map(lambda x: f"${x:,.0f}"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Shipment delay reasons
    def delay_reason_chart(self):
        delayed = self.f_shipment[self.f_shipment["delay_reason"].notna() & (
            self.f_shipment["delay_reason"].str.strip() != "")]
        if delayed.empty:
            fig = go.Figure()
            fig.add_annotation(text="No delay data available", xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False, font=dict(color=TEXT_MUTED, size=13))
            apply_theme(fig, height=290)
            return fig
        grouped = delayed.groupby("delay_reason")[
            "shipment_id"].count().reset_index()
        grouped.columns = ["reason", "count"]
        fig = px.pie(grouped, names="reason", values="count",
                     color_discrete_sequence=CHART_COLORS, hole=0.5)
        fig.update_traces(marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=290)
        return fig

    # Total weight shipped per carrier
    def carrier_weight_chart(self):
        grouped = self.f_shipment.groupby("carrier").agg(
            total_weight=("total_weight_kg", "sum"),
            shipments=("shipment_id", "count")
        ).reset_index()
        grouped["avg_weight"] = grouped["total_weight"] / grouped["shipments"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=grouped["carrier"], y=grouped["total_weight"],
                             name="Total Weight (kg)", marker_color=ACCENT, opacity=0.85))
        fig.add_trace(go.Scatter(x=grouped["carrier"], y=grouped["avg_weight"],
                                 name="Avg per Shipment", yaxis="y2",
                                 line=dict(color=WARNING, width=2),
                                 mode="lines+markers", marker=dict(size=7)))
        fig.update_layout(yaxis2=dict(
            overlaying="y", side="right",
            gridcolor="rgba(0,0,0,0)", tickfont=dict(color=WARNING, size=10)
        ))
        apply_theme(fig, height=290)
        return fig

    # Shipment volume by destination country
    def shipment_by_country_chart(self):
        merged = self.f_shipment.merge(
            self.dim_customer[["customer_id", "country"]], on="customer_id")
        grouped = merged.groupby("country").agg(
            shipments=("shipment_id", "count"),
            quantity=("quantity", "sum")
        ).reset_index().sort_values("quantity", ascending=False)
        fig = px.bar(grouped, x="country", y="quantity",
                     color="quantity", color_continuous_scale=[[0, PRIMARY], [1, ACCENT]],
                     text=grouped["quantity"].map(lambda x: f"{x:,}"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    def sales_trend_chart(self):
        merged = self.f_sales.merge(
            self.dim_date[["date_key", "year", "month", "month_name"]], on="date_key")
        grouped = merged.groupby(["year", "month", "month_name"]).agg(
            revenue=("net_revenue", "sum"), orders=("order_number", "nunique")
        ).reset_index().sort_values(["year", "month"])
        grouped["period"] = grouped["month_name"].str[:3] + \
            " " + grouped["year"].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grouped["period"], y=grouped["revenue"],
                                 fill="tozeroy", fillcolor=f"rgba(0,180,216,0.12)",
                                 line=dict(color=ACCENT, width=2.5),
                                 name="Revenue", mode="lines"))
        fig.add_trace(go.Bar(x=grouped["period"], y=grouped["orders"],
                             name="Orders", marker_color=WARNING, opacity=0.5,
                             yaxis="y2"))
        fig.update_layout(yaxis2=dict(
            overlaying="y", side="right",
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color=WARNING, size=10)
        ))
        apply_theme(fig, height=310)
        return fig

    def sales_by_channel_chart(self):
        merged = self.f_sales.merge(
            self.dim_customer[["customer_id", "channel_type"]], on="customer_id")
        grouped = merged.groupby("channel_type")[
            "net_revenue"].sum().reset_index()
        fig = px.pie(grouped, names="channel_type", values="net_revenue",
                     color_discrete_sequence=CHART_COLORS, hole=0.5)
        fig.update_traces(marker=dict(line=dict(color=BG_DARK, width=2)))
        apply_theme(fig, height=300)
        return fig

    def discount_impact_chart(self):
        merged = self.f_sales.merge(
            self.dim_product[["product_id", "category"]], on="product_id")
        grouped = merged.groupby("category").agg(
            avg_discount=("discount_pct", "mean"),
            avg_margin=("profit_margin_pct", "mean"),
            revenue=("net_revenue", "sum")
        ).reset_index()
        fig = px.scatter(grouped, x="avg_discount", y="avg_margin",
                         size="revenue", color="category",
                         color_discrete_sequence=CHART_COLORS, text="category",
                         size_max=45)
        fig.update_traces(textposition="top center",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        apply_theme(fig, height=300)
        return fig

    def top_products_chart(self):
        merged = self.f_sales.merge(
            self.dim_product[["product_id", "product_name"]], on="product_id")
        grouped = merged.groupby("product_name")[
            "net_revenue"].sum().nlargest(8).reset_index()
        grouped["short"] = grouped["product_name"].str[:28]
        fig = px.bar(grouped, x="net_revenue", y="short", orientation="h",
                     color="net_revenue",
                     color_continuous_scale=[[0, PRIMARY], [1, ACCENT]])
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Avg order value by customer country
    def avg_order_value_chart(self):
        merged = self.f_sales.merge(
            self.dim_customer[["customer_id", "country"]], on="customer_id")
        grouped = merged.groupby("country").agg(
            revenue=("net_revenue", "sum"),
            orders=("order_number", "nunique")
        ).reset_index()
        grouped["aov"] = grouped["revenue"] / grouped["orders"]
        grouped = grouped.sort_values("aov", ascending=False)
        fig = px.bar(grouped, x="country", y="aov",
                     color="aov", color_continuous_scale=[[0, PRIMARY], [1, SUCCESS]],
                     text=grouped["aov"].map(self.fmt_currency))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=10))
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=290)
        return fig

    # Quantity sold by product spec
    def quantity_by_spec_chart(self):
        merged = self.f_sales.merge(
            self.dim_product[["product_id", "spec", "category"]], on="product_id")
        grouped = merged.groupby(["spec", "category"])[
            "quantity_sold"].sum().reset_index()
        grouped = grouped.sort_values(
            "quantity_sold", ascending=False).head(12)
        fig = px.bar(grouped, x="spec", y="quantity_sold", color="category",
                     color_discrete_sequence=CHART_COLORS,
                     text=grouped["quantity_sold"].map(lambda x: f"{x:,}"))
        fig.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_LIGHT, size=9))
        apply_theme(fig, height=290)
        return fig

    # Revenue & units heatmap (product line × month)
    def revenue_heatmap_chart(self):
        merged = self.f_sales.merge(
            self.dim_date[["date_key", "month_name"]], on="date_key")
        merged = merged.merge(
            self.dim_product[["product_id", "product_line"]], on="product_id")
        grouped = merged.groupby(["month_name", "product_line"])[
            "net_revenue"].sum().unstack(fill_value=0)
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        grouped = grouped.reindex(
            [m for m in month_order if m in grouped.index])
        fig = px.imshow(grouped, color_continuous_scale=[[0, BG_DARK], [0.5, PRIMARY], [1, ACCENT]],
                        aspect="auto", text_auto=False)
        fig.update_coloraxes(showscale=False)
        apply_theme(fig, height=300)
        return fig
