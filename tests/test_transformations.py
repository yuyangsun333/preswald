import pandas as pd
from preswald.transformations import clean_nulls, deduplicate, filter_data

def test_clean_nulls():
    df = pd.DataFrame({"a": [1, 2, None], "b": [4, 5, 6]})
    result = clean_nulls(df, ["a"])
    assert result.shape[0] == 2  # Two rows should remain

def test_deduplicate():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [4, 4, 5]})
    result = deduplicate(df, ["a"])
    assert result.shape[0] == 2  # Two unique rows should remain

def test_filter_data():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    result = filter_data(df, "a > 1")
    assert result.shape[0] == 2  # Two rows where a > 1 should remain
