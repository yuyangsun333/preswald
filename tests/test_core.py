import pytest
import pandas as pd
from preswald.core import text, connect, get_connection


def test_text():
    markdown_input = "# Hello, World!"
    result = text(markdown_input)
    assert "<h1>Hello, World!</h1>" in result


def test_connect_csv(tmpdir):
    # Create a temporary CSV file
    csv_path = tmpdir.join("test.csv")
    csv_path.write("name,age\nAlice,30\nBob,25")

    connection_name = connect(str(csv_path), "test_csv")
    connection = get_connection(connection_name)
    assert isinstance(connection, pd.DataFrame)
    assert len(connection) == 2
    assert "name" in connection.columns


def test_connect_json(tmpdir):
    # Create a temporary JSON file
    json_path = tmpdir.join("test.json")
    json_path.write(
        '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]')

    connection_name = connect(str(json_path), "test_json")
    connection = get_connection(connection_name)
    assert isinstance(connection, pd.DataFrame)
    assert len(connection) == 2
    assert "name" in connection.columns
