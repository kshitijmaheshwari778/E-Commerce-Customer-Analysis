"""
generate_dataset.py
--------------------
Generates a realistic, messy synthetic E-Commerce dataset for the
E-Commerce Customer Analytics Dashboard portfolio project.

The dataset intentionally includes:
- Missing values (Age, Discount, Customer_Name)
- Duplicate rows
- Inconsistent text casing/whitespace (City, Gender, Payment_Method)
- Mixed date formats
- A few negative/invalid numeric entries

This mirrors real-world raw data so the cleaning notebook has genuine
work to do (important for portfolio credibility).
"""

import numpy as np
import pandas as pd
from faker import Faker
import random

fake = Faker("en_IN")
Faker.seed(42)
np.random.seed(42)
random.seed(42)

N_CUSTOMERS = 1200
N_ORDERS = 12000
START_DATE = pd.Timestamp("2022-01-01")
END_DATE = pd.Timestamp("2024-12-31")

REGIONS = {
    "North": ["Delhi", "Chandigarh", "Lucknow", "Jaipur", "Dehradun"],
    "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
    "East": ["Kolkata", "Patna", "Bhubaneswar", "Guwahati", "Ranchi"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nagpur"],
}
STATE_MAP = {
    "Delhi": "Delhi", "Chandigarh": "Punjab", "Lucknow": "Uttar Pradesh",
    "Jaipur": "Rajasthan", "Dehradun": "Uttarakhand",
    "Bengaluru": "Karnataka", "Chennai": "Tamil Nadu", "Hyderabad": "Telangana",
    "Kochi": "Kerala", "Coimbatore": "Tamil Nadu",
    "Kolkata": "West Bengal", "Patna": "Bihar", "Bhubaneswar": "Odisha",
    "Guwahati": "Assam", "Ranchi": "Jharkhand",
    "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Ahmedabad": "Gujarat",
    "Surat": "Gujarat", "Nagpur": "Maharashtra",
}

CATEGORY_PRODUCTS = {
    "Electronics": ["Wireless Earbuds", "Smartphone", "Laptop", "Bluetooth Speaker",
                    "Smartwatch", "Power Bank", "LED Monitor", "Tablet"],
    "Fashion": ["Men's T-Shirt", "Women's Kurti", "Running Shoes", "Denim Jacket",
                "Formal Shirt", "Handbag", "Sunglasses", "Leather Wallet"],
    "Home & Kitchen": ["Non-Stick Pan", "Mixer Grinder", "Air Fryer", "Bedsheet Set",
                       "Storage Containers", "Vacuum Cleaner", "Table Lamp"],
    "Beauty & Personal Care": ["Face Serum", "Hair Dryer", "Perfume", "Lipstick Set",
                               "Trimmer", "Sunscreen"],
    "Books": ["Fiction Novel", "Self-Help Book", "Children's Storybook", "Cookbook",
              "Biography"],
    "Sports & Fitness": ["Yoga Mat", "Dumbbell Set", "Cricket Bat", "Football",
                         "Resistance Bands", "Cycling Helmet"],
    "Groceries": ["Organic Atta 5kg", "Cold Pressed Oil", "Green Tea Pack",
                  "Dry Fruits Combo", "Spices Combo Pack"],
}

CATEGORY_PRICE_RANGE = {
    "Electronics": (1200, 65000),
    "Fashion": (399, 4500),
    "Home & Kitchen": (499, 12000),
    "Beauty & Personal Care": (199, 3500),
    "Books": (150, 900),
    "Sports & Fitness": (300, 8000),
    "Groceries": (99, 1200),
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "Wallet"]
GENDERS = ["Male", "Female"]

# ---------------------------------------------------------------
# 1. Generate customer master list (so customers repeat across orders)
# ---------------------------------------------------------------
customers = []
for i in range(1, N_CUSTOMERS + 1):
    region = random.choice(list(REGIONS.keys()))
    city = random.choice(REGIONS[region])
    customers.append({
        "Customer_ID": f"CUST{i:05d}",
        "Customer_Name": fake.name(),
        "Gender": random.choice(GENDERS),
        "Age": int(np.clip(np.random.normal(34, 10), 18, 70)),
        "City": city,
        "State": STATE_MAP[city],
        "Region": region,
    })
customers_df = pd.DataFrame(customers)

# Give some customers a "joined" weight so some are far more frequent buyers
customer_weights = np.random.pareto(2.0, size=len(customers_df)) + 0.1
customer_weights = customer_weights / customer_weights.sum()

# ---------------------------------------------------------------
# 2. Generate orders
# ---------------------------------------------------------------
date_range_days = (END_DATE - START_DATE).days

# Slight seasonal/trend skew: more orders in later years and Oct-Dec (festive)
def random_order_date():
    year_weights = [0.25, 0.35, 0.40]  # 2022, 2023, 2024
    year = np.random.choice([2022, 2023, 2024], p=year_weights)
    month_weights = np.array([0.07, 0.06, 0.07, 0.07, 0.07, 0.07,
                               0.07, 0.08, 0.09, 0.13, 0.13, 0.09])
    month_weights = month_weights / month_weights.sum()
    month = np.random.choice(range(1, 13), p=month_weights)
    day = random.randint(1, 28)
    return pd.Timestamp(year=year, month=month, day=day)

rows = []
for order_num in range(1, N_ORDERS + 1):
    cust_idx = np.random.choice(customers_df.index, p=customer_weights)
    cust = customers_df.loc[cust_idx]

    category = random.choice(list(CATEGORY_PRODUCTS.keys()))
    product = random.choice(CATEGORY_PRODUCTS[category])
    low, high = CATEGORY_PRICE_RANGE[category]
    unit_price = round(np.random.uniform(low, high), 2)

    quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.13, 0.08, 0.04])
    discount = round(np.random.choice([0, 0.05, 0.10, 0.15, 0.20, 0.25],
                                       p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]), 2)

    gross_sales = unit_price * quantity
    sales = round(gross_sales * (1 - discount), 2)

    # cost ratio varies by category to create realistic profit margins
    cost_ratio = {
        "Electronics": 0.78, "Fashion": 0.55, "Home & Kitchen": 0.65,
        "Beauty & Personal Care": 0.5, "Books": 0.6,
        "Sports & Fitness": 0.6, "Groceries": 0.72,
    }[category]
    cost = gross_sales * cost_ratio
    profit = round(sales - cost, 2)

    order_date = random_order_date()

    rows.append({
        "Order_ID": f"ORD{order_num:06d}",
        "Order_Date": order_date,
        "Customer_ID": cust["Customer_ID"],
        "Customer_Name": cust["Customer_Name"],
        "Gender": cust["Gender"],
        "Age": cust["Age"],
        "City": cust["City"],
        "State": cust["State"],
        "Region": cust["Region"],
        "Product_Category": category,
        "Product_Name": product,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "Payment_Method": random.choice(PAYMENT_METHODS),
    })

df = pd.DataFrame(rows)

# ---------------------------------------------------------------
# 3. Inject realistic messiness for the cleaning step
# ---------------------------------------------------------------
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)  # shuffle

# 3a. Duplicate ~1.5% of rows
dupe_idx = df.sample(frac=0.015, random_state=1).index
df = pd.concat([df, df.loc[dupe_idx]], ignore_index=True)

# 3b. Missing values
na_age_idx = df.sample(frac=0.04, random_state=2).index
df.loc[na_age_idx, "Age"] = np.nan

na_discount_idx = df.sample(frac=0.03, random_state=3).index
df.loc[na_discount_idx, "Discount"] = np.nan

na_name_idx = df.sample(frac=0.01, random_state=4).index
df.loc[na_name_idx, "Customer_Name"] = np.nan

na_city_idx = df.sample(frac=0.005, random_state=5).index
df.loc[na_city_idx, "City"] = np.nan

# 3c. Inconsistent text casing / whitespace
def messy_case(x):
    if pd.isna(x):
        return x
    r = random.random()
    if r < 0.25:
        return x.upper()
    elif r < 0.45:
        return x.lower()
    elif r < 0.55:
        return f"  {x}  "
    return x

mess_idx = df.sample(frac=0.15, random_state=6).index
df.loc[mess_idx, "City"] = df.loc[mess_idx, "City"].apply(messy_case)

mess_idx2 = df.sample(frac=0.15, random_state=7).index
df.loc[mess_idx2, "Gender"] = df.loc[mess_idx2, "Gender"].apply(messy_case)

mess_idx3 = df.sample(frac=0.10, random_state=8).index
df.loc[mess_idx3, "Payment_Method"] = df.loc[mess_idx3, "Payment_Method"].apply(messy_case)

# 3d. A few invalid numeric entries (negative quantity / unit price typos)
bad_idx = df.sample(frac=0.003, random_state=9).index
df.loc[bad_idx, "Quantity"] = -df.loc[bad_idx, "Quantity"]

bad_idx2 = df.sample(frac=0.002, random_state=10).index
df.loc[bad_idx2, "Unit_Price"] = 0

# 3e. Mixed date formats (store as strings for some rows to simulate raw export)
def mixed_date_format(d):
    r = random.random()
    if r < 0.5:
        return d.strftime("%Y-%m-%d")
    elif r < 0.8:
        return d.strftime("%d/%m/%Y")
    else:
        return d.strftime("%d-%b-%Y")

df["Order_Date"] = df["Order_Date"].apply(mixed_date_format)

# 3f. Shuffle final rows and reset Order_ID gaps are fine (realistic)
df = df.sample(frac=1.0, random_state=99).reset_index(drop=True)

# Reorder columns per the spec
cols = ["Order_ID", "Order_Date", "Customer_ID", "Customer_Name", "Gender", "Age",
        "City", "State", "Region", "Product_Category", "Product_Name", "Quantity",
        "Unit_Price", "Discount", "Sales", "Profit", "Payment_Method"]
df = df[cols]

df.to_csv("/home/claude/ECommerce-Customer-Analytics/data/ecommerce_raw.csv", index=False)
print("Generated raw dataset:", df.shape)
print(df.head())
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
