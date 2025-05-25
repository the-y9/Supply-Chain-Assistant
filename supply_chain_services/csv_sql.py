import pandas as pd
import sqlite3
import os

# === CONFIGURATION ===
CSV_DIR = 'Supply Chain dataset'
csv_file_path = os.path.join(CSV_DIR, 'DataCoSupplyChainDataset.csv')
sqlite_db_path = 'supply_chain.db'
table_name = 'supply_chain'

# === STEP 1: Read CSV with pandas ===
try:
    df = pd.read_csv(csv_file_path, encoding='latin1')
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)
# === STEP 2: Connect to SQLite database (creates file if not exists) ===
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

# === STEP 3: Optional - Drop table if already exists ===
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# === STEP 4: Write DataFrame to SQLite ===
df.to_sql(table_name, conn, if_exists='replace', index=False)

# === STEP 5: Verify the insert (optional) ===
cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
count = cursor.fetchone()[0]
print(f"Inserted {count} rows into '{table_name}' table in '{sqlite_db_path}'.")

# === STEP 6: Close connection ===
conn.close()
