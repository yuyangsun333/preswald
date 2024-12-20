from markdown import markdown
import pandas as pd
from sqlalchemy import create_engine

# Store connections globally
connections = {}


def text(markdown_str):
    """
    Render Markdown as HTML.

    Args:
        markdown_str (str): A string in Markdown format.
    Returns:
        str: Rendered HTML string.
    """
    html = markdown(markdown_str)
    return f"<div>{html}</div>"


def connect(source, name=None):
    """
    Connect to a data source such as a CSV, JSON, or database.

    Args:
        source (str): Path to a file or database connection string.
        name (str, optional): A unique name for the connection. Defaults to None.
    Returns:
        str: The name of the connection.
    """
    if name is None:
        name = f"connection_{len(connections) + 1}"

    try:
        if source.endswith(".csv"):
            # Connect to a CSV file
            connections[name] = pd.read_csv(source)
        elif source.endswith(".json"):
            # Connect to a JSON file
            connections[name] = pd.read_json(source)
        elif source.endswith(".parquet"):
            # Connect to a Parquet file
            connections[name] = pd.read_parquet(source)
        elif source.startswith("postgres://") or source.startswith("mysql://"):
            # Connect to a SQL database
            engine = create_engine(source)
            connections[name] = engine
        else:
            raise ValueError(f"Unsupported data source format: {source}")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to source '{source}': {str(e)}")

    return name


def get_connection(name):
    """
    Retrieve a connection by name.

    Args:
        name (str): The name of the connection.
    Returns:
        object: The data or connection object.
    """
    if name not in connections:
        raise ValueError(f"No connection found with name '{name}'")
    return connections[name]


def execute_query(connection_name, query):
    """
    Execute a SQL query on a database connection.

    Args:
        connection_name (str): The name of the database connection.
        query (str): The SQL query to execute.
    Returns:
        pd.DataFrame: The query result as a pandas DataFrame.
    """
    connection = get_connection(connection_name)

    if not isinstance(connection, create_engine().__class__):
        raise TypeError(
            f"Connection '{connection_name}' is not a database connection")

    with connection.connect() as conn:
        result = pd.read_sql(query, conn)

    return result
