#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 18:34:00 2025

@author: phineasphan
"""


# -------------------------------------------
#  Import libraries
# -------------------------------------------
import pandas as pd                          # For data handling
import matplotlib.pyplot as plt              # For visualization

# -------------------------------------------
#  Step 1: Load the large CSV file in chunks
# -------------------------------------------
chunk_size = 100_000                         # Load 100,000 rows at a time
chunks = []                                  # List to store each chunk

print("Loading CSV...")

for chunk in pd.read_csv('2019-Oct.csv', engine='python', chunksize=chunk_size):
    chunks.append(chunk)                     # Append each chunk to the list

print("Loaded")

# -------------------------------------------
#  Step 2: Combine all chunks into one DataFrame
# -------------------------------------------
df = pd.concat(chunks, ignore_index=True)    # Merge chunks into one full table

# -------------------------------------------
#  Step 3: Clean the data
# -------------------------------------------
df['event_time'] = pd.to_datetime(df['event_time'])   # Convert time column to datetime format
df.dropna(inplace=True)                              # Drop rows with missing values

# -------------------------------------------
#  Step 4: Filter for purchase events only
# -------------------------------------------
df1 = df[df['event_type'] == 'purchase']     # Keep only rows where someone made a purchase

print(df1.info())                            # Show column info
print(df1.describe())                        # Show stats like min, max, avg (for price, etc.)

# -------------------------------------------
#  Step 5: Analyze Top Products by Revenue
# -------------------------------------------
top_products = df1.groupby('product_id')['price'].sum()         # Total revenue per product
top_products = top_products.sort_values(ascending=False).head(10)  # Top 10 products

# -------------------------------------------
#  Step 6: Plot Top 10 Products (Horizontal Bar Chart)
# -------------------------------------------
plt.figure(figsize=(10, 6))                              # Set chart size
plt.barh(top_products.index.astype(str), top_products.values)  # Horizontal bar chart
plt.xlabel("Total Revenue ($)")
plt.ylabel("Product ID")
plt.title("Top 10 Products by Revenue")
plt.gca().invert_yaxis()                                 # Highest product on top
plt.tight_layout()
plt.show()

# -------------------------------------------
# 📅 Step 7: Analyze Daily Revenue Trends
# -------------------------------------------
daily_revenue = df1.groupby(df1['event_time'].dt.date)['price'].sum()

# -------------------------------------------
# 📈 Plot Daily Revenue Over Time
# -------------------------------------------
plt.figure(figsize=(12, 6))
daily_revenue.plot(kind='line')
plt.title("Daily Revenue – October 2019")
plt.xlabel("Date")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()





