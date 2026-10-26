import sqlite3

DB_PATH = "my_database.db"  # replace with your real filename

con = sqlite3.connect(DB_PATH)
con.execute("ALTER TABLE products ADD COLUMN search_vector VARCHAR")
con.commit()
con.close()
print("done")