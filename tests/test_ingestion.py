import pandas as pd
from preswald.ingestion import from_csv, from_api, from_postgres

def test_from_csv():
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df.to_csv("test.csv", index=False)
    
    loaded_data = from_csv("test.csv")
    assert isinstance(loaded_data, pd.DataFrame)
    assert loaded_data.shape == df.shape

def test_from_api(mocker):
    mocker.patch("requests.get", return_value=mocker.Mock(
        status_code=200, 
        json=lambda: [{"key": "value"}]
    ))
    
    data = from_api("http://fakeapi.com")
    assert isinstance(data, pd.DataFrame)
    assert "key" in data.columns

# Add tests for from_postgres and from_google_sheets as needed
