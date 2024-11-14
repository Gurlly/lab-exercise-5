# EDA 
import pandas as pd
import numpy as np
import sqlite3

# ----------------------------------------------LOADING-------------------------------------------------------------------

# Loading the Data
df = pd.read_csv('./inconsistent_transactions.csv')

# Show the first few rows of the dataset.
    #print(df.head())

# Retrieving the missing values
    #missing_values = df.isnull().sum()
    #print("\n\nThe missing values per column: \n", missing_values)

# Check data types and unique format for each column
    #print("\n\nData types: \n", df.dtypes)

# Detect outliers and inconsistencies
    #print("\n\nDescriptive statistics: \n", df.describe())

# ----------------------------------------------STANDARDIZATION-------------------------------------------------------------------

# product_id format (Number of digits and capitalizes lowercase "p")
df['product_id'] = df['product_id'].astype(str).str.strip().str.upper()
df['product_id'] = df['product_id'].apply(lambda x: 'P' + ''.join(filter(str.isdigit, x)).zfill(5) if x.startswith('P') else 'P' + ''.join(filter(str.isdigit, x)).zfill(5))

# timestamp format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Convert quantity and price to numeric, handling errors
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Handle missing values
df['quantity'].fillna(df['quantity'].mean(), inplace=True)
df['price'].fillna(df['price'].mean(), inplace=True)
df['product_id'].fillna('unknown', inplace=True)

# Format Price and quantity
df['price'] = df['price'].round(2)
df['quantity'] = df['quantity'].round(2)

# Remove negative values in 'quantity and 'price'
df = df[df['quantity'] >= 0]
df = df[df['price'] >= 0]

# Preview standardized data
print(df.head())

# Save standardized data
df.to_csv('./cleaned_transactions.csv', index=False)

# ----------------------------------------------DATABASE-------------------------------------------------------------------

# Connect to SQLite database
#conn = sqlite3.connect('shopease_sales.db')
#cursor = conn.cursor()
#
## Insert standardized table in the sales table
#df.to_sql('sales', conn, if_exists='replace', index=False)  
