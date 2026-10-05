-- =====================================================================
-- analysis_queries.sql
-- E-Commerce Customer Analytics Dashboard — SQL Analysis Queries
-- Target schema: orders table (see schema.sql)
-- Dialect: ANSI SQL / MySQL-compatible (window functions used — MySQL 8+,
-- PostgreSQL, or SQL Server all support this syntax with no changes)
-- =====================================================================


-- =====================================================================
-- 1. TOP 10 CUSTOMERS BY REVENUE
-- =====================================================================
SELECT
    Customer_ID,
    Customer_Name,
    COUNT(DISTINCT Order_ID)   AS Total_Orders,
    SUM(Sales)                 AS Total_Revenue,
    SUM(Profit)                AS Total_Profit,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
FROM orders
GROUP BY Customer_ID, Customer_Name
ORDER BY Total_Revenue DESC
LIMIT 10;


-- =====================================================================
-- 2. TOP SELLING PRODUCTS (by revenue and by units sold)
-- =====================================================================
-- 2a. By Revenue
SELECT
    Product_Name,
    Product_Category,
    SUM(Quantity)       AS Units_Sold,
    SUM(Sales)          AS Total_Revenue,
    SUM(Profit)          AS Total_Profit
FROM orders
GROUP BY Product_Name, Product_Category
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 2b. By Units Sold
SELECT
    Product_Name,
    Product_Category,
    SUM(Quantity)       AS Units_Sold,
    SUM(Sales)          AS Total_Revenue
FROM orders
GROUP BY Product_Name, Product_Category
ORDER BY Units_Sold DESC
LIMIT 10;


-- =====================================================================
-- 3. MONTHLY REVENUE TRENDS (with month-over-month growth %)
-- =====================================================================
SELECT
    Year_Month,
    SUM(Sales)  AS Monthly_Revenue,
    SUM(Profit) AS Monthly_Profit,
    ROUND(
        (SUM(Sales) - LAG(SUM(Sales)) OVER (ORDER BY Year_Month))
        / LAG(SUM(Sales)) OVER (ORDER BY Year_Month) * 100
    , 2) AS MoM_Growth_Pct
FROM orders
GROUP BY Year_Month
ORDER BY Year_Month;


-- =====================================================================
-- 4. REGION-WISE SALES
-- =====================================================================
SELECT
    Region,
    COUNT(DISTINCT Order_ID)       AS Total_Orders,
    COUNT(DISTINCT Customer_ID)    AS Total_Customers,
    SUM(Sales)                     AS Total_Revenue,
    SUM(Profit)                    AS Total_Profit,
    ROUND(SUM(Sales) * 100.0 / SUM(SUM(Sales)) OVER (), 2) AS Pct_of_Total_Revenue
FROM orders
GROUP BY Region
ORDER BY Total_Revenue DESC;


-- =====================================================================
-- 5. PROFIT ANALYSIS (by category, with margin %)
-- =====================================================================
SELECT
    Product_Category,
    SUM(Sales)                                 AS Total_Revenue,
    SUM(Profit)                                AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS Profit_Margin_Pct,
    RANK() OVER (ORDER BY SUM(Profit) DESC)    AS Profit_Rank
FROM orders
GROUP BY Product_Category
ORDER BY Total_Profit DESC;


-- =====================================================================
-- 6. CUSTOMER RETENTION ANALYSIS
-- =====================================================================
-- 6a. New vs Returning customers per month (a customer counts as
--     "returning" in month M if they had at least one order before month M)
WITH first_order AS (
    SELECT Customer_ID, MIN(Year_Month) AS First_Month
    FROM orders
    GROUP BY Customer_ID
),
monthly_activity AS (
    SELECT DISTINCT o.Customer_ID, o.Year_Month
    FROM orders o
)
SELECT
    ma.Year_Month,
    SUM(CASE WHEN ma.Year_Month = fo.First_Month THEN 1 ELSE 0 END) AS New_Customers,
    SUM(CASE WHEN ma.Year_Month > fo.First_Month THEN 1 ELSE 0 END) AS Returning_Customers
FROM monthly_activity ma
JOIN first_order fo ON ma.Customer_ID = fo.Customer_ID
GROUP BY ma.Year_Month
ORDER BY ma.Year_Month;

-- 6b. Overall repeat purchase rate
SELECT
    COUNT(DISTINCT Customer_ID)                                   AS Total_Customers,
    SUM(CASE WHEN Order_Count > 1 THEN 1 ELSE 0 END)              AS Repeat_Customers,
    ROUND(SUM(CASE WHEN Order_Count > 1 THEN 1 ELSE 0 END) * 100.0
          / COUNT(DISTINCT Customer_ID), 2)                        AS Repeat_Purchase_Rate_Pct
FROM (
    SELECT Customer_ID, COUNT(DISTINCT Order_ID) AS Order_Count
    FROM orders
    GROUP BY Customer_ID
) customer_orders;


-- =====================================================================
-- 7. AVERAGE ORDER VALUE (overall, and by region/category)
-- =====================================================================
-- 7a. Overall AOV
SELECT ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Overall_AOV
FROM orders;

-- 7b. AOV by Region
SELECT
    Region,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
FROM orders
GROUP BY Region
ORDER BY Avg_Order_Value DESC;

-- 7c. AOV by Product Category
SELECT
    Product_Category,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
FROM orders
GROUP BY Product_Category
ORDER BY Avg_Order_Value DESC;


-- =====================================================================
-- 8. PRODUCT CATEGORY PERFORMANCE (comprehensive scorecard)
-- =====================================================================
SELECT
    Product_Category,
    COUNT(DISTINCT Order_ID)                       AS Total_Orders,
    SUM(Quantity)                                  AS Units_Sold,
    SUM(Sales)                                     AS Total_Revenue,
    SUM(Profit)                                    AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2)     AS Profit_Margin_Pct,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value,
    ROUND(SUM(Sales) * 100.0 / SUM(SUM(Sales)) OVER (), 2) AS Pct_of_Total_Revenue
FROM orders
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;


-- =====================================================================
-- BONUS: ADVANCED KPI QUERIES
-- =====================================================================

-- B1. Revenue Growth % (Year-over-Year)
SELECT
    Year,
    SUM(Sales) AS Annual_Revenue,
    ROUND(
        (SUM(Sales) - LAG(SUM(Sales)) OVER (ORDER BY Year))
        / LAG(SUM(Sales)) OVER (ORDER BY Year) * 100
    , 2) AS YoY_Growth_Pct
FROM orders
GROUP BY Year
ORDER BY Year;

-- B2. Average Basket Size (items per order)
SELECT ROUND(SUM(Quantity) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS Avg_Basket_Size
FROM orders;

-- B3. Payment Method Distribution
SELECT
    Payment_Method,
    COUNT(DISTINCT Order_ID)   AS Total_Orders,
    SUM(Sales)                 AS Total_Revenue,
    ROUND(COUNT(DISTINCT Order_ID) * 100.0
          / SUM(COUNT(DISTINCT Order_ID)) OVER (), 2) AS Pct_of_Orders
FROM orders
GROUP BY Payment_Method
ORDER BY Total_Revenue DESC;

-- B4. State-wise Sales (for the Regional Analytics Power BI page / map)
SELECT
    State,
    Region,
    COUNT(DISTINCT Order_ID)   AS Total_Orders,
    SUM(Sales)                 AS Total_Revenue,
    SUM(Profit)                AS Total_Profit
FROM orders
GROUP BY State, Region
ORDER BY Total_Revenue DESC;

-- B5. Top 5 Products per Category (ranked, using window function)
SELECT *
FROM (
    SELECT
        Product_Category,
        Product_Name,
        SUM(Sales) AS Revenue,
        RANK() OVER (PARTITION BY Product_Category ORDER BY SUM(Sales) DESC) AS Rank_in_Category
    FROM orders
    GROUP BY Product_Category, Product_Name
) ranked
WHERE Rank_in_Category <= 5
ORDER BY Product_Category, Rank_in_Category;
