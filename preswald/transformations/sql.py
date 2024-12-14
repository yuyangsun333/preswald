from sqlalchemy import create_engine

def apply_sql(connection_string, sql_script):
    """
    Apply an SQL transformation to a database table.

    Args:
        connection_string (str): SQLAlchemy connection string to the database.
        sql_script (str): The SQL script to execute.

    Returns:
        None
    """
    try:
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(sql_script)
            print(f"Executed SQL script: {sql_script}")
            return result
    except Exception as e:
        print(f"Error applying SQL script: {e}")
        raise
