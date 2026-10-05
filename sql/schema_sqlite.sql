
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    Order_ID TEXT NOT NULL PRIMARY KEY,
    Order_Date TEXT NOT NULL,
    Customer_ID TEXT NOT NULL,
    Customer_Name TEXT,
    Gender TEXT,
    Age INTEGER,
    City TEXT,
    State TEXT,
    Region TEXT,
    Product_Category TEXT,
    Product_Name TEXT,
    Quantity INTEGER,
    Unit_Price REAL,
    Discount REAL,
    Sales REAL,
    Profit REAL,
    Payment_Method TEXT,
    Year INTEGER,
    Month INTEGER,
    Month_Name TEXT,
    Quarter INTEGER,
    Year_Quarter TEXT,
    Year_Month TEXT,
    Profit_Margin REAL
);

CREATE INDEX idx_orders_customer ON orders (Customer_ID);
CREATE INDEX idx_orders_date ON orders (Order_Date);
CREATE INDEX idx_orders_category ON orders (Product_Category);
CREATE INDEX idx_orders_region ON orders (Region);
