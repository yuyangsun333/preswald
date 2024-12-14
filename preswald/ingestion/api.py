import requests
import pandas as pd

def from_api(url, headers=None, params=None):
    """
    Fetch data from a REST API endpoint and return it as a DataFrame.
    
    Args:
        url (str): The API endpoint URL.
        headers (dict, optional): Request headers.
        params (dict, optional): Query parameters.
    
    Returns:
        pd.DataFrame: DataFrame containing the API response data.
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Assume the response is a list of records
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unsupported response format.")
        
        print(f"Loaded data from API: {url}")
        return df
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        raise
