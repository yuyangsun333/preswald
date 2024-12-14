import pandas as pd

def clean_nulls(df, columns):
    """
    Remove rows with null values in the specified columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list): List of column names to check for nulls.

    Returns:
        pd.DataFrame: DataFrame with rows containing nulls removed.
    """
    return df.dropna(subset=columns)

def deduplicate(df, key_columns):
    """
    Remove duplicate rows based on key columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        key_columns (list): List of columns to use as keys for deduplication.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    return df.drop_duplicates(subset=key_columns)

def filter_data(df, condition):
    """
    Filter rows based on a condition.

    Args:
        df (pd.DataFrame): The input DataFrame.
        condition (str): A pandas query string to filter the data.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    return df.query(condition)
