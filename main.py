import streamlit as st
import pandas as pd

from components.data import Chart, chart_card

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Sora', sans-serif;
      background-color: {BG_DARK};
      color: {TEXT_LIGHT};
  }}
 .block-container {{ padding: 3.5rem 2rem 2rem 2rem; }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
      background: linear-gradient(160deg, #0D1B2A 0%, #1A2744 100%);
      border-right: 1px solid #1E3A5F;
  }}
  section[data-testid="stSidebar"] .stMultiSelect label,
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] p {{
      color: {TEXT_LIGHT} !important;
      font-size: 0.82rem;
  }}

  /* Header banner */
  .header-banner {{
      background: linear-gradient(135deg, {PRIMARY} 0%, #1A3A6E 50%, #0A2540 100%);
      border-radius: 14px;
      padding: 1.4rem 2rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 1rem;
      border: 1px solid #1E4080;
      box-shadow: 0 8px 32px rgba(0,180,216,0.12);
  }}
  .header-title {{
      font-size: 2rem;
      font-weight: 700;
      color: white;
      letter-spacing: -0.02em;
      line-height: 1.1;
  }}
  .header-subtitle {{
      font-size: 0.82rem;
      color: {ACCENT};
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-top: 0.25rem;
  }}

  /* KPI cards */
  .kpi-grid {{ display: flex; gap: 0.9rem; flex-wrap: wrap; margin-bottom: 1.4rem; }}
  .kpi-card {{
      background: linear-gradient(135deg, {BG_CARD} 0%, #0F2235 100%);
      border: 1px solid #1E3A5F;
      border-radius: 12px;
      padding: 1rem 1.25rem;
      flex: 1;
      min-width: 145px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }}
  .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      border-radius: 12px 12px 0 0;
  }}
  .kpi-card.blue::before   {{ background: {ACCENT}; }}
  .kpi-card.green::before  {{ background: {SUCCESS}; }}
  .kpi-card.yellow::before {{ background: {WARNING}; }}
  .kpi-card.red::before    {{ background: {DANGER}; }}
  .kpi-card.purple::before {{ background: #9B5DE5; }}
  .kpi-card.teal::before   {{ background: #06D6A0; }}
  .kpi-card.orange::before {{ background: #FF6B35; }}

  .kpi-icon  {{ font-size: 1.4rem; margin-bottom: 0.35rem; }}
  .kpi-label {{
      font-size: 0.7rem;
      color: {TEXT_MUTED};
      text-transform: uppercase;
      letter-spacing: 0.07em;
      font-family: 'JetBrains Mono', monospace;
  }}
  .kpi-value {{
      font-size: 1.45rem;
      font-weight: 700;
      color: white;
      line-height: 1.2;
      margin-top: 0.1rem;
  }}
  .kpi-delta {{
      font-size: 0.72rem;
      margin-top: 0.2rem;
      font-family: 'JetBrains Mono', monospace;
  }}
  .delta-up   {{ color: {SUCCESS}; }}
  .delta-down {{ color: {DANGER}; }}

  /* Section heading */
  .section-title {{
      font-size: 0.72rem;
      font-family: 'JetBrains Mono', monospace;
      color: {ACCENT};
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin: 0.2rem 0 1rem 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
  }}
  .section-title::after {{
      content: '';
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, #1E3A5F, transparent);
  }}

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {{
      background: {BG_CARD};
      border-radius: 10px;
      padding: 0.3rem;
      gap: 0.2rem;
      border: 1px solid #1E3A5F;
  }}
  .stTabs [data-baseweb="tab"] {{
      border-radius: 8px;
      color: {TEXT_MUTED};
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.45rem 0.9rem;
      letter-spacing: 0.02em;
  }}
  .stTabs [aria-selected="true"] {{
      background: linear-gradient(135deg, {PRIMARY}, #0A2D5E) !important;
      color: white !important;
      box-shadow: 0 2px 12px rgba(0,180,216,0.25);
  }}
  .stTabs [data-baseweb="tab-panel"] {{
      padding: 1.2rem 0 0 0;
  }}

  /* Chart cards */
  .chart-wrap {{
      background: linear-gradient(135deg, {BG_CARD} 0%, #0F2235 100%);
      border: 1px solid #1E3A5F;
      border-radius: 12px;
      padding: 1.1rem 1.2rem;
      margin-bottom: 1rem;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  }}
  .chart-title {{
      font-size: 0.78rem;
      font-family: 'JetBrains Mono', monospace;
      color: {TEXT_MUTED};
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0.6rem;
  }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
  ::-webkit-scrollbar-track {{ background: {BG_DARK}; }}
  ::-webkit-scrollbar-thumb {{ background: #1E3A5F; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)

datasets = {
    'sales': 'data/fact_sales.csv',
    'inventory': 'data/fact_inventory.csv',
    'procurement': 'data/fact_procurement.csv',
    'production': 'data/fact_production.csv',
    'shipment': 'data/fact_shipment.csv',
    'dim_date': 'data/dim_date.csv',
    'dim_product': 'data/dim_product.csv',
    'dim_supplier': 'data/dim_supplier.csv',
    'dim_customer': 'data/dim_customer.csv',
    'dim_facility': 'data/dim_facility.csv',
}
c = Chart(datasets)

with st.sidebar:
    st.sidebar.markdown("""
<div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
  <span style='font-size:2rem;'>🔗</span><br>
  <span style='font-size:1rem; font-weight:700; color:white; letter-spacing:-0.01em;'>Supply Chain</span><br>
  <span style='font-size:0.68rem; color:#00B4D8; font-family:monospace; text-transform:uppercase; letter-spacing:0.1em;'>Analytics Platform</span>
</div>
<hr style='border-color:#1E3A5F; margin:0.8rem 0;'>
""", unsafe_allow_html=True)

    st.markdown("**📅 Year**")
    years = c.unique_values(c.dim_date, 'year')
    sel_years = st.multiselect(
        "Year", years, default=years, label_visibility="collapsed")

    st.markdown("**📦 Product Category**")
    categories = c.unique_values(c.dim_product, 'category')
    sel_cats = st.multiselect(
        "Category", categories, default=categories, label_visibility="collapsed")

    st.markdown("**🏭 Facility**")
    facilities = c.unique_values(c.dim_facility, 'facility_name')
    sel_facilities = st.multiselect(
        "Facility", facilities, default=facilities, label_visibility="collapsed")

    st.markdown("**🌐 Customer Country**")
    cust_countries = c.unique_values(c.dim_customer, 'country')
    sel_cust_countries = st.multiselect(
        "Customer Country", cust_countries, default=cust_countries, label_visibility="collapsed")

    st.markdown("**🏷️ Supplier Tier**")
    tiers = c.unique_values(c.dim_supplier, 'tier')
    sel_tiers = st.multiselect(
        "Supplier Tier", tiers, default=tiers, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:{BG_CARD}; border:1px solid #1E3A5F; border-radius:8px; padding:0.7rem; font-size:0.7rem; color:{TEXT_MUTED};'>
    💡 <b style='color:{ACCENT};'>Tip:</b> All filters apply globally across every tab.
    </div>
    """, unsafe_allow_html=True)

c.filters_df({
    "year": sel_years,
    "category": sel_cats,
    "facility_name": sel_facilities,
    "country": sel_cust_countries,
    "tier": sel_tiers,
})

st.markdown(f"""
<div class="header-banner">
  <span style='font-size:2.4rem;'>🔗</span>
  <div>
    <div class="header-title">Supply Chain</div>
    <div class="header-subtitle">⬡ Analytics Dashboard &nbsp;·&nbsp; Real-time Intelligence Platform</div>
  </div>
  <div style='margin-left:auto; text-align:right;'>
    <div style='font-size:0.68rem; color:{TEXT_MUTED}; font-family:monospace;'>DATA RANGE</div>
    <div style='font-size:0.88rem; color:{ACCENT}; font-weight:600; font-family:monospace;'>
      {", ".join(str(y) for y in sorted(sel_years)) if sel_years else "—"}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

kpis = c.compute_kpis()

kpi_cols = st.columns(8, gap="small")
kpi_data = [
    ("💰", "Total Revenue", c.fmt_currency(
        kpis['total_revenue']), "blue", "Net of discounts"),
    ("📈", "Total Profit", c.fmt_currency(
        kpis['total_profit']), "green", "Gross profit"),
    ("🎯", "Profit Margin", f"{kpis['profit_margin']:.1f}%",
     "teal",   f"Cost ratio {kpis['cost_ratio']:.1f}%"),
    ("⚖️", "Cost Ratio", f"{kpis['cost_ratio']:.1f}%",
     "yellow", "COGS / Revenue"),
    ("✅", "Perfect Order Rate", f"{kpis['perfect_order_rate']:.1f}%",
     "green",  f"{kpis['delivered_ship']:,} delivered"),
    ("🔄", "Cash Cycle Days", f"{kpis['cash_cycle_days']:.1f}d",
     "purple", f"Avg lead {kpis['avg_lead_time']:.0f}d"),
    ("🏷️", "Discount Rate",
     f"{kpis['avg_discount']:.2f}%",  "orange", "Avg order discount"),
    ("🛒", "Total Orders", f"{kpis['total_orders']:,}",
     "blue", f"{len(c.f_sales):,} line items"),
]

for col, (icon, label, value, color_key, delta) in zip(kpi_cols, kpi_data):
    c.render_kpi_card(col, icon, label, value, color_key, delta)

st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Performance Modules</div>',
            unsafe_allow_html=True)

tab_exec, tab_supplier, tab_production, tab_inventory, tab_shipment, tab_sales = st.tabs([
    "🏢  Executive",
    "🤝  Supplier",
    "🏭  Production",
    "📦  Inventory",
    "🚚  Shipment",
    "💵  Sales",
])


with tab_exec:
    c1, c2 = st.columns([2, 1])

    with c1:
        chart_card(c.revenue_trend_chart(),
                   "📈 Revenue & Profit Trend (Monthly)")
    with c2:
        chart_card(c.revenue_category_chart(), "🗂️ Revenue Mix by Category")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.top_customers_chart(), "🏆 Top 8 Customers by Revenue")
    with c4:
        chart_card(c.margin_product_chart(), "🎯 Profit Margin by Product Line")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.revenue_by_country_chart(),
                   "🌍 Revenue by Customer Country")
    with c6:
        chart_card(c.yoy_revenue_chart(),
                   "📅 Year-over-Year Revenue Comparison")

    chart_card(c.customer_size_chart(), "🏢 Revenue by Customer Size Segment")

with tab_supplier:
    c1, c2 = st.columns(2)
    with c1:
        chart_card(c.supplier_quality_chart(),
                   "⭐ Average Quality Score by Supplier")
    with c2:
        chart_card(c.supplier_spend_chart(),
                   "💸 Procurement Spend by Supplier")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.lead_time_chart(),
                   "⏱️ Avg Lead Time by Supplier Country")
    with c4:
        chart_card(c.supplier_tier_chart(),   "🏷️ Spend Distribution by Tier")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.procurement_trend_chart(),
                   "📅 Monthly Procurement Spend & Orders")
    with c6:
        chart_card(c.quality_distribution_chart(),
                   "📦 Quality Score Distribution by Country")

    chart_card(c.supplier_reliability_chart(),
               "🎯 Supplier Reliability: Orders vs Quality (bubble = spend)")

with tab_production:
    c1, c2 = st.columns(2)
    with c1:
        chart_card(c.production_volume_chart(),
                   "🏭 Monthly Production Volume vs Defects")
    with c2:
        chart_card(c.defect_rate_chart(),
                   "⚠️ Avg Defect Rate by Facility")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.facility_utilization_chart(),
                   "📊 Facility Capacity Utilization")
    with c4:
        chart_card(c.product_production_chart(),   "📦 Production by Category")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.yield_rate_chart(),
                   "✅ Production Yield Rate by Facility")
    with c6:
        chart_card(c.defect_by_category_chart(),
                   "🔬 Defective Units & Rate by Category")

    chart_card(c.production_trend_by_line_chart(),
               "📈 Monthly Production Trend by Product Line")

with tab_inventory:
    c1, c2 = st.columns(2)
    with c1:
        chart_card(c.stock_level_chart(),
                   "📈 Stock Level Trend by Category")
    with c2:
        chart_card(c.reorder_analysis_chart(),
                   "🔔 Reorder Point Analysis by Category")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.safety_stock_chart(),
                   "🛡️ Stock vs Safety Stock by Facility")
    with c4:
        chart_card(c.inventory_heatmap_chart(),
                   "🗓️ Avg Stock Heatmap (Month × Category)")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.stock_coverage_chart(),
                   "📐 Stock Coverage Ratio by Category")
    with c6:
        chart_card(c.inventory_turnover_chart(),
                   "🔄 Inventory Turnover by Facility")

    chart_card(c.stock_treemap_chart(),
               "🗂️ Stock Distribution: Facility → Category (Treemap)")

with tab_shipment:
    c1, c2 = st.columns(2)
    with c1:
        chart_card(c.shipment_status_chart(),
                   "📋 Shipment Status Distribution")
    with c2:
        chart_card(c.carrier_performance_chart(),
                   "🚢 Carrier: Volume vs Avg Cost")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.shipment_volume_chart(),    "📦 Monthly Shipment Volume")
    with c4:
        chart_card(c.shipping_cost_chart(),
                   "💲 Avg Shipping Cost per Shipment by Carrier")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.carrier_weight_chart(),
                   "⚖️ Total & Avg Weight Shipped by Carrier")
    with c6:
        chart_card(c.delay_reason_chart(),       "⏰ Shipment Delay Reasons")

    chart_card(c.shipment_by_country_chart(),
               "🌍 Shipment Quantity by Destination Country")

with tab_sales:
    c1, c2 = st.columns([3, 1])
    with c1:
        chart_card(c.sales_trend_chart(),
                   "📅 Revenue Trend & Order Volume")
    with c2:
        chart_card(c.sales_by_channel_chart(), "🛍️ Sales by Channel")

    c3, c4 = st.columns(2)
    with c3:
        chart_card(c.discount_impact_chart(),
                   "🏷️ Discount Rate vs Profit Margin Bubble")
    with c4:
        chart_card(c.top_products_chart(),     "🥇 Top 8 Products by Revenue")

    c5, c6 = st.columns(2)
    with c5:
        chart_card(c.avg_order_value_chart(),
                   "💳 Avg Order Value by Customer Country")
    with c6:
        chart_card(c.quantity_by_spec_chart(), "📱 Units Sold by Product Spec")

    chart_card(c.revenue_heatmap_chart(),
               "🗓️ Revenue Heatmap (Month × Product Line)")
