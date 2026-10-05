
import sqlite3
import pandas as pd

csv_path = "data/ecommerce_features.csv"
db_path = "ecommerce.db"

columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Customer_Name",
    "Gender",
    "Age",
    "City",
    "State",
    "Region",
    "Product_Category",
    "Product_Name",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Profit",
    "Payment_Method",
    "Year",
    "Month",
    "Month_Name",
    "Quarter",
    "Year_Quarter",
    "Year_Month",
    "Profit_Margin"
]

df = pd.read_csv(csv_path)
df = df[columns]

# Remove duplicate Order_ID values from CSV if any
df = df.drop_duplicates(subset=["Order_ID"])

conn = sqlite3.connect(db_path)

try:
    # Clear existing records before fresh import
    conn.execute("DELETE FROM orders")
    conn.commit()

    # Import all records
    df.to_sql("orders", conn, if_exists="append", index=False)

    # Verify record count
    count = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    print("CSV imported successfully!")
    print("Records imported:", count)

    print("\nFirst 5 records:")
    print(pd.read_sql_query(
        "SELECT * FROM orders LIMIT 5", conn
    ))

except Exception as e:
    conn.rollback()
    print("Import failed:", e)

finally:
    conn.close()
