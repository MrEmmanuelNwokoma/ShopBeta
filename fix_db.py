import sqlite3

# DB_PATH = "my_database.db"  # replace with your real filename

# con = sqlite3.connect(DB_PATH)
# con.execute("ALTER TABLE products ADD COLUMN search_vector VARCHAR")
# con.commit()
# con.close()
# print("done")


import sqlite3

DB_PATH = "my_database.db"  # replace with your real database filename

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# 1. add the column if it isn't there yet
columns = [row[1] for row in cur.execute("PRAGMA table_info(products)")]
if "brand_name" not in columns:
    cur.execute("ALTER TABLE products ADD COLUMN brand_name VARCHAR")
    print("Added brand_name column")
else:
    print("brand_name column already exists")

# 2. copy each product's brand name from the brands table
cur.execute(
    """
    UPDATE products
    SET brand_name = (
        SELECT brands.name FROM brands WHERE brands.id = products.brand_id
    )
    """
)
print(f"Updated {cur.rowcount} products")

# 3. report any product that still has no brand name
missing = cur.execute(
    "SELECT COUNT(*) FROM products WHERE brand_name IS NULL"
).fetchone()[0]
print(f"Products still without a brand_name: {missing}")

con.commit()
con.close()