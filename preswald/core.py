from markdown import markdown
import pandas as pd
from sqlalchemy import create_engine

# Global store for connections and rendered components
connections = {}
_rendered_html = []


def text(markdown_str):
    """
    Render Markdown as HTML and store it in the global render list.

    Args:
        markdown_str (str): A string in Markdown format.
    """
    html = f"<div class='markdown-text'>{markdown(markdown_str)}</div>"
    _rendered_html.append(html)


def connect(source, name=None):
    """
    Connect to a data source such as a CSV, JSON, or database.

    Args:
        source (str): Path to a file or database connection string.
        name (str, optional): A unique name for the connection.
    """
    if name is None:
        name = f"connection_{len(connections) + 1}"

    try:
        if source.endswith(".csv"):
            connections[name] = pd.read_csv(source)
        elif source.endswith(".json"):
            connections[name] = pd.read_json(source)
        elif source.endswith(".parquet"):
            connections[name] = pd.read_parquet(source)
        elif source.startswith("postgres://") or source.startswith("mysql://"):
            engine = create_engine(source)
            connections[name] = engine
        else:
            raise ValueError(f"Unsupported data source format: {source}")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to source '{source}': {e}")

    return name


def get_connection(name):
    """
    Retrieve a connection by name.

    Args:
        name (str): The name of the connection.
    """
    if name not in connections:
        raise ValueError(f"No connection found with name '{name}'")
    return connections[name]


def view(connection_name, limit=50):
    """
    Render a data preview table based on the connection.

    Args:
        connection_name (str): Name of the connection to display.
        limit (int): Maximum number of rows to display.
    """
    connection = get_connection(connection_name)
    if isinstance(connection, pd.DataFrame):
        html_table = connection.head(limit).to_html(
            index=False, classes="table table-striped")
        _rendered_html.append(html_table)
    else:
        raise TypeError(
            f"Connection '{connection_name}' is not a valid DataFrame")


def get_rendered_html():
    """
    Retrieve all rendered components as a single HTML string.
    """
    global _rendered_html
    html_output = "".join(_rendered_html)
    _rendered_html.clear()
    return html_output


def execute_query(connection_name, query):
    """
    Execute a SQL query on a database connection.

    Args:
        connection_name (str): Name of the database connection.
        query (str): The SQL query to execute.
    """
    connection = get_connection(connection_name)

    if not isinstance(connection, create_engine().__class__):
        raise TypeError(
            f"Connection '{connection_name}' is not a database connection")

    with connection.connect() as conn:
        result = pd.read_sql(query, conn)
        return result


def plotly(fig):
    """
    Render a Plotly figure.

    Args:
        fig: A Plotly figure object.
    """
    html = fig.to_html(full_html=False, include_plotlyjs="cdn")
    _rendered_html.append(html)
