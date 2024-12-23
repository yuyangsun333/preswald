from markdown import markdown
import pandas as pd
from sqlalchemy import create_engine
from preswald.state import StateManager
from functools import wraps
from typing import Dict, Any
import json
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global store for connections and rendered components
connections = {}
_rendered_html = []
_component_states: Dict[str, Any] = {}

# Create a global state manager
state_manager = StateManager()


def track(func):
    """Decorator to track function calls and their dependencies"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Register this function call
        node_id = state_manager.track_function_call(func, args, kwargs)

        # Get or compute the result
        return state_manager.get_or_compute(node_id)

    return wrapper


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
            index=False, classes="table table-striped"
        )
        _rendered_html.append(html_table)
    else:
        raise TypeError(f"Connection '{connection_name}' is not a valid DataFrame")


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
        raise TypeError(f"Connection '{connection_name}' is not a database connection")

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


def update_component_state(component_id: str, value: Any):
    """Update the state of a component"""
    logger.debug(f"Updating state for component {component_id}: {value}")
    _component_states[component_id] = value
    
def get_component_state(component_id: str, default: Any = None) -> Any:
    """Get the current state of a component"""
    return _component_states.get(component_id, default)

def get_rendered_components():
    """Get all rendered components as JSON"""
    logger.debug(f"Getting rendered components, count: {len(_rendered_html)}")
    components = []
    
    # Create a set to track unique component IDs
    seen_ids = set()
    
    for item in _rendered_html:
        try:
            if isinstance(item, dict):
                # Only add component if we haven't seen its ID before
                if item.get('id') not in seen_ids:
                    components.append(item)
                    seen_ids.add(item.get('id'))
                    logger.debug(f"Added component: {item}")
            else:
                # Convert HTML string to component data
                component = {
                    "type": "html",
                    "content": str(item)
                }
                components.append(component)
                logger.debug(f"Converted HTML to component: {component}")
        except Exception as e:
            logger.error(f"Error processing component: {e}", exc_info=True)
    
    # Clear the rendered_html list after processing
    _rendered_html.clear()
    
    logger.info(f"Returning {len(components)} unique components")
    return components
