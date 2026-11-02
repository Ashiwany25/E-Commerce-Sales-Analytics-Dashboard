
import pandas as pd
from pathlib import Path

# Locate the raw dataset folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data" / "raw"

# Find all CSV files
csv_files = sorted(data_folder.glob("*.csv"))

print("Total CSV files found:", len(csv_files))

# Read and examine each dataset
for file in csv_files:
    print("\n" + "=" * 60)
    print("Dataset:", file.name)

    df = pd.read_csv(file)

    print("\nShape (Rows, Columns):")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

print("\nDataset exploration completed!")
