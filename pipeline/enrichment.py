import pandas as pd
import numpy as np

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns like is_premium, install_bucket, rating_label.

    Args:
        df (pd.DataFrame): Cleaned data

    Returns:
        pd.DataFrame: Enriched data
    """
    df = df.copy()

    # Columna: is_premium
    df['is_premium'] = (df['Type'] == 'Paid') & (df['Price'] > 10)

    # Columna: install_bucket
    bins = [-1, 1000, 100000, 1000000, np.inf]
    labels = ['<1k', '1k-100k', '100k-1M', '+1M']
    df['install_bucket'] = pd.cut(df['Installs'], bins=bins, labels=labels)

    # Columna: rating_label
    df['rating_label'] = pd.cut(
        df['Rating'],
        bins=[-1, 2, 3.5, 4.5, 5],
        labels=['Mala', 'Regular', 'Buena', 'Excelente']
    )

    print(f"[Enrich] Enriched dataset with {df.shape[1]} columns.")
    return df