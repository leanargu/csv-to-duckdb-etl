import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataset: fix types, remove bad characters, standardize values.

    Args:
        df (pd.DataFrame): Raw data

    Returns:
        pd.DataFrame: Cleaned data
    """
    df = df.copy()

    # Clean Installs
    df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)

    # Clean Price
    df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Clean Size
    df['Size'] = df['Size'].replace('Varies with device', np.nan)
    df['Size'] = df['Size'].str.replace('M', '', regex=False)

    kb_mask = df['Size'].str.endswith('k', na=False)
    df.loc[kb_mask, 'Size'] = df.loc[kb_mask, 'Size'].str.replace('k', '', regex=False)
    df.loc[kb_mask, 'Size'] = df.loc[kb_mask, 'Size'].astype(float) / 1024

    df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

    # Clean Rating
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Clean Type
    df.loc[df['Type'] == '0', 'Type'] = 'Free'

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    print(f"[Clean] Cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df