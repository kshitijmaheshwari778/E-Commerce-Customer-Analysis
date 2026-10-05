# Project Report: E-Commerce Customer Analytics Dashboard

**Author:** Kshitij Dakhera
**Tools Used:** Python (Pandas, NumPy), SQL, Power BI, Jupyter Notebook
**Dataset:** Synthetic e-commerce transactions, 2022–2024 (17 columns, ~12,000 order lines, 1,137 unique customers)

---

## 1. Executive Summary

This project analyzes three years of e-commerce transaction data to surface
revenue trends, customer value patterns, and product/category profitability,
with the goal of identifying concrete, actionable growth opportunities. The
analysis pipeline spans data cleaning, feature engineering, SQL-based
business queries, Python-based statistical analysis (RFM segmentation,
cohort retention), and a 4-page Power BI dashboard.

**Headline numbers:**

| Metric | Value |
|---|---|
| Total Revenue (2022–2024) | ₹14.68 Crore (₹146.8M) |
| Total Profit | ₹3.09 Crore (₹30.9M) |
| Overall Profit Margin | 21.0% |
| Total Orders | 11,978 |
| Total Customers | 1,137 |
| Average Order Value | ₹12,258.65 |
| Repeat Purchase Rate | 86.2% |
| Avg. Quarter-over-Quarter Retention | 57.3% |

---

## 2. Methodology

### 2.1 Data Cleaning
The raw export contained realistic data-quality issues: mixed date formats
(`YYYY-MM-DD`, `DD/MM/YYYY`, `DD-Mon-YYYY`), ~1.5% duplicate rows,
inconsistent text casing (`"mumbai"` vs `"MUMBAI"` vs `"Mumbai "`), missing
values in `Age` (4%), `Discount` (3%), `Customer_Name` (1%) and `City`
(0.5%), and a small number of invalid numeric entries (negative quantities,
zero unit prices). Each issue was resolved with a documented, defensible
strategy (median imputation for `Age`, zero-fill for `Discount`, dropped
rows for zero-price transactions, etc.) — see `notebooks/01_data_cleaning.ipynb`
for the full audit trail.

### 2.2 Feature Engineering
Derived `Month`, `Quarter`, `Year`, and `Year_Month` fields for time-series
analysis; `Profit_Margin` per order line; and customer-level aggregates —
`Customer_Lifetime_Value`, `Average_Order_Value`, `Total_Orders`,
`Customer_Tenure_Days`, and a repeat-customer flag.

### 2.3 SQL Analysis
Eight categories of business queries were written and validated against the
cleaned dataset (`sql/analysis_queries.sql`): top customers, top products,
monthly revenue trends with MoM growth, region-wise sales, profit analysis,
customer retention, average order value, and category performance — plus
five bonus queries (YoY growth, basket size, payment distribution,
state-wise sales, and per-category product ranking using window functions).

### 2.4 Python Analysis
Using Pandas: customer segmentation (value-tier and RFM-based), revenue and
profitability breakdowns, product analysis, and two advanced techniques:

- **RFM Analysis** — customers scored 1–5 on Recency, Frequency, and
  Monetary value, then mapped into 7 segments (Champions, Loyal Customers,
  Potential Loyalists, New Customers, Needs Attention, At Risk, Lost).
- **Cohort Analysis** — customers grouped by first-purchase month, with
  retention tracked for up to 18 months post-acquisition, visualized as a
  heatmap.

---

## 3. Key Findings

### 3.1 Revenue is growing, but growth is decelerating
Annual revenue grew from ₹3.37 Cr (2022) → ₹5.40 Cr (2023, **+60.0%**) →
₹5.91 Cr (2024, **+9.5%**). The deceleration in 2024 growth relative to 2023
is the single most important trend for leadership to address — it suggests
the business is shifting from a high-growth acquisition phase toward a
maturity phase where retention and basket-size growth will matter more than
new customer acquisition.

### 3.2 A small customer segment drives most of the revenue
RFM segmentation shows **Champions** (312 customers, 27.4% of the customer
base) generate **₹10.05 Cr — 68.5% of total revenue**. By contrast, the
**Lost** segment (183 customers, 16.1%) contributes just ₹27.7 Lakh (1.9%).
This is a classic Pareto pattern and has two direct implications:
1. Retention/loyalty investment should prioritize protecting the Champions
   segment (even small churn here has outsized revenue impact).
2. The "Needs Attention" and "At Risk" segments (272 customers combined,
   ₹1.58 Cr in historical revenue) represent the highest-leverage win-back
   opportunity — they have proven purchase intent but declining recency.

### 3.3 Electronics dominates revenue but has the thinnest margin
Electronics is the clear revenue leader (₹9.96 Cr, ~68% of total revenue)
but carries the **lowest profit margin of any category at 14.9%** — well
below the 21% company average. By contrast, **Beauty & Personal Care**
(45.0% margin) and **Fashion** (39.8% margin) are comparatively small
revenue contributors but highly profitable per rupee of sales. A deliberate
mix-shift strategy — promotional emphasis on Fashion/Beauty alongside
Electronics — could lift overall profit margin without sacrificing revenue
scale.

### 3.4 Regional performance is balanced, with East leading narrowly
Revenue is fairly evenly split across regions: East (₹3.89 Cr), West
(₹3.67 Cr), South (₹3.57 Cr), North (₹3.54 Cr) — no region is
underperforming dramatically, which suggests the current regional go-to-market
approach is reasonably well-balanced, though East's slight lead is worth
investigating for replicable best practices (e.g. city-level demand drivers).

### 3.5 Retention has room to improve
The average quarter-over-quarter customer retention rate is **57.3%** — a
healthy figure, but cohort analysis shows retention drops sharply after the
first 1–2 months post-acquisition (from 100% to roughly 10–30% by month 1)
before stabilizing into a long noisy tail. This points to an opportunity for
a structured "month 1–2" re-engagement campaign (e.g. a second-purchase
incentive) to convert more first-time buyers into repeat Champions before
they churn.

### 3.6 Payment method usage is balanced — no single dependency risk
Revenue is spread fairly evenly across Wallet (₹2.58 Cr), Net Banking
(₹2.58 Cr), UPI (₹2.47 Cr), Credit Card (₹2.42 Cr), Cash on Delivery
(₹2.41 Cr), and Debit Card (₹2.23 Cr) — no single payment rail accounts for
more than ~18% of revenue, which is a healthy risk profile (no
over-dependence on any one payment processor or method).

---

## 4. Recommendations

1. **Protect the Champions segment.** Launch a loyalty/VIP program targeted
   at the top 312 customers driving 68.5% of revenue — even a 5% churn
   reduction here would protect roughly ₹5 Cr in annual revenue.
2. **Win back "Needs Attention" and "At Risk" segments** with targeted
   discount or re-engagement campaigns — 272 customers with proven purchase
   history and ₹1.58 Cr in historical spend are at risk of moving to "Lost."
3. **Rebalance category promotion toward higher-margin lines** (Beauty &
   Personal Care, Fashion) to lift blended profit margin above the current
   21%, without abandoning Electronics' revenue scale.
4. **Build a "second purchase" campaign** targeting customers in their first
   60 days, since cohort data shows the steepest retention drop-off occurs
   in month 1.
5. **Investigate East region's slight outperformance** for replicable
   tactics (marketing channel mix, city-level demand) that could be applied
   to North, which currently lags slightly.

---

## 5. Limitations & Next Steps

- This analysis uses a synthetic dataset generated to mirror realistic
  e-commerce patterns (seasonality, category margins, customer behavior);
  conclusions demonstrate methodology and should be re-validated against
  real transaction data in a production setting.
- Retention rate is calculated quarter-over-quarter as a proxy; a true
  survival-analysis or predictive churn model (e.g. logistic regression or
  gradient boosting on RFM + behavioral features) would be a natural
  next step.
- The Power BI dashboard design (`dashboard/PowerBI_Design_Spec.md`) is
  provided as a complete, build-ready specification with DAX measures;
  building the final interactive `.pbix` file requires Power BI Desktop.

---

*Full code, SQL queries, and visualizations are available in this repository
under `/notebooks`, `/sql`, and `/images`.*
