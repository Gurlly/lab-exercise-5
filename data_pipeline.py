import pandas as pd
import numpy as np
import math
from dateutil import parser as dp

#----------------------------------------- T A S K # 1 : E D A  -------------------------------------------------
df = pd.read_csv('./inconsistent_transactions.csv')

print("Number of transactional records in the dataset :",df.shape,"\n")
print("First and last few rows of dataset")
print(df.head(),"\n")
print(df.tail(),"\n")

# Check for missing and duplicated values
missing_values = df.isnull().sum()
print("List of missing values for each attribute:")
print(missing_values,"\n")

duplicated_values = df.duplicated().sum()
print(f"Number of duplicated rows: {duplicated_values}")
print("\n")

print("The data types of each column: ")
print(df.dtypes,"\n")

# Transaction ID
# Checks the column transaction id to check whether all of the rows conform to the current obvious format "T####"
df['valid_tran'] = df['transaction_id'].str.match(r'^T\d{4}$', na=False)
invalid_tranC = (df['valid_tran'] == False).sum()
print(f"Number of invalid transaction id formats: {invalid_tranC}")

# Checks duplicates of transaction id
duplicate_count = df['transaction_id'].duplicated(keep=False).sum()
print(f"Total number of duplicate transaction IDs: {duplicate_count}")

# Product ID
# Checks the column product id to check whether all of the rows conform to the current obvious format "P###"
df['valid_prod'] = df['product_id'].str.match(r'^P\d{3}$', na=False)
invalid_prodC = (df['valid_prod'] == False).sum()
print(f"Number of invalid product id formats: {invalid_prodC}")

#Timestamp
print(df[['transaction_id','timestamp']])


#-------------------------------------------------------------------------------------------------------------


#---------------------------------- T A S K # 2 : D A T A  C L E A N I N G ----------------------------------

#Reset the data frame values and columns for standardizations
df = pd.read_csv('./inconsistent_transactions.csv')

print('Before Cleaning and Standardization: \n', df.head(n=31),'\n')


# Product Standardization (P####)
df['product_id'] = df['product_id'].astype(str).str.strip().str.upper()
df['product_id'] = df['product_id'].apply(lambda x: 'P' + ''.join(filter(str.isdigit, x)).zfill(4))

# Timestamp Formatting (YYYY-MM-DD)
def parse_date(date_str):
    try:
        parsed_date = dp.parse(date_str)
        return parsed_date
    except (ValueError, TypeError):
        return pd.NaT

df['timestamp'] = df['timestamp'].apply(parse_date)
df['timestamp'] = df['timestamp'].dt.date

# Quantity and Price Formatting (Quantity : Integer, Price : $##.##)

# Clean the price (remove $ sign, convert to float, round to 4 decimal places)
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float).round(4)

# Calculate each unit_price by using (price / quantity), and fill missing values using max unit price for each product_id
# Max is used in order to consider the possible discounts, sales, and other variables that influenced the unequal pricing of same product in different transactions
df['unit_price'] = df.apply(lambda row: row['price'] / row['quantity'] if pd.notna(row['price']) and pd.notna(row['quantity']) else None, axis=1)
max_unit_prices = df.groupby('product_id')['unit_price'].transform('max')
df['unit_price'] = df['unit_price'].fillna(max_unit_prices)

# Fill the missing prices using unit_price and quantity (price = unit_price * quantity)
df['price'] = df['price'].fillna(df['unit_price'] * df['quantity'])

# Fill the missing quantities using price and unit_price (quantity = price / unit_price) if there is a price
df['quantity'] = df['quantity'].fillna(df['price'] / df['unit_price'])
df['quantity'] = df['quantity'].apply(lambda x: math.floor(x) if x > 1 else x)

# Drop rows where both price and quantity are missing which resembles invalid transactions
df = df.dropna(subset=['price', 'quantity'], how='all')

# Drop 'unit_price' column, convert 'quantity' to integer to remove decimals and ceiling decimal quantities, and append '$' to the prices.
df = df.drop(columns=['unit_price'])
df['quantity'] = df['quantity'].apply(lambda x: math.ceil(x) if x < 1 else x)
df['quantity'] = df['quantity'].astype(int)
df['price'] = df['price'].apply(lambda x: f"${x:.2f}")

#Save standardized data
df.to_csv('./cleaned_transactions.csv', index=False)

print(df)

print('After Cleaning and Standardization: \n', df.head(n=31), '\n\n')

#-----------------------------------------------------------------------------------------------------

#---------------------------------- T A S K # 3 : D A T A   B A S E ----------------------------------
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('shopease_sales.db')
cursor = conn.cursor()

# Insert the DataFrame into the sales table
df.to_sql('sales', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

#-----------------------------------------------------------------------------------------------------
