-- =====================================================================
-- schema.sql
-- E-Commerce Customer Analytics Dashboard
-- Schema definition for the cleaned, feature-engineered dataset.
-- Compatible with MySQL / PostgreSQL (minor type tweaks noted inline).
-- =====================================================================

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    Order_ID            VARCHAR(20)     NOT NULL,
    Order_Date          DATE            NOT NULL,
    Customer_ID         VARCHAR(20)     NOT NULL,
    Customer_Name       VARCHAR(100),
    Gender              VARCHAR(10),
    Age                 INT,
    City                VARCHAR(50),
    State               VARCHAR(50),
    Region              VARCHAR(20),
    Product_Category    VARCHAR(50),
    Product_Name        VARCHAR(100),
    Quantity            INT,
    Unit_Price          DECIMAL(10,2),
    Discount            DECIMAL(4,2),     -- stored as a fraction, e.g. 0.10 = 10%
    Sales               DECIMAL(12,2),
    Profit              DECIMAL(12,2),
    Payment_Method      VARCHAR(30),

    -- Feature-engineered columns (added in 02_feature_engineering.ipynb)
    Year                INT,
    Month               INT,
    Month_Name          VARCHAR(15),
    Quarter             INT,
    Year_Quarter        VARCHAR(10),
    Year_Month          VARCHAR(10),
    Profit_Margin       DECIMAL(6,2),     -- percentage

    PRIMARY KEY (Order_ID)
);

CREATE INDEX idx_orders_customer   ON orders (Customer_ID);
CREATE INDEX idx_orders_date       ON orders (Order_Date);
CREATE INDEX idx_orders_category   ON orders (Product_Category);
CREATE INDEX idx_orders_region     ON orders (Region);

-- ---------------------------------------------------------------------
-- Loading the cleaned CSV (MySQL example — adjust path & permissions):
--
-- LOAD DATA LOCAL INFILE '/path/to/ecommerce_features.csv'
-- INTO TABLE orders
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
--
-- PostgreSQL example:
-- \copy orders FROM '/path/to/ecommerce_features.csv' DELIMITER ',' CSV HEADER;
-- ---------------------------------------------------------------------
