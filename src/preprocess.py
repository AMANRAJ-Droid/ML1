import pandas as pd

META_COLS = [
    "sleep_hours", "energy_level", "stress_level", "duration_min"
]

def clean_data(df):
    df = df.copy()

    df["journal_text"] = df["journal_text"].fillna("")

    for col in META_COLS:
        df[col] = df[col].fillna(df[col].median())

    return df