# 🔗 Supply Chain Analytics Dashboard

> A comprehensive, interactive analytics platform for end-to-end supply chain visibility — covering executive performance, supplier relationships, production operations, inventory health, shipment logistics, and sales outcomes.

---

## Overview

The **Supply Chain Analytics Dashboard** is a Streamlit-based business intelligence tool designed to give supply chain managers, analysts, and executives a unified view of operations across the entire supply chain lifecycle. It consolidates data from procurement through to final customer delivery, enabling data-driven decisions at every level of the organization.

The dashboard is built around a **star schema data model** — fact tables that record transactional events joined to dimension tables that provide descriptive context. All views are driven by the same filtered data state, meaning every chart across every tab responds consistently to the sidebar filters applied by the user.

---

## Data Model

The dashboard is powered by ten source datasets — five fact tables and five dimension tables.

### Fact Tables

| Table              | Description                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `fact_sales`       | Individual sales line items including revenue, cost, profit, discount, and order references |
| `fact_procurement` | Purchase orders placed with suppliers including cost, lead time, and quality scores         |
| `fact_production`  | Production batch records per facility including units produced and defect counts            |
| `fact_inventory`   | Point-in-time stock level snapshots per product and facility                                |
| `fact_shipment`    | Outbound shipment records including carrier, status, weight, and shipping cost              |

### Dimension Tables

| Table          | Description                                                                                |
| -------------- | ------------------------------------------------------------------------------------------ |
| `dim_date`     | Calendar dimension with year, quarter, month, week, and day attributes                     |
| `dim_product`  | Product master including category, product line, spec, color, price, and cost              |
| `dim_supplier` | Supplier master including country, city, specialty, tier classification, and quality score |
| `dim_customer` | Customer master including country, channel type, and size classification                   |
| `dim_facility` | Facility master including location, facility type, specialization, and annual capacity     |

---

## Global KPI Bar

At the top of every page, above the tabs, eight headline KPIs summarize the overall health of the supply chain for the current filter selection. These metrics are always visible regardless of which tab is active.

| KPI                       | Definition                                            | Purpose                                                                                   |
| ------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **💰 Total Revenue**      | Sum of net revenue across all filtered sales          | Top-line performance indicator; reflects actual revenue after discounts                   |
| **📈 Total Profit**       | Sum of gross profit across all filtered sales         | Measures absolute profitability of the selected scope                                     |
| **🎯 Profit Margin**      | Total profit ÷ total revenue × 100                    | Efficiency of converting revenue into profit; higher is better                            |
| **⚖️ Cost Ratio**         | Total cost of goods sold ÷ total revenue × 100        | Proportion of revenue consumed by direct costs; lower is better                           |
| **✅ Perfect Order Rate** | Delivered shipments ÷ total shipments × 100           | Fulfillment reliability; measures the share of orders reaching the customer without issue |
| **🔄 Cash Cycle Days**    | Average supplier lead time + 30 days payable estimate | Proxy for working capital efficiency; shorter cycles free up cash faster                  |
| **🏷️ Discount Rate**      | Average discount percentage across all sales orders   | Reveals pricing pressure and promotional intensity                                        |
| **🛒 Total Orders**       | Count of unique order numbers in filtered sales       | Volume indicator; useful for contextualizing revenue and margin figures                   |

---

## Sidebar Filters

The sidebar provides five multi-select filters. All filters default to **all values selected** and apply globally across every tab simultaneously.

| Filter               | Dimension                    | Effect                                                                   |
| -------------------- | ---------------------------- | ------------------------------------------------------------------------ |
| **Year**             | `dim_date.year`              | Restricts all fact data to the selected calendar years                   |
| **Product Category** | `dim_product.category`       | Limits data to products belonging to the selected categories             |
| **Facility**         | `dim_facility.facility_name` | Scopes production, inventory, and shipment data to selected facilities   |
| **Customer Country** | `dim_customer.country`       | Filters sales and shipment data to customers in the selected countries   |
| **Supplier Tier**    | `dim_supplier.tier`          | Limits procurement data to suppliers of the selected tier classification |

Narrowing filters may result in some charts showing no data. In those cases the chart displays a neutral "no data for current filters" message.

---

## Tabs & Charts

### 🏢 Executive

**Purpose:** High-level view of overall business performance. Designed for senior leadership and general management to assess revenue health, profitability trends, and customer contribution without needing to drill into operational detail.

---

#### 📈 Revenue & Profit Trend (Monthly)

**Chart type:** Overlapping bar + line (dual axis)

Plots monthly net revenue and gross profit as overlapping bars, with profit margin percentage overlaid as a line on the secondary axis. This allows readers to spot months where revenue grew but margin compressed — a common early warning sign of pricing or cost pressure.

---

#### 🗂️ Revenue Mix by Category

**Chart type:** Donut pie

Shows the proportional contribution of each product category to total net revenue. Useful for understanding portfolio concentration and identifying whether the business is over-reliant on a single category.

---

#### 🏆 Top 8 Customers by Revenue

**Chart type:** Horizontal bar

Ranks the top eight customers by net revenue, sorted descending. Highlights key account concentration and supports account management prioritization.

---

#### 🎯 Profit Margin by Product Line

**Chart type:** Vertical bar (color-scaled)

Displays the calculated profit margin percentage for each product line. Color gradient moves from red (low margin) to green (high margin), making underperforming lines immediately visible.

---

#### 🌍 Revenue by Customer Country

**Chart type:** Vertical bar (color-scaled)

Breaks down net revenue by the country of the purchasing customer. Helps identify which geographies are the strongest revenue contributors and where growth opportunities or dependence risks exist.

---

#### 📅 Year-over-Year Revenue Comparison

**Chart type:** Multi-line chart

Plots monthly revenue for each available year as separate lines on the same axis. Enables direct seasonal comparison across years to identify growth, decline, or shifting demand patterns month by month.

---

#### 🏢 Revenue by Customer Size Segment

**Chart type:** Vertical bar (color by segment)

Aggregates net revenue by customer size classification (e.g. Large, Medium, Small). Useful for understanding which customer segments drive the most value and informing go-to-market strategy.

---

### 🤝 Supplier

**Purpose:** Evaluates supplier performance, procurement spend, and reliability. Supports procurement teams and supply chain managers in managing vendor relationships, identifying quality risks, and optimizing sourcing decisions.

---

#### ⭐ Average Quality Score by Supplier

**Chart type:** Vertical bar (color-scaled)

Shows the mean quality score recorded across all procurement orders for the top ten suppliers by order volume. Color ranges from red (low quality) to green (high quality), with the y-axis anchored near 80 to amplify differences between suppliers.

---

#### 💸 Procurement Spend by Supplier

**Chart type:** Horizontal bar (colored by tier)

Ranks the top eight suppliers by total procurement spend, with bars colored by supplier tier. Reveals spend concentration and whether high-spend suppliers align with the expected tier classification.

---

#### ⏱️ Avg Lead Time by Supplier Country

**Chart type:** Vertical bar (color-scaled)

Displays the average lead time in days aggregated by the supplier's country of origin. Color moves from green (fast) to red (slow), helping identify geographic sourcing risks and informing safety stock decisions.

---

#### 🏷️ Spend Distribution by Tier

**Chart type:** Donut pie

Shows the proportion of total procurement spend allocated to each supplier tier. A healthy supply chain typically maintains a balance between premium Tier 1 reliability and cost-effective lower-tier sourcing.

---

#### 📅 Monthly Procurement Spend & Orders

**Chart type:** Area + dotted line (dual axis)

Tracks total monthly procurement spend as a filled area chart, with the number of purchase orders overlaid as a dotted line on the secondary axis. Useful for identifying procurement seasonality, bulk buying patterns, or unusual spend spikes.

---

#### 📦 Quality Score Distribution by Country

**Chart type:** Box plot

Visualizes the spread and distribution of quality scores across all procurement orders, grouped by supplier country. Outliers are shown individually, making it easy to identify countries with consistently high variance or poor floor quality.

---

#### 🎯 Supplier Reliability: Orders vs Quality

**Chart type:** Bubble scatter

Each bubble represents a supplier, positioned by order count (x-axis) and average quality score (y-axis), with bubble size encoding total spend. High-volume, high-quality, high-spend suppliers in the upper-right represent strategic partners. Low-quality suppliers with high spend are flagged as risk concentrations.

---

### 🏭 Production

**Purpose:** Monitors manufacturing operations across facilities. Enables operations managers to track output volumes, identify quality issues, assess facility efficiency, and understand production mix by product line.

---

#### 🏭 Monthly Production Volume vs Defects

**Chart type:** Grouped bar

Shows total units produced and defective units side by side for each month. Provides an immediate visual of whether defect counts are growing in proportion to output or staying flat.

---

#### ⚠️ Avg Defect Rate by Facility

**Chart type:** Vertical bar (color-scaled)

Displays the mean defect rate percentage per facility, color-coded from green (low defects) to red (high defects). Directly surfaces which facilities have quality control concerns that require investigation.

---

#### 📊 Facility Capacity Utilization

**Chart type:** Vertical bar (color-scaled)

Calculates each facility's total units produced as a percentage of its annual capacity, then plots this utilization rate per facility. Identifies both over-stressed facilities approaching capacity limits and underutilized facilities that could absorb more production.

---

#### 📦 Production by Category

**Chart type:** Donut pie

Shows the share of total units produced attributed to each product category. Useful for understanding manufacturing portfolio mix and whether production allocation matches demand signals from the sales tab.

---

#### ✅ Production Yield Rate by Facility

**Chart type:** Vertical bar (color-scaled)

Calculates yield rate as `(units produced − defective units) ÷ units produced × 100` per facility. The y-axis is anchored near 90% to amplify differences. Facilities below 95% yield warrant process review.

---

#### 🔬 Defective Units & Rate by Category

**Chart type:** Bar + line (dual axis)

Plots total defective unit counts as bars and defect rate percentage as a line overlay per product category. Separating volume from rate helps distinguish whether a category has high defects because of scale or because of a genuine quality problem.

---

#### 📈 Monthly Production Trend by Product Line

**Chart type:** Multi-line (spline)

Tracks monthly production volume for each product line as separate smoothed lines. Useful for spotting production ramp-ups, seasonal patterns, or line-specific disruptions over time.

---

### 📦 Inventory

**Purpose:** Provides visibility into stock positions, reorder health, and inventory efficiency across products and facilities. Supports inventory planners and warehouse managers in preventing stockouts, identifying excess inventory, and maintaining appropriate safety buffers.

---

#### 📈 Stock Level Trend by Category

**Chart type:** Multi-line (spline)

Plots average stock levels over time for each product category. Enables planners to see whether inventory is being built up, drawn down, or holding steady across categories, and to detect seasonal replenishment cycles.

---

#### 🔔 Reorder Point Analysis by Category

**Chart type:** Stacked bar

For each category, shows the count of inventory records where stock is above the reorder point (green) versus below it (red). A high proportion of "below reorder" records signals stockout risk for that category.

---

#### 🛡️ Stock vs Safety Stock by Facility

**Chart type:** Grouped bar

Compares average actual stock level against average safety stock level side by side for each facility. Any facility where actual stock consistently falls below its safety stock threshold is at risk of not absorbing demand variability.

---

#### 🗓️ Avg Stock Heatmap (Month × Category)

**Chart type:** Heatmap

A grid where rows are calendar months and columns are product categories. Cell color encodes average stock level — darker cells indicate higher stock. Reveals seasonal stocking patterns and which categories accumulate inventory in specific months.

---

#### 📐 Stock Coverage Ratio by Category

**Chart type:** Vertical bar (color-scaled) with threshold line

Calculates the ratio of average stock to average safety stock per category. A ratio above 1.0 (marked by a dashed warning line) means the category is adequately covered. Ratios below 1.0 represent categories where stock has fallen below the safety buffer.

---

#### 🔄 Inventory Turnover by Facility

**Chart type:** Vertical bar (color-scaled)

Estimates inventory turnover by dividing total units sold by average stock level per facility. Higher turnover rates indicate efficient inventory flow; very low turnover may indicate overstocking or slow-moving inventory at a facility.

---

#### 🗂️ Stock Distribution: Facility → Category (Treemap)

**Chart type:** Treemap

A hierarchical area chart where the outer rectangles represent facilities and inner rectangles represent product categories within each facility. Rectangle size encodes total stock volume. Immediately shows where physical inventory is concentrated and how it is spread across the warehouse network.

---

### 🚚 Shipment

**Purpose:** Tracks outbound logistics performance from dispatch to delivery. Supports logistics managers and customer service teams in monitoring fulfillment rates, carrier efficiency, cost management, and delivery reliability.

---

#### 📋 Shipment Status Distribution

**Chart type:** Donut pie

Shows the proportion of all shipments in each status (Delivered, In Transit, Delayed, Processing). The delivered share is the primary component of the Perfect Order Rate KPI and indicates overall fulfillment health.

---

#### 🚢 Carrier: Volume vs Avg Cost

**Chart type:** Bubble scatter

Each carrier is plotted by total shipment volume (x-axis) against average shipping cost (y-axis), with bubble size also encoding volume. Highlights carriers that are expensive relative to their volume and surfaces candidates for rate renegotiation.

---

#### 📦 Monthly Shipment Volume

**Chart type:** Area chart

Tracks total units shipped per month as a filled area. Identifies shipping seasonality, fulfillment surges aligned with sales peaks, and periods of unusual shipping inactivity.

---

#### 💲 Avg Shipping Cost per Shipment by Carrier

**Chart type:** Vertical bar (color-scaled)

Compares the average cost per shipment across all carriers. Color moves from green (low cost) to red (high cost). Provides a direct cost comparison for carrier selection and contract review.

---

#### ⚖️ Total & Avg Weight Shipped by Carrier

**Chart type:** Bar + line (dual axis)

Total weight handled by each carrier is shown as bars, while average weight per shipment is overlaid as a line. Useful for understanding carrier workload distribution and whether certain carriers are handling disproportionately heavy consignments.

---

#### ⏰ Shipment Delay Reasons

**Chart type:** Donut pie

Breaks down the reasons recorded for shipment delays. Where delay reason data is available, this chart identifies the most frequent root causes — such as customs holds, carrier capacity, or weather — enabling targeted interventions.

---

#### 🌍 Shipment Quantity by Destination Country

**Chart type:** Vertical bar (color-scaled)

Shows the total units shipped to customers in each destination country. Identifies the highest-volume destination markets and supports logistics network planning decisions such as regional warehouse placement.

---

### 💵 Sales

**Purpose:** Provides detailed analysis of sales performance, customer behavior, pricing dynamics, and product demand. Supports sales managers, account executives, and commercial analysts in understanding what is selling, to whom, at what price, and with what profitability.

---

#### 📅 Revenue Trend & Order Volume

**Chart type:** Area + bar (dual axis)

Net revenue is shown as a filled area line over time. Order count is overlaid as bars on the secondary axis. Divergence between the two lines — revenue growing while orders stagnate, or vice versa — signals changes in average order value worth investigating.

---

#### 🛍️ Sales by Channel

**Chart type:** Donut pie

Shows the revenue contribution of each customer channel type (e.g. Online, Retailer, Distributor). Useful for understanding channel mix and evaluating whether the business is appropriately diversified across routes to market.

---

#### 🏷️ Discount Rate vs Profit Margin Bubble

**Chart type:** Bubble scatter

Each bubble represents a product category, positioned by average discount rate (x-axis) and average profit margin (y-axis), with bubble size encoding revenue. Categories in the lower-right (high discount, low margin) are candidates for pricing strategy review.

---

#### 🥇 Top 8 Products by Revenue

**Chart type:** Horizontal bar (color-scaled)

Ranks the top eight individual products by net revenue. Identifies hero products that carry a disproportionate share of revenue and highlights dependency risk if any single product dominates.

---

#### 💳 Avg Order Value by Customer Country

**Chart type:** Vertical bar (color-scaled)

Calculates average order value (total revenue ÷ unique orders) per customer country and sorts descending. Countries with high average order values may represent premium or enterprise customer bases worth prioritizing.

---

#### 📱 Units Sold by Product Spec

**Chart type:** Vertical bar (colored by category)

Shows units sold broken down by product specification (e.g. storage tier, model variant), colored by category. Reveals which specific configurations drive demand volume and informs production planning and inventory positioning decisions.

---

#### 🗓️ Revenue Heatmap (Month × Product Line)

**Chart type:** Heatmap

A grid where rows are calendar months and columns are product lines. Cell color encodes total revenue — darker cells represent higher revenue periods. Surfaces seasonality patterns by product line and helps align promotional calendars with natural demand peaks.

---

## Design Principles

The dashboard follows a set of consistent design principles applied uniformly across all views.

**Dark theme.** The interface uses a deep navy dark theme optimized for extended analytical work. The color palette (`#0D1B2A` background, `#1A2744` card surfaces) reduces eye strain during long sessions and provides strong contrast for data visualization.

**Consistent chart theming.** Every chart is rendered through a shared `apply_theme()` function that enforces transparent backgrounds, matching font families, muted grid lines, and a consistent color sequence. This ensures visual coherence regardless of chart type or data volume.

**Color semantics.** Colors carry consistent meaning throughout the dashboard. Green (`#06D6A0`) indicates positive or healthy values. Red (`#EF233C`) indicates risk or negative values. Amber (`#FFB703`) signals caution or secondary metrics. Cyan (`#00B4D8`) is used for primary data series.

**Filter-responsive.** All five sidebar filters are applied at the data layer before any chart function runs. Every single visualization in every tab reflects the same filtered slice of data, ensuring that numbers are always internally consistent when comparing across tabs.

**Modular chart functions.** Each chart is encapsulated in its own function. This makes individual charts independently testable, replaceable, and extensible without affecting surrounding charts.

---

## Data Sources Summary

| Dataset                | Rows (approx.) | Primary use                                         |
| ---------------------- | -------------- | --------------------------------------------------- |
| `fact_sales.csv`       | 8,500          | Revenue, profit, margin, discount analysis          |
| `fact_procurement.csv` | 2,200          | Supplier spend, quality, lead time                  |
| `fact_production.csv`  | 4,500          | Output volume, defect rates, facility utilization   |
| `fact_inventory.csv`   | 1,150          | Stock levels, safety stock, reorder positions       |
| `fact_shipment.csv`    | 7,500          | Delivery status, carrier performance, shipping cost |
| `dim_date.csv`         | 730            | Calendar joins for time-series analysis             |
| `dim_product.csv`      | —              | Product attributes, category, spec, pricing         |
| `dim_supplier.csv`     | —              | Supplier name, country, tier, quality benchmark     |
| `dim_customer.csv`     | —              | Customer name, country, channel, size               |
| `dim_facility.csv`     | —              | Facility name, location, type, annual capacity      |

---

_Supply Chain Analytics Dashboard — built with Streamlit & Plotly_
