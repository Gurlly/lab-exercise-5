-- SQLite
CREATE TABLE IF NOT EXISTS sales (
    transaction_id TEXT PRIMARY KEY,
    product_id TEXT,
    quantity REAL,
    price REAL,
    timestamp TEXT
)

DROP TABLE sales;

SELECT * from sales LIMIT 30;


SELECT 
    COUNT(*) AS possible_total_null_count,
    SUM(CASE WHEN transaction_id IS NULL THEN 1 ELSE 0 END) AS transaction_id_nulls,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS product_id_nulls,
    SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) AS quantity_nulls,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS price_nulls,
    SUM(CASE WHEN timestamp IS NULL THEN 1 ELSE 0 END) AS timestamp_nulls
FROM sales;

SELECT 
    product_id, 
    SUM(quantity) AS total_quantity_sold
FROM sales
GROUP BY product_id
ORDER BY total_quantity_sold DESC
LIMIT 5;


