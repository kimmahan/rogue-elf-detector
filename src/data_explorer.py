import pandas as pd
import os
from pathlib import Path

# Get the absolute path to the data directory
data_dir = Path(__file__).parent.parent / 'data'

def explore_datasets():
    """Explore all CSV files in the data directory"""
    for file in data_dir.glob('*.csv'):
        print(f"\n{'='*50}")
        print(f"Examining: {file.name}")
        print(f"{'='*50}")
        
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Display basic information
        print("\nColumns:")
        print(df.columns.tolist())
        
        print("\nFirst few rows:")
        print(df.head(2))
        
        print("\nBasic information:")
        print(df.info())

if __name__ == "__main__":
    explore_datasets()