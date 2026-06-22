import pandas as pd
import sys

df = pd.read_csv('casinos_export.csv')
print('=== BASIC INFO ===')
print(f'Total rows: {len(df)}')
print(f'Total columns: {len(df.columns)}')
print(f'\n=== COLUMNS ===')
for i, col in enumerate(df.columns):
    print(f'  {i}: {col}')
print(f'\n=== MISSING DATA SUMMARY ===')
for col in df.columns:
    missing = df[col].isna().sum()
    empty = (df[col].astype(str).str.strip() == '').sum()
    unknown = df[col].astype(str).str.lower().isin(['unknown', 'n/a', 'na', 'none', 'null', '']).sum()
    pct = (len(df) - missing) / len(df) * 100
    print(f'  {col}: {missing} NaN, {empty} empty, {unknown} unknown/na -> {pct:.1f}% complete')
print(f'\n=== SAMPLE ROWS ===')
print(df.head(3).to_string())