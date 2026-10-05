
import sqlite3
import pandas as pd
import re

DB_PATH = "ecommerce.db"
SQL_PATH = "sql/analysis_queries.sql"

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql = file.read()

# Remove SQL single-line comments
sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)

# Split SQL into individual queries
queries = [q.strip() for q in sql.split(";") if q.strip()]

conn = sqlite3.connect(DB_PATH)

print(f"\nTotal SQL queries found: {len(queries)}")

for i, query in enumerate(queries, 1):
    try:
        result = pd.read_sql_query(query, conn)

        print("\n" + "=" * 65)
        print(f"QUERY {i} RESULT")
        print("=" * 65)
        print(result.to_string(index=False, max_rows=30))

    except Exception as e:
        print(f"\nQUERY {i} ERROR: {e}")

conn.close()
print("\nSQL ANALYSIS COMPLETED!")
