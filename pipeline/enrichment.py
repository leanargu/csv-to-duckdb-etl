from datetime import timedelta

import pandas as pd
import numpy as np

LAST_UPDATED_FIELD = 'Last Updated'

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns like is_premium, install_bucket, rating_label.

    Args:
        df (pd.DataFrame): Cleaned data

    Returns:
        pd.DataFrame: Enriched data
    """
    df = df.copy()

    df['is_premium'] = get_premium_apps(df)

    df['install_bucket'] = get_bucket_installs(df)

    df['rating_label'] = get_rating_level(df)

    df['is_discontinued'] = get_discontinued_apps(df)

    print(f"[Enrich] Enriched dataset with {df.shape[1]} columns.")
    return df


def get_rating_level(df: pd.DataFrame) -> pd.DataFrame:
    return pd.cut(
        df['Rating'],
        bins=[-1, 2, 3.5, 4.5, 5],
        labels=['Mala', 'Regular', 'Buena', 'Excelente']
    )


def get_bucket_installs(df: pd.DataFrame) -> pd.DataFrame:
    bins = [-1, 1000, 100000, 1000000, np.inf]
    labels = ['<1k', '1k-100k', '100k-1M', '+1M']
    return pd.cut(df['Installs'], bins=bins, labels=labels)


def get_premium_apps(df: pd.DataFrame) -> pd.DataFrame:
    return (df['Type'] == 'Paid') & (df['Price'] > 10)

def get_discontinued_apps(df: pd.DataFrame) -> pd.Series:
    parsed_dates = pd.to_datetime(df[LAST_UPDATED_FIELD], errors='coerce')

    not_null_dates = parsed_dates.notna()
    most_recent = parsed_dates[not_null_dates].max()

    return not_null_dates & ((most_recent - parsed_dates) > timedelta(days=365))