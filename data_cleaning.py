# data_cleaning.py
import pandas as pd
import re

def clean_data(input_csv, output_csv):
    # Read raw data
    df = pd.read_csv(input_csv)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Remove currency symbols and commas from 'Selling Price' and convert to float
    df["Selling Price"] = df["Selling Price"].apply(
        lambda x: re.sub(r'[₹,]', '', str(x)) if x != "N/A" else None
    )
    df["Selling Price"] = pd.to_numeric(df["Selling Price"], errors="coerce")
    
    # Remove commas and any non-numeric characters from Reviews and convert to integer
    df["Reviews"] = df["Reviews"].apply(
        lambda x: re.sub(r'[,\+]', '', str(x)) if x != "0" else "0"
    )
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    
    # Convert Rating to numeric
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    
    # Drop rows with missing selling price (or other essential fields if needed)
    df.dropna(subset=["Selling Price"], inplace=True)
    
    df.to_csv(output_csv, index=False)
    print(f"Data cleaned and saved to {output_csv}")

if __name__ == "__main__":
    clean_data("amazon_soft_toys_raw.csv", "amazon_soft_toys_clean.csv")
