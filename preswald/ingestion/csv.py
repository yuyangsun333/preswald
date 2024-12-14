import pandas as pd

def from_csv(file_path):
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded data from {file_path}.")
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        raise
