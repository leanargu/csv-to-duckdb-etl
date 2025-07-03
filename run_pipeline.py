from pipeline import (ingest, clean, enrichment, persist)

df_raw = ingest.load_csv("resources/ingest/googleplaystore.csv")
df_cleaned = clean.clean_data(df_raw)
df_enriched = enrichment.add_derived_columns(df_cleaned)
persist.save_to_duckdb(
    df_enriched,
    "enriched_apps",
    "./resources/delivery/enriched_apps.duckdb"
)