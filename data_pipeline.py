# EDA 
import pandas as pd
import numpy as np

# Loading the Data
df = pd.read_csv('./inconsistent_transactions.csv')

# Show the first few rows of the dataset.
print(df.head())

# Retrieving the missing values
missing_values = df.isnull().sum()
print("\n\nThe missing values per column: \n", missing_values)

# Check data types and unique format for each column
print("\n\nData types: \n", df.dtypes)

# Detect outliers and inconsistencies
print("\n\nDescriptive statistics: \n", df.describe())