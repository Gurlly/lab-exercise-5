-- SQLite
CREATE TABLE IF NOT EXISTS sales (
    transaction_id TEXT PRIMARY KEY,
    product_id TEXT,
    quantity REAL,
    price REAL,
    timestamp TEXT
)

SELECT * from sales LIMIT 20;
