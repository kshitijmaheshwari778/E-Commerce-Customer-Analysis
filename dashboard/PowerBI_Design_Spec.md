# Power BI Dashboard Design Specification
### E-Commerce Customer Analytics Dashboard

> **Note on deliverable format:** This repository includes the full data
> model design, DAX measures (`DAX_Measures.txt`), page-by-page layout,
> and visual specifications needed to build the `.pbix` file in Power BI
> Desktop. A `.pbix` is a binary file tied to a local Power BI
> installation and cannot be generated outside of it — so this document
> is written to be followed step-by-step to (re)build the actual file in
> under an hour, using the CSVs already produced in `/data`.

---

## 1. Data Model

**Tables to import** (Get Data → Text/CSV):

| Table Name | Source File | Grain |
|---|---|---|
| `Orders` | `data/ecommerce_features.csv` | One row per order line |
| `Customer_RFM` | `data/customer_rfm.csv` | One row per customer |
| `Customer_Features` | `data/customer_features.csv` | One row per customer |
| `Cohort_Retention` | `data/cohort_retention_table.csv` | One row per acquisition cohort |
| `Date` | Created in-model via DAX (see `DAX_Measures.txt`) | One row per calendar day, 2022–2024 |

**Relationships:**
- `Orders[Customer_ID]` → `Customer_RFM[Customer_ID]` (Many-to-One)
- `Orders[Customer_ID]` → `Customer_Features[Customer_ID]` (Many-to-One)
- `Orders[Order_Date]` → `Date[Date]` (Many-to-One) — mark `Date` as the official Date Table

**Recommended column data types:**
- `Order_Date` → Date
- `Sales`, `Profit`, `Unit_Price`, `Discount` → Decimal Number
- `Age`, `Quantity` → Whole Number
- All ID/text columns → Text

---

## 2. Page 1 — Executive Overview

**Layout:** 5 KPI cards across the top, 3 charts below.

**KPI Cards** (top row):
| Card | Measure | Format |
|---|---|---|
| Total Revenue | `[Total Revenue]` | ₹ Lakhs/Millions, 1 decimal |
| Total Profit | `[Total Profit]` | ₹ Lakhs/Millions, 1 decimal |
| Total Orders | `[Total Orders]` | Whole number, comma separator |
| Total Customers | `[Total Customers]` | Whole number |
| Average Order Value | `[Average Order Value]` | ₹, 0 decimals |

**Charts:**
1. **Monthly Revenue Trend** — Line chart. X = `Date[YearMonth]`, Y = `[Total Revenue]` and `[Total Profit]` (dual line). Add a trend line.
2. **Revenue by Region** — Clustered column or donut chart. Axis = `Orders[Region]`, Value = `[Total Revenue]`.
3. **Sales by Category** — Treemap or bar chart. Axis = `Orders[Product_Category]`, Value = `[Total Revenue]`.

**Slicers (page-level, top-right):** Date range slider, Region, Product Category.

---

## 3. Page 2 — Customer Analytics

**Visuals:**
1. **Customer Segmentation** — Donut or bar chart using `Customer_RFM[Segment]` (Champions, Loyal Customers, At Risk, Lost, etc.), Value = Customer count and `[Total Revenue]` (use a tooltip to show both).
2. **Customer Lifetime Value Distribution** — Histogram (use a CLV-bucket calculated column, e.g. 0–5K, 5–10K, 10–25K, 25K+) — bar chart of customer counts per bucket.
3. **Repeat vs New Customers** — Card pair or stacked bar by month: `[New Customers (This Period)]` vs `[Returning Customers (This Period)]`.
4. **Cohort Retention Heatmap** — Matrix visual: Rows = `Cohort_Retention[Cohort_Month]`, Columns = month-offset columns (0,1,2...), Values = retention %, conditional formatting (color scale) applied — replicates the heatmap built in `04_rfm_cohort_analysis.ipynb` (`images/10_cohort_retention_heatmap.png`).
5. **KPI Cards:** `[Repeat Purchase Rate %]`, `[Customer Retention Rate %]`, `[Customer Lifetime Value (Avg)]`.

**Slicers:** Gender, Age Group (calculated column bucketing Age into 18–25/26–35/36–50/50+), Region.

---

## 4. Page 3 — Product Analytics

**Visuals:**
1. **Top Products** — Horizontal bar chart, top 10 by `[Total Revenue]`, axis = `Orders[Product_Name]`.
2. **Top Categories** — Bar/treemap, axis = `Orders[Product_Category]`, value = `[Total Revenue]`.
3. **Product Profitability** — Table or matrix: Product_Name, Units Sold, Revenue, Profit, Profit Margin % — sortable, with data bars on Profit Margin %.
4. **Product Performance Matrix** — Scatter chart: X = `[Total Revenue]`, Y = `[Profit Margin %]`, Size = `[Units Sold]`, Legend = `Product_Category`. This is the classic BCG-style "stars / cash cows / question marks" quadrant view — replicate the bubble logic from `images/07_revenue_vs_profit.png` but at product grain instead of category grain.

**Slicers:** Product Category, Payment Method.

---

## 5. Page 4 — Regional Analytics

**Visuals:**
1. **State-wise Sales** — Bar chart or table, axis = `Orders[State]`, value = `[Total Revenue]`, sorted descending.
2. **Region-wise Profit** — Column chart, axis = `Orders[Region]`, value = `[Total Profit]`, with `[Profit Margin %]` as a secondary line.
3. **Interactive Map** — Power BI **Filled Map** or **ArcGIS Map** visual. Location = `Orders[State]` (or `City` for finer granularity), Size/Color = `[Total Revenue]`. Note: ensure "State" values match Power BI's geo-recognition (they're standard Indian state names in this dataset, which Power BI's Bing-powered map recognizes natively).
4. **Region/State cross-filter table** — Matrix with Region (rows), State (sub-rows), Revenue, Profit, Orders.

**Slicers:** Region, State, Date range.

---

## 6. Visual Theme & Formatting

To keep this on-brand and portfolio-polished:
- **Color palette:** Use a consistent 4–6 color palette across all pages (e.g. deep blue `#2C3E50`, teal `#16A085`, amber `#F39C12`, coral `#E74C3C` for negative/at-risk indicators).
- **Font:** Segoe UI (Power BI default) or a single consistent font throughout.
- **Card design:** Use consistent KPI card styling (rounded corners, subtle shadow, icon + label + value layout).
- **Conditional formatting:** Apply red/amber/green to Profit Margin %, Retention Rate columns in tables.
- Save a **theme JSON** (`View → Themes → Save current theme`) and include it in `/dashboard` once built, so the file is reusable.

---

## 7. Build Checklist

- [ ] Import all 5 tables, set relationships
- [ ] Mark Date table as official date table
- [ ] Paste in all DAX measures from `DAX_Measures.txt`
- [ ] Build Page 1 → 4 per the layouts above
- [ ] Apply consistent theme/colors
- [ ] Add page navigation buttons (top-right of each page)
- [ ] Test all slicers cross-filter correctly across visuals
- [ ] Publish to Power BI Service (optional) and grab the public/embed link for the README

Once built, export 1 screenshot per page to `/images` (e.g. `dashboard_page1_overview.png`, etc.) and link them in the main `README.md`.
