import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file and return it as a pandas DataFrame.

    Args:
        path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Raw data
    """
    try:
        df = pd.read_csv(path)
        print(f"[Ingest] Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print(f"[Ingest] File {path} not found.")
        raise
    except Exception as e:
        print(f"[Ingest] Failed to load CSV: {e}")
        raise