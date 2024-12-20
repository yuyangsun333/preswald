import pandas as pd
from preswald.core import connections, get_connection


def view(connection_name, limit=100):
    """
    Render a preview of the data from a connection as an HTML table.

    Args:
        connection_name (str): The name of the data connection.
        limit (int): Maximum number of rows to display in the table.
    Returns:
        str: HTML string containing the table representation of the data.
    """
    # Fetch the connection object
    connection = get_connection(connection_name)

    # Check if it's a pandas DataFrame
    if isinstance(connection, pd.DataFrame):
        # Limit rows and convert to HTML
        table_html = connection.head(limit).to_html(
            classes="table", index=False)
        return f"<div>{table_html}</div>"
    else:
        raise TypeError("Unsupported data type for rendering as a table.")


def query(connection_name, sql_query):
    """
    Execute a SQL query on a database connection and return the result as a DataFrame.

    Args:
        connection_name (str): The name of the database connection.
        sql_query (str): The SQL query to execute.
    Returns:
        pd.DataFrame: Query results as a pandas DataFrame.
    """
    # Get the connection object
    connection = get_connection(connection_name)

    # Ensure the connection is a SQLAlchemy engine
    if not hasattr(connection, "execute"):
        raise TypeError(
            f"Connection '{connection_name}' is not a database connection.")

    # Execute the query and return results as a DataFrame
    with connection.connect() as conn:
        result_df = pd.read_sql(sql_query, conn)
    return result_df


def summary(connection_name):
    """
    Generate a summary of the data from a connection.

    Args:
        connection_name (str): The name of the data connection.
    Returns:
        str: HTML representation of the data summary.
    """
    # Fetch the connection object
    connection = get_connection(connection_name)

    if isinstance(connection, pd.DataFrame):
        # Generate summary statistics for numeric columns
        summary_df = connection.describe(include="all")
        summary_html = summary_df.to_html(classes="table", index=True)
        return f"<div><h3>Data Summary</h3>{summary_html}</div>"
    else:
        raise TypeError("Unsupported data type for generating summary.")


def save(connection_name, file_path, format="csv"):
    """
    Save data from a connection to a file.

    Args:
        connection_name (str): The name of the data connection.
        file_path (str): Path to save the file.
        format (str): Format to save the data in ('csv', 'json', 'parquet').
    Returns:
        str: Success message.
    """
    # Get the connection object
    connection = get_connection(connection_name)

    if not isinstance(connection, pd.DataFrame):
        raise TypeError(
            f"Connection '{connection_name}' does not contain tabular data.")

    # Save the data in the specified format
    if format == "csv":
        connection.to_csv(file_path, index=False)
    elif format == "json":
        connection.to_json(file_path, orient="records")
    elif format == "parquet":
        connection.to_parquet(file_path, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")

    return f"Data saved to {file_path} in {format} format."


def load(file_path, name=None):
    """
    Load data from a file and store it as a new connection.

    Args:
        file_path (str): Path to the file.
        name (str, optional): Name of the new connection. Defaults to None.
    Returns:
        str: The name of the created connection.
    """
    from preswald.core import connect

    # Use the `connect` function to load the file into a connection
    connection_name = connect(file_path, name=name)
    return connection_name
