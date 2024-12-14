import pandas as pd
from sqlalchemy import create_engine

def from_postgres(connection_string, query):
    """
    Query data from a PostgreSQL database and return it as a DataFrame.
    
    Args:
        connection_string (str): SQLAlchemy connection string.
        query (str): SQL query to execute.
        
    Returns:
        pd.DataFrame: DataFrame containing the query results.
    """
    try:
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
        print(f"Executed query: {query}")
        return df
    except Exception as e:
        print(f"Error querying PostgreSQL: {e}")
        raise
