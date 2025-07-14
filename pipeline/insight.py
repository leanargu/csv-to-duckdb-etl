import pandas as pd

def generate_insights(df: pd.DataFrame) -> None:
    """
    Set up useful views: calculate and save insights without modifying original
    pipeline data.

    Args:
        df (pd.DataFrame): Raw data

    Returns:
        None
    """
    export_insights({
        'top_5_categories_by_excelent_ratio': get_top_5_categories_by_excelent_ratio(df),
        'weird_apps': get_weird_apps(df),
        'best_apps_stats': get_best_apps_stats(df)
    })

def get_top_5_categories_by_excelent_ratio(df: pd.DataFrame) -> pd.DataFrame:
    is_excellent = df["rating_label"] == "Excelente"  # Series<bool>

    excellent_share = (
        is_excellent
        .groupby(df["Category"])  # align by index
        .mean()  # proportion of True values
        .round(2)  # same precision as SQL ROUND(..., 2)
    )

    return (
        excellent_share
        .sort_values(ascending=False)  # highest proportion first
        .head(5)
        .reset_index(name="excellent_apps_percentage")
    )

def get_weird_apps(df: pd.DataFrame) -> pd.DataFrame:
    is_premium          = df["is_premium"] == True
    has_low_rating      = df["rating_label"].isin(["Malo", "Regular"])
    mid_install_bucket  = df["install_bucket"] == "100k-1M"

    rare_apps_mask = is_premium & has_low_rating & mid_install_bucket

    return df.loc[rare_apps_mask, "App"]

def get_best_apps_stats(df: pd.DataFrame) -> pd.DataFrame:
    NUMERIC_COLS = ["Size", "Price"]

    best_apps = df[
        (df["Installs"] > 1_000_000) &
        (df["rating_label"] == "Excelente")
        ]
    best_stats = best_apps[NUMERIC_COLS].mean()

    global_apps = df[df["Size"].notna()]  # descartá Size = NULL/NaN
    global_stats = global_apps[NUMERIC_COLS].mean()

    summary = (
        pd.concat(
            {"best_apps": best_stats, "global_avg": global_stats},
            axis=1
        )
        .T
        .round(2)
    )

    return summary

def export_insights(files_with_name: dict) -> None:
    for file_name, df in files_with_name.items():
        if df is not None: df.to_csv(f"./resources/delivery/insights/{file_name}.csv", index=False)
        else: print(f"{file_name}.csv was not printed because is empty.")